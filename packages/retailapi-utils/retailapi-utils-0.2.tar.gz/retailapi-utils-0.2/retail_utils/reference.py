import constants
from request import RetailRequestClient

async def get_delivery_types(crm_url:str,api_key:str):
    client = RetailRequestClient(retail_api_key=api_key,retail_url=crm_url)
    response = await client.send_request(endpoint=f'{crm_url}{constants.reference_url}/delivery-types', method='GET')
    return response


async def get_order_types(crm_url:str,api_key:str):
    client = RetailRequestClient(retail_api_key=api_key,retail_url=crm_url)
    response = await client.send_request(endpoint=f'{crm_url}{constants.reference_url}/order-types', method='GET')
    return response