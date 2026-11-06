"""API integration tests demonstrating pre-seeding state for Mobile UI flows."""

import pytest

from src.api.client import MockStoreApiClient
from src.api.models import OrderRequest, UserCredentials, UserSessionResponse


@pytest.mark.api
class TestApiDataPreseeding:
    """Verifies backend API readiness and test data generation."""

    @pytest.fixture
    def api_client(self) -> MockStoreApiClient:
        return MockStoreApiClient()

    def test_user_authentication_contract(self, api_client: MockStoreApiClient) -> None:
        """Verify API authentication response matches Pydantic schema."""
        creds = UserCredentials(username="standard_user", password="valid_password_123")
        session = api_client.authenticate_user(creds)

        assert isinstance(session, UserSessionResponse)
        assert session.user_id.startswith("usr_")
        assert len(session.token) > 10
        assert session.active_profile == "standard_user"

    def test_catalog_retrieval(self, api_client: MockStoreApiClient) -> None:
        """Verify remote catalog items can be queried before UI verification."""
        items = api_client.fetch_catalog()

        assert len(items) >= 4
        assert all(item.price > 0 for item in items)
        first_item = items[0]
        assert first_item.name == "Sauce Labs Backpack"

    def test_order_preconditioning_for_mobile_history(self, api_client: MockStoreApiClient) -> None:
        """Verify pre-seeding orders to test Mobile Order History screen."""
        order_req = OrderRequest(
            user_id="usr_tactical_01",
            product_ids=[1, 2],
            delivery_note="Leave at checkpoint A",
        )
        response = api_client.create_preconditioned_order(order_req)

        assert response.order_id.startswith("ORD-")
        assert response.user_id == "usr_tactical_01"
        assert response.status == "confirmed"
        assert response.total_amount == 39.98  # 29.99 + 9.99
