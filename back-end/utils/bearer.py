import os
from jose import jwt
from fastapi import FastAPI,Depends,HTTPException,status,Request
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import json


token_expiry_minutes=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
algorithm=os.getenv('ALGORITHM')
secret_key=os.getenv('JWT_SECRET_KEY')
refresh_token_expiry_minutes=os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

def decodeJWT(jwttoken:str):
    try:
        payload=jwt.decode(jwttoken,secret_key,algorithm)
        return payload
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Token")


class JWTBearer(HTTPBearer):
    def __init__(self,auto_error:bool=True):
        super(JWTBearer,self).__init__(auto_error=auto_error)

    async def __call__(self, request:Request):
        credentials:HTTPAuthorizationCredentials=await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403,detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token or expired token")
            return self.verify_jwt(credentials.credentials)
        else:
            raise HTTPException(status_code=403,detail="invalid authroization code")

    def verify_jwt(self,jwtoken:str)-> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload=None

        if payload:
            payload_data = payload.get('sub', '')
            data = json.loads(payload_data.replace("'", "\""))
            #user_id = data.get('id')
            isTokenValid = True
            return data

#JWTBearer=JWTBearer()