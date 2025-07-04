from fastapi import Depends
from fastapi import Request
import json
from fastapi import HTTPException

def get_current_user_id(request: Request):
    user_info = request.headers.get('x-user-info')
    
    if user_info:
        user_info = json.loads(user_info)
        user_id = user_info.get('data').get('id')
        return user_id
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")