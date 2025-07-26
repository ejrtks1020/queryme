from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import uuid

class Tracer(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        
    async def dispatch(self, request: Request, call_next):
        # 기존 헤더에서 trace 정보 추출
        span_id = request.headers.get('x-span-id')

        # 새로운 span-id 생성 및 parent-span-id 설정
        new_span_id = str(uuid.uuid4())
        new_parent_span_id = span_id  # 현재 span-id를 parent로 설정

        # request.scope의 headers를 업데이트
        # headers는 (name, value) 튜플의 리스트 형태로 저장됨
        updated_headers = []
        header_names_updated = set()
        
        # 기존 헤더들을 순회하면서 trace 관련 헤더는 새 값으로 대체
        for name_bytes, value_bytes in request.scope['headers']:
            name = name_bytes.decode('utf-8').lower()
            if name == 'x-span-id':
                updated_headers.append((b'x-span-id', new_span_id.encode('utf-8')))
                header_names_updated.add('x-span-id')
            elif name == 'x-parent-span-id':
                if new_parent_span_id:
                    updated_headers.append((b'x-parent-span-id', new_parent_span_id.encode('utf-8')))
                header_names_updated.add('x-parent-span-id')
            else:
                updated_headers.append((name_bytes, value_bytes))
        
        # 새로운 헤더가 기존에 없었다면 추가
        if 'x-span-id' not in header_names_updated:
            updated_headers.append((b'x-span-id', new_span_id.encode('utf-8')))
        if 'x-parent-span-id' not in header_names_updated and new_parent_span_id:
            updated_headers.append((b'x-parent-span-id', new_parent_span_id.encode('utf-8')))
        
        # request.scope의 headers 업데이트
        request.scope['headers'] = updated_headers

        return await call_next(request)