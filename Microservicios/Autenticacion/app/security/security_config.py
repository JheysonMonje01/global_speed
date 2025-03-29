class SecurityConfig:
    """Configuraciones de seguridad del sistema"""

    MAX_LOGIN_ATTEMPTS = 5  # Intentos fallidos antes de bloquear la cuenta
    LOCKOUT_TIME_MINUTES = 30  # Tiempo de bloqueo después de fallar
    PASSWORD_RESET_EXPIRY = 60  # Minutos de expiración del token de recuperación
    SESSION_TIMEOUT_MINUTES = 15  # Tiempo de expiración de sesión inactiva

    @staticmethod
    def get_password_complexity():
        """Reglas de complejidad de contraseñas"""
        return {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_digit": True
        }
