# backend/auth.py
from jose import jwt
import requests
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

AUTH0_DOMAIN = "dev-lgjtqkcbt2po3fk1.us.auth0.com"  # e.g. dev-xyz.us.auth0.com
API_AUDIENCE = "https://dev-lgjtqkcbt2po3fk1.us.auth0.com/api/v2/"  # Same as audience
ALGORITHMS = ["RS256"]

bearer_scheme = HTTPBearer()

def get_jwks():
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    return requests.get(url).json()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header['kid']

        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
        if key is None:
            raise Exception("Public key not found")

        payload = jwt.decode(
            token,
            key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )

        return payload  # contains sub (user ID), name, etc.
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        )
