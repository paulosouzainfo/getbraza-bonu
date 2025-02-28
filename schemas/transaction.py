from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Transaction(BaseModel):
    created_at: datetime | str
    updated_at: datetime | str
    installation_id: str
    transaction_id: str
    status: str
    amount: float
    amount_to_transfer: float
    fee: float
    coin_name: str
    network_fee: Optional[float] = None
    tx_hash: Optional[str] = None
    reason: Optional[str] = None
    wallet: Optional[str] = None
    fireblocks_id: Optional[str] = None
    block_hash: Optional[str] = None
    blockchain: Optional[str] = None
