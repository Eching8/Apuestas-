import unittest

from apuestas.api_football import ApiError, ApiFootball, PresupuestoAgotado


class Respuesta:
    def __init__(self, data, status=200, headers=None):
        self._data, self.status_code, self.headers = data, status, headers or {}

    def json(self):
        return self._data

    def raise_for_status(self):
        pass


class SesionFalsa:
    """Imita API-Football: /status gratis y un contador de peticiones del día."""

    def __init__(self, usadas: int, limite: int = 100):
        self.usadas, self.limite, self.headers, self.llamadas = usadas, limite, {}, []

    def get(self, url, params=None, headers=None, timeout=None):
        self.llamadas.append(url)
        if url.endswith("/status"):
            return Respuesta({"errors": [], "response": {"requests": {"current": self.usadas,
                                                                      "limit_day": self.limite}}})
        self.usadas += 1
        return Respuesta({"errors": [], "response": [{"ok": 1}]},
                         headers={"x-ratelimit-requests-remaining": str(self.limite - self.usadas),
                                  "x-ratelimit-remaining": "9"})


class LimiteDiarioTest(unittest.TestCase):
    def setUp(self):
        import apuestas.api_football as af
        self._intervalo, af.MIN_INTERVALO = af.MIN_INTERVALO, 0.0

    def tearDown(self):
        import apuestas.api_football as af
        af.MIN_INTERVALO = self._intervalo

    def test_respeta_lo_ya_usado_hoy_y_la_reserva(self):
        s = SesionFalsa(usadas=85)
        api = ApiFootball("clave", presupuesto=60, session=s, reserva=10, registro=None)
        self.assertEqual(api.presupuesto, 5)          # 100 - 85 - 10
        for _ in range(5):
            api.partido(1)
        with self.assertRaises(PresupuestoAgotado):
            api.partido(1)
        self.assertEqual(s.usadas, 90)               # nunca toca las 10 de reserva

    def test_varias_ejecuciones_suman(self):
        s = SesionFalsa(usadas=0)
        for _ in range(4):                           # p. ej. diario + varios chequeos
            api = ApiFootball("clave", presupuesto=30, session=s, reserva=10, registro=None)
            try:
                while True:
                    api.partido(1)
            except PresupuestoAgotado:
                pass
        self.assertEqual(s.usadas, 90)

    def test_sin_estado_no_arranca(self):
        class Rota(SesionFalsa):
            def get(self, url, **kw):
                raise OSError("sin red")
        with self.assertRaises(ApiError):
            ApiFootball("clave", session=Rota(0), registro=None)


class PrioridadTest(unittest.TestCase):
    def test_orden_y_solo_tarjetas(self):
        from apuestas.config import Config, ligas_filtro, prioridad
        c = Config(ligas=[2, 39, 140], ligas_solo_tarjetas=[239])
        self.assertEqual(ligas_filtro(c), [2, 39, 140, 239])
        self.assertLess(prioridad(c, 2), prioridad(c, 140))
        self.assertLess(prioridad(c, 140), prioridad(c, 239))
        self.assertEqual(ligas_filtro(Config(ligas=[], ligas_solo_tarjetas=[239])), [])


class RegistroTest(unittest.TestCase):
    def test_status_atrasado_no_engana(self):
        import tempfile
        from pathlib import Path
        import apuestas.api_football as af
        intervalo, af.MIN_INTERVALO = af.MIN_INTERVALO, 0.0
        try:
            with tempfile.TemporaryDirectory() as tmp:
                reg = Path(tmp) / "uso.json"

                class Atrasada(SesionFalsa):
                    """/status siempre dice 0 (como la API real, que se actualiza con retraso)."""
                    def get(self, url, params=None, headers=None, timeout=None):
                        if url.endswith("/status"):
                            return Respuesta({"errors": [], "response": {"requests": {"current": 0,
                                                                                      "limit_day": 100}}})
                        return super().get(url, params, headers, timeout)

                s = Atrasada(usadas=0)
                for _ in range(5):
                    api = ApiFootball("clave", presupuesto=40, session=s, reserva=10, registro=reg)
                    try:
                        while True:
                            api.partido(1)
                    except PresupuestoAgotado:
                        pass
                self.assertEqual(s.usadas, 90)
        finally:
            af.MIN_INTERVALO = intervalo


if __name__ == "__main__":
    unittest.main()
