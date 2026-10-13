import sys
from pathlib import Path
from typing import Optional

# Intentar importar argon2; si se ejecuta con el Python global del sistema,
# auto-detectar e incorporar el site-packages del entorno virtual .venv del proyecto.
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError, InvalidHashError, VerificationError
except ModuleNotFoundError:
    raiz = Path(__file__).resolve().parent.parent.parent
    for venv_path in raiz.glob(".venv/lib/python*/site-packages"):
        if venv_path.exists() and str(venv_path) not in sys.path:
            sys.path.append(str(venv_path))
    try:
        from argon2 import PasswordHasher
        from argon2.exceptions import VerifyMismatchError, InvalidHashError, VerificationError
    except ModuleNotFoundError:
        PasswordHasher = None
        VerifyMismatchError = InvalidHashError = VerificationError = Exception


class GestorSeguridad:
    """Componente centralizado para hashing y verificación de contraseñas mediante Argon2id."""

    # Utiliza la API de alto nivel de argon2-cffi con parámetros seguros predeterminados de Argon2id (RFC 9106)
    _hasher = PasswordHasher() if PasswordHasher is not None else None

    @classmethod
    def es_hash_argon2(cls, valor: Optional[str]) -> bool:
        """Determina si una cadena ya posee el formato de hash Argon2id codificado."""
        if not valor or not isinstance(valor, str):
            return False
        return valor.startswith("$argon2id$") or valor.startswith("$argon2")

    @classmethod
    def hashear_password(cls, password_plano: str) -> str:
        """
        Genera un hash Argon2id con salt criptográfico codificado internamente.
        Si la cadena ya es un hash Argon2id válido, la retorna intacta para evitar re-hashear.
        """
        if not password_plano or not isinstance(password_plano, str):
            raise ValueError("La contraseña no puede estar vacía.")
        if cls.es_hash_argon2(password_plano):
            return password_plano
        if cls._hasher is None:
            raise RuntimeError("argon2-cffi no está disponible en el entorno. Instálelo con: pip install argon2-cffi")
        return cls._hasher.hash(password_plano)

    @classmethod
    def verificar_password(cls, hash_almacenado: Optional[str], password_intent: str) -> bool:
        """
        Verifica una contraseña en texto plano contra el hash almacenado en formato Argon2id.
        Maneja de forma segura contraseñas incorrectas y hashes inválidos/corruptos,
        sin filtrar datos sensibles ni romper el flujo de ejecución.
        """
        if cls._hasher is None:
            return False
        if not hash_almacenado or not password_intent:
            return False
        if not isinstance(hash_almacenado, str) or not isinstance(password_intent, str):
            return False
        try:
            return cls._hasher.verify(hash_almacenado, password_intent)
        except (VerifyMismatchError, InvalidHashError, VerificationError):
            return False
        except Exception:
            return False
