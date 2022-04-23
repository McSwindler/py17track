"""Define tests for the client object."""
import aiohttp
import pytest

from seventeentrack import Client
from seventeentrack.errors import RequestError


@pytest.mark.asyncio
async def test_bad_request(aresponses):
    """Test that a failed login returns the correct response."""
    aresponses.add(
        "random.domain", "/no/good", "get", aresponses.Response(text="", status=404)
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client._request("get", "https://random.domain/no/good")


@pytest.mark.asyncio
async def test_no_explicit_session(aresponses):
    """Test not providing an explicit aiohttp ClientSession."""
    aresponses.add(
        "random.domain",
        "/good",
        "get",
        aresponses.Response(text='{"good":true}', status=200),
    )

    client = Client()
    response = await client._request("get", "https://random.domain/good")
    assert response["good"] is True
