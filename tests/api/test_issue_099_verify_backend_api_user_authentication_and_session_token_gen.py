"""Test TC-099: Verify Backend API User Authentication and Session Token Generation."""

from __future__ import annotations

import allure
import pytest

from src.api.client import MockStoreApiClient
from src.api.models import UserCredentials, UserSessionResponse


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.auth
@allure.feature("Backend API Integration")
@allure.story("Authentication")
@allure.title("TC-099: Verify Backend API User Authentication and Session Token Generation")
def test_issue_099_verify_backend_api_user_authentication_and_session_token_gen() -> None:
    """Preconditions:
        Store backend API is accessible.
    Steps:
        1. Send an authentication request with valid user credentials.
        2. Inspect the returned session payload.
    Expected Result:
        The API returns HTTP 200 with a valid session token, user identifier,
        and active profile details.
    """
    with allure.step("Precondition: Initialize API client"):
        api_client = MockStoreApiClient()

    with allure.step("Step 1: Send an authentication request with valid user credentials"):
        credentials = UserCredentials(username="tactical_operator", password="secure_password_123")
        session = api_client.authenticate_user(credentials)

    with allure.step("Step 2: Inspect the returned session payload"):
        assert isinstance(session, UserSessionResponse), (
            f"Expected UserSessionResponse instance, got {type(session)}"
        )
        assert session.user_id.startswith("usr_"), (
            f"Expected user_id prefix 'usr_', got '{session.user_id}'"
        )
        assert len(session.token) > 0, "Session token is empty"
        assert session.token.startswith("jwt_"), (
            f"Expected token prefix 'jwt_', got '{session.token}'"
        )
        assert session.token_type == "Bearer", (
            f"Expected token_type 'Bearer', got '{session.token_type}'"
        )
        assert session.expires_in_seconds > 0, "expires_in_seconds must be positive"
        assert session.active_profile == "tactical_operator", (
            f"Expected active_profile 'tactical_operator', got '{session.active_profile}'"
        )
