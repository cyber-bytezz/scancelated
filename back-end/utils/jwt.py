# load env
from dotenv import load_dotenv
load_dotenv(override=True)


import os
from datetime import datetime,timedelta
from typing import Union,Any
from jose import jwt


token_expiry_minutes=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
algorithm=os.getenv('ALGORITHM')
secret_key=os.getenv('JWT_SECRET_KEY')
refresh_token_expiry_minutes=os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')



def create_access_token(subject:Union[str,Any],expires_delta:int=None)->str:
    if expires_delta is not None:
        expires_delta=datetime.utcnow()+expires_delta

    else:
        expires_delta=datetime.utcnow()+timedelta(minutes=int(token_expiry_minutes))

    to_encode={"exp":expires_delta,"sub":str(subject)}
    encoded_jwt=jwt.encode(to_encode,secret_key,algorithm)
    return encoded_jwt


