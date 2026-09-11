"""Credenciales del administrador principal de PowerFit."""

import hashlib
import hmac


class Admin:
    """Representa al administrador que autoriza la gestión del sistema."""

    ID = "17310447-2"
    PASSWORD_HASH = (
        "pbkdf2_sha256$600000$8f7c2b1a4d6e8091a2b3c4d5e6f70819$"
        "3a110e0d22abf81f85c2ecbdc62b2b734c2755e9603ee2f248e5daf50de2be40"
    )

    def autenticar(self, password: str) -> bool:
        """Comprueba la contraseña del administrador contra su hash fijo."""
        try:
            algoritmo, iteraciones, sal, resumen = self.PASSWORD_HASH.split("$", 3)
            if algoritmo != "pbkdf2_sha256":
                return False
            calculado = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                bytes.fromhex(sal),
                int(iteraciones),
            ).hex()
            return hmac.compare_digest(calculado, resumen)
        except (TypeError, ValueError):
            return False