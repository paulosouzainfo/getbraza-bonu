import httpx
from typing import Any, Dict, Optional

class GetBrazaAsyncClient:
    BASE_URL = "https://sandbox-api.getbraza.uk/v2/business"

    def __init__(self, application_id: str, api_key: str, account_number: str):
        self.headers = {
            "x-application-id": application_id,
            "x-api-key": api_key,
            "x-account-number": account_number,
        }
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, headers=self.headers)

    async def close(self):
        await self.client.aclose()

    async def auth(self) -> Dict[str, Any]:
        response = await self.client.post("/v1/auth")
        response.raise_for_status()
        return response.json()

    async def get_balance(self) -> Dict[str, Any]:
        response = await self.client.get("/v1/balance")
        response.raise_for_status()
        return response.json()

    async def get_quote(self, pair: str, markup_type: Optional[str] = None, markup_value: Optional[float] = None) -> Dict[str, Any]:
        params = {"pair": pair}
        if markup_type:
            params["markup_type"] = markup_type
        if markup_value:
            params["markup_value"] = markup_value
        response = await self.client.get("/v1/quote", params=params)
        response.raise_for_status()
        return response.json()

    async def input_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post("/v1/", json=transaction_data)
        response.raise_for_status()
        return response.json()

    async def retrieve_transactions(self) -> Dict[str, Any]:
        response = await self.client.post("/v1/transactions")
        response.raise_for_status()
        return response.json()

    async def withdraw(self, withdraw_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post("/v1/withdraw", json=withdraw_data)
        response.raise_for_status()
        return response.json()

    async def internal_transfer(self, transfer_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post("/v1/internal-transfer", json=transfer_data)
        response.raise_for_status()
        return response.json()