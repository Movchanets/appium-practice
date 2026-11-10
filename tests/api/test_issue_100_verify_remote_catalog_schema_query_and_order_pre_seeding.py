"""Test TC-100: Verify Remote Catalog Schema Query and Order Pre-seeding."""

from __future__ import annotations

import allure
import pytest

from src.api.client import MockStoreApiClient
from src.api.models import OrderRequest, OrderResponse, ProductPayload


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.catalog
@allure.feature("Backend API Integration")
@allure.story("Catalog & Order Pre-seeding")
@allure.title("TC-100: Verify Remote Catalog Schema Query and Order Pre-seeding")
@allure.issue("100")
def test_issue_100_verify_remote_catalog_schema_query_and_order_pre_seeding() -> None:
    """
    Preconditions:
        Store backend API is accessible.
    Steps:
        1. Query the remote product catalog endpoint.
        2. Verify available catalog products.
        3. Send an order creation request with specified product IDs to pre-seed test data.
    Expected Result:
        API returns catalog products with valid prices, and the pre-seeded order is created
        with a confirmed status and calculated total.
    """
    with allure.step("Precondition: Initialize API client"):
        api_client = MockStoreApiClient()

    with allure.step("Step 1: Query the remote product catalog endpoint"):
        products = api_client.fetch_catalog()

    with allure.step("Step 2: Verify available catalog products"):
        assert len(products) > 0, "Remote catalog returned empty list"
        assert all(isinstance(p, ProductPayload) for p in products), (
            "Not all items match ProductPayload schema"
        )
        assert all(p.price > 0.0 for p in products), "All products must have positive prices"
        assert all(p.currency == "USD" for p in products), "Expected all products in USD currency"
        product_map = {p.id: p for p in products}
        assert 1 in product_map and 2 in product_map, "Expected product IDs 1 and 2 in catalog"

    with allure.step("Step 3: Send order creation request with specified product IDs"):
        selected_ids = [1, 2]
        order_request = OrderRequest(
            user_id="usr_tactical_100",
            product_ids=selected_ids,
            delivery_note="Pre-seeded order for verification",
        )
        order_response = api_client.create_preconditioned_order(order_request)

    with allure.step("Verify pre-seeded order response confirms status and calculates total"):
        assert isinstance(order_response, OrderResponse), (
            f"Expected OrderResponse instance, got {type(order_response)}"
        )
        assert order_response.order_id.startswith("ORD-"), (
            f"Expected order_id starting with 'ORD-', got '{order_response.order_id}'"
        )
        assert order_response.user_id == "usr_tactical_100", (
            f"Expected user_id 'usr_tactical_100', got '{order_response.user_id}'"
        )
        assert order_response.status == "confirmed", (
            f"Expected status 'confirmed', got '{order_response.status}'"
        )
        assert order_response.product_ids == selected_ids, (
            f"Expected product_ids {selected_ids}, got {order_response.product_ids}"
        )
        expected_total = round(product_map[1].price + product_map[2].price, 2)
        assert order_response.total_amount == expected_total, (
            f"Expected total_amount {expected_total}, got {order_response.total_amount}"
        )
