import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


def hash_password(password):
    """
    Hacher un mot de passe pour le stockage.
    """
    return generate_password_hash(password)


def check_password(hashed_password, password):
    """
    Vérifier un mot de passe haché avec le mot de passe fourni.
    """
    return check_password_hash(hashed_password, password)


def generate_jwt(user_id, roles=None, expiration=600):
    """
    Générer un token JWT pour un utilisateur.
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'roles': roles or []  # Inclure les rôles de l'utilisateur
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_jwt(token):
    """
    Décoder un token JWT pour extraire les informations de l'utilisateur.
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide


def get_user_id_from_token(token):
    """
    Extraire l'ID de l'utilisateur à partir du token JWT.
    """
    payload = decode_jwt(token)
    if payload:
        return payload['sub']
    return None


def get_user_roles_from_token(token):
    """
    Extraire les rôles de l'utilisateur à partir du token JWT.
    """
    payload = decode_jwt(token)
    if payload and 'roles' in payload:
        return payload['roles']
    return []


def refresh_jwt(token, expiration=600):
    """
    Rafraîchir un token JWT existant en prolongeant sa validité.
    """
    payload = decode_jwt(token)
    if payload:
        new_payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration),
            'iat': datetime.datetime.utcnow(),
            'sub': payload['sub'],
            'roles': payload.get('roles', [])
        }
        return jwt.encode(new_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return None


def require_role(token, required_role):
    """
    Vérifier si un utilisateur a le rôle requis.
    """
    roles = get_user_roles_from_token(token)
    if required_role in roles:
        return True
    return False
