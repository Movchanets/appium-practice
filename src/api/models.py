"""Pydantic data models for API integration and test data preparation."""

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class UserCredentials(BaseModel):
    """Payload representing login credentials."""

    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., min_length=3, max_length=50, description="User identifier")
    password: str = Field(..., min_length=6, description="User password")


class UserSessionResponse(BaseModel):
    """Response model returned after authentication."""

    user_id: str
    token: str
    token_type: str = "Bearer"
    expires_in_seconds: int = 3600
    active_profile: str = "standard_user"


class ProductPayload(BaseModel):
    """Payload representing catalog items."""

    id: int
    name: str
    price: float = Field(..., gt=0.0)
    currency: str = "USD"
    in_stock: bool = True


class OrderRequest(BaseModel):
    """Payload for placing an order/seeding checkout cart."""

    user_id: str
    product_ids: list[int] = Field(..., min_length=1)
    delivery_note: str | None = None


class OrderResponse(BaseModel):
    """Order confirmation response."""

    order_id: str
    user_id: str
    product_ids: list[int]
    total_amount: float
    status: str = "confirmed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
