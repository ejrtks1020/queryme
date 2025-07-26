from fastapi import Request, HTTPException
import json

def get_current_user_id(request: Request):
    user_info = request.headers.get('x-user-info')
    user_id = request.headers.get('x-user-id')
    if user_info:
        user_info = json.loads(user_info)
        user_id = user_info.get('data').get('id')
        return user_id
    elif user_id:
        return user_id
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

def get_trace_info(request: Request):
    trace_id = request.headers.get('x-trace-id')
    session_id = request.headers.get('x-session-id')
    span_id = request.headers.get('x-span-id')
    parent_span_id = request.headers.get('x-parent-span-id')
    request_id = request.headers.get('x-request-id')
    correlation_id = request.headers.get('x-correlation-id')
    trace_info = {
        "x-trace-id": trace_id,
        "x-session-id": session_id,
        "x-span-id": span_id,
        "x-parent-span-id": parent_span_id,
        "x-request-id": request_id,
        "x-correlation-id": correlation_id
    }
    return trace_info