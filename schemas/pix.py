from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Pix(BaseModel):
    created_at: datetime
    updated_at: datetime
    installation_id: str
    status: str
    payer_masked_doc: Optional[str] = None
    end_to_end_id: Optional[str] = None
    payment_id: Optional[str | int] = None
    amount: float
    original_amount: float
    brl_value: float
    original_brl_value: float
    quotation: Optional[float]
    markup_value: float
    markup_type: str
    affiliate_code: Optional[str] = None
    wallet: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    additionalInfo: Optional[str] = None
