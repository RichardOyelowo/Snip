import pytest


@pytest.mark.asyncio
async def test_create_link(client):
    response = await client.post("/link/", data={"original_url": "https://example.com"})
    assert response.status_code == 200
    assert "http://test/" in response.text


@pytest.mark.asyncio
async def test_load_link_success(client):
    pass


@pytest.mark.asyncio
async def test_load_link_not_found(client):
    pass


@pytest.mark.asyncio
async def create_duplicate_link(client):
    pass
