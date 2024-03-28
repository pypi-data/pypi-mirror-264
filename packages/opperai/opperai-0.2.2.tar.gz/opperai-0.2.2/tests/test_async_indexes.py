import os
import tempfile
from unittest.mock import ANY, MagicMock, call, patch

import pytest
from opperai import AsyncClient
from opperai.types.indexes import DocumentIn


@pytest.mark.asyncio
@patch("opperai._http_clients._async_http_client.do_request")
async def test_async_indexes_retrieve(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {
                "score": 2.3,
                "id": 1,
                "content": "Bonjour",
                "metadata": {"source": "test"},
            }
        ],
    )
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    resp = await client.indexes.retrieve(index_id=1, query="test", k=1)

    assert resp[0].content == "Bonjour"
    assert resp[0].metadata == {"source": "test"}
    mock_do_request.assert_called_once()


@pytest.mark.asyncio
@patch("opperai._http_clients._async_http_client.do_request")
async def test_async_indexes_create(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: {"id": 123},
    )
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    index_id = await client.indexes.create(name="test_index")

    assert index_id == 123
    mock_do_request.assert_called_once_with(
        "POST",
        "/v1/indexes",
        json={"name": "test_index"},
    )


@pytest.mark.asyncio
@patch("opperai._http_clients._async_http_client.do_request")
async def test_async_indexes_index(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "id": 1,
            "uuid": "506768ec-54ac-4233-8a7b-ea9d1f12b879",
            "key": "test_key",
        },
    )
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    doc_in = DocumentIn(content="Hello", metadata={"source": "test"})
    doc_out = await client.indexes.index(index_id=42, doc=doc_in)

    assert doc_out.id == 1
    assert str(doc_out.uuid) == "506768ec-54ac-4233-8a7b-ea9d1f12b879"
    assert doc_out.key == "test_key"
    mock_do_request.assert_called_once_with(
        "POST",
        "/v1/indexes/42/index",
        json=doc_in.model_dump(),
    )


@pytest.mark.asyncio
@patch("opperai._http_clients._async_http_client.do_request")
async def test_async_indexes_list(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {"id": 1, "name": "test_index_1", "created_at": "2021-07-21T17:32:28Z"},
            {"id": 2, "name": "test_index_2", "created_at": "2021-07-22T17:32:28Z"},
        ],
    )
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    indexes = await client.indexes.list()

    assert len(indexes) == 2
    assert indexes[0].id == 1
    assert indexes[0].name == "test_index_1"
    assert indexes[1].id == 2
    assert indexes[1].name == "test_index_2"
    mock_do_request.assert_called_once_with(
        "GET",
        "/v1/indexes",
    )


@pytest.mark.asyncio
@patch("opperai._http_clients._async_http_client.do_request")
async def test_async_indexes_upload_file(mock_do_request):
    mock_do_request.side_effect = [
        MagicMock(
            status_code=200,
            json=lambda: {
                "url": "http://localhost:8000/upload",
                "fields": {"key": "value"},
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
            },
        ),
        MagicMock(status_code=204),
        MagicMock(
            status_code=200,
            json=lambda: {"uuid": "123e4567-e89b-12d3-a456-426614174000"},
        ),
    ]
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("Some test content")
        tmp_file_path = tmp_file.name
    response = await client.indexes.upload_file(index_id=1, file_path=tmp_file_path)
    os.remove(tmp_file_path)  # Clean up the temporary file after use

    assert response == {"uuid": "123e4567-e89b-12d3-a456-426614174000"}
    mock_do_request.assert_has_calls(
        [
            call("GET", "/v1/indexes/1/upload_url", params={"filename": ANY}),
            call(
                "POST",
                "http://localhost:8000/upload",
                files=ANY,
                data={"key": "value"},
            ),
            call(
                "POST",
                "/v1/indexes/1/register_file",
                json={"uuid": "123e4567-e89b-12d3-a456-426614174000"},
            ),
        ]
    )
