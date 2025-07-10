import aiohttp

class AsyncHTTPClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _get(self, url, headers=None, **kwargs):
        return await self.session.get(url, headers=headers, **kwargs)

    async def _post(self, url, headers=None, **kwargs):
        return await self.session.post(url, headers=headers, **kwargs)