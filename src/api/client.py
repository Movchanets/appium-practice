"""HTTP API Client demonstrating integration testing & test data pre-seeding."""

import uuid

import requests

from src.api.models import (
    OrderRequest,
    OrderResponse,
    ProductPayload,
    UserCredentials,
    UserSessionResponse,
)


class MockStoreApiClient:
    """API client demonstrating pre-conditioning mobile tests with backend API state.

    In production ATQC workflows, creating pre-conditions (e.g. users, loaded carts,
    active subscriptions) via fast API calls before running slow Mobile UI tests
    reduces test execution time by up to 80%.
    """

    def __init__(self, base_url: str = "https://reqres.in/api") -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mobile-ATQC-TestHarness/1.0",
            }
        )

    def authenticate_user(self, credentials: UserCredentials) -> UserSessionResponse:
        """Authenticate user and return typed session details."""
        # Simulated fast API auth contract
        return UserSessionResponse(
            user_id=f"usr_{uuid.uuid4().hex[:8]}",
            token=f"jwt_{uuid.uuid4().hex}",
            active_profile=credentials.username,
        )

    def fetch_catalog(self) -> list[ProductPayload]:
        """Fetch remote product catalog items."""
        return [
            ProductPayload(id=1, name="Sauce Labs Backpack", price=29.99),
            ProductPayload(id=2, name="Sauce Labs Bike Light", price=9.99),
            ProductPayload(id=3, name="Sauce Labs Bolt T-Shirt", price=15.99),
            ProductPayload(id=4, name="Sauce Labs Fleece Jacket", price=49.99),
        ]

    def create_preconditioned_order(self, order: OrderRequest) -> OrderResponse:
        """Pre-seed an order before verifying mobile order history screen."""
        catalog = {p.id: p.price for p in self.fetch_catalog()}
        total = sum(catalog.get(pid, 20.0) for pid in order.product_ids)
        return OrderResponse(
            order_id=f"ORD-{uuid.uuid4().hex[:6].upper()}",
            user_id=order.user_id,
            product_ids=order.product_ids,
            total_amount=round(total, 2),
            status="confirmed",
        )
