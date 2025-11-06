from typing import Dict, Any, Optional
from jose import jwt, JWTError
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import requests
from app.core.config import settings


def get_jwks() -> Dict[str, Any]:
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()


def get_rsa_key(token: str, jwks: Dict[str, Any]):
    unverified_header = jwt.get_unverified_header(token)
    jwk = None
    
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            jwk = key
            break
    
    if not jwk:
        raise JWTError("Unable to find appropriate key")
    
    def base64url_decode(value: str) -> bytes:
        padding = 4 - len(value) % 4
        if padding != 4:
            value += "=" * padding
        return base64.urlsafe_b64decode(value)
    
    n_bytes = base64url_decode(jwk["n"])
    e_bytes = base64url_decode(jwk["e"])
    
    n_int = int.from_bytes(n_bytes, byteorder="big")
    e_int = int.from_bytes(e_bytes, byteorder="big")
    
    public_key = rsa.RSAPublicNumbers(e_int, n_int).public_key(default_backend())
    
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return pem


def verify_auth0_token(token: str) -> Dict[str, Any]:
    try:
        jwks = get_jwks()
        rsa_key = get_rsa_key(token, jwks)
        
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=settings.AUTH0_ALGORITHMS,
            audience=settings.AUTH0_API_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
            options={"verify_signature": True, "verify_aud": True, "verify_exp": True}
        )
        
        return payload
        
    except JWTError as e:
        error_msg = str(e)
        if "expired" in error_msg.lower():
            raise JWTError(f"Token has expired: {error_msg}")
        elif "audience" in error_msg.lower() or "aud" in error_msg.lower():
            raise JWTError(f"Token audience mismatch. Expected: {settings.AUTH0_API_AUDIENCE}. Error: {error_msg}")
        elif "issuer" in error_msg.lower() or "iss" in error_msg.lower():
            raise JWTError(f"Token issuer mismatch. Expected: https://{settings.AUTH0_DOMAIN}/. Error: {error_msg}")
        elif "signature" in error_msg.lower():
            raise JWTError(f"Token signature verification failed: {error_msg}")
        else:
            raise JWTError(f"Token verification failed: {error_msg}")
    except Exception as e:
        raise Exception(f"Error verifying token: {str(e)}")


def verify_id_token(id_token: str) -> Dict[str, Any]:
    try:
        jwks = get_jwks()
        rsa_key = get_rsa_key(id_token, jwks)
        
        payload = jwt.decode(
            id_token,
            rsa_key,
            algorithms=settings.AUTH0_ALGORITHMS,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
            options={"verify_signature": True, "verify_aud": False, "verify_exp": True}
        )
        
        if not payload.get("sub"):
            available_claims = list(payload.keys())
            raise JWTError(f"ID token missing required claim: sub. Available claims: {available_claims}")
        
        return payload
        
    except JWTError as e:
        raise JWTError(f"ID token verification failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error verifying ID token: {str(e)}")

