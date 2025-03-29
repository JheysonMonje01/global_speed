class APIException(Exception):
    """Clase base para excepciones personalizadas"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

class UserNotFoundException(APIException):
    """Excepción para usuario no encontrado"""
    def __init__(self):
        super().__init__("User not found", 404)

class InvalidCredentialsException(APIException):
    """Excepción para credenciales inválidas"""
    def __init__(self):
        super().__init__("Invalid credentials", 401)

class UnauthorizedAccessException(APIException):
    """Excepción para acceso no autorizado"""
    def __init__(self):
        super().__init__("Unauthorized access", 403)
