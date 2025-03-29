import bcrypt

def hash_password(password):
    """Genera un hash seguro de la contraseña"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password, hashed_password):
    """Verifica si la contraseña ingresada coincide con el hash almacenado"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def is_password_secure(password):
    """Verifica si la contraseña cumple con los requisitos de seguridad"""
    return (
        any(char.isdigit() for char in password) and  # Al menos un número
        any(char.isupper() for char in password) and  # Al menos una mayúscula
        any(char.islower() for char in password) and  # Al menos una minúscula
        len(password) >= 8  # Longitud mínima
    )
