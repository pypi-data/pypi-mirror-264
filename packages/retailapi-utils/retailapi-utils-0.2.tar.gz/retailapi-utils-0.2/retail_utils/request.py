import httpx


class RetailRequestClient:

    def __init__(self, retail_url: str, retail_api_key: str):
        self.retail_url = retail_url.rstrip("/")
        self.retail_api_key = retail_api_key

    async def send_request(self, endpoint: str, method: str, params=None, data=None):
        async with httpx.AsyncClient() as client:
            match method:
                case 'GET':
                    response = await client.get(url=endpoint, params=params, data=data)
                case 'POST':
                    response = await client.post(url=endpoint, params=params, data=data)
                case 'PATCH':
                    response = await client.patch(url=endpoint, params=params, data=data)
            return response
