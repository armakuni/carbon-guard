from httpx import Request

from src.repos.carbon_intensity.co2_signal import CO2SignalAuthClient


def test_auth_client_auth_flow() -> None:
    request = Request(method="GET", url="https://example.com")
    auth_req = next(CO2SignalAuthClient(api_key="abc").auth_flow(request))
    assert auth_req.headers["auth-token"] == "abc"
