import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fess_mcp_server import check_fess_connection, make_search_request, get_fess_search_results
from tests.unit.test_utils import create_mock_fess_response, create_mock_fess_error_response

@pytest.mark.asyncio
async def test_check_fess_connection_success():
    """FESSサーバーへの接続テスト（成功ケース）"""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(status_code=200)
        result = await check_fess_connection()
        print(f"\ncheck_fess_connection_success result: {result}")
        assert result is True

@pytest.mark.asyncio
async def test_check_fess_connection_failure():
    """FESSサーバーへの接続テスト（失敗ケース）"""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = Exception("Connection failed")
        result = await check_fess_connection()
        print(f"\ncheck_fess_connection_failure result: {result}")
        assert result is False

@pytest.mark.asyncio
async def test_make_search_request_success():
    """検索リクエストテスト（成功ケース）"""
    mock_response = create_mock_fess_response(2)
    mock_response_obj = AsyncMock()
    mock_response_obj.status_code = 200
    mock_response_obj.json = AsyncMock(return_value=mock_response)
    mock_response_obj.raise_for_status = AsyncMock(return_value=None)
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get.return_value = mock_response_obj
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await make_search_request("test query")
        # モックのコルーチンを待機
        await mock_response_obj.raise_for_status()
        await mock_response_obj.json()
        print(f"\nmock_response: {mock_response}")
        print(f"\ntest_make_search_request_success result: {result}")
        # コルーチンを待機してから比較
        if hasattr(result, '__await__'):
            result = await result
        assert result == mock_response

@pytest.mark.asyncio
async def test_make_search_request_error():
    """検索リクエストテスト（エラーケース）"""
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get.side_effect = Exception("Request failed")
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await make_search_request("test query")
        print(f"\ntest_make_search_request_error result: {result}")
        assert result is None

@pytest.mark.asyncio
async def test_get_fess_search_results_success():
    """検索結果取得テスト（成功ケース）"""
    mock_response = create_mock_fess_response(2)
    with patch("fess_mcp_server.make_search_request") as mock_request:
        mock_request.return_value = mock_response
        result = await get_fess_search_results("test query")
        print(f"\ntest_get_fess_search_results_success result: {result}")
        assert "テストコンテンツ" in result
        assert "【参考文献】" in result

@pytest.mark.asyncio
async def test_get_fess_search_results_no_results():
    """検索結果取得テスト（結果なしケース）"""
    with patch("fess_mcp_server.make_search_request") as mock_request:
        mock_request.return_value = None
        result = await get_fess_search_results("test query")
        print(f"\ntest_get_fess_search_results_no_results result: {result}")
        assert result == "検索結果が見つかりませんでした。"

@pytest.mark.asyncio
async def test_get_fess_search_results_invalid_response():
    """検索結果取得テスト（無効なレスポンスケース）"""
    with patch("fess_mcp_server.make_search_request") as mock_request:
        mock_request.return_value = {"invalid": "response"}
        result = await get_fess_search_results("test query")
        print(f"\ntest_get_fess_search_results_invalid_response result: {result}")
        assert result == "検索結果が見つかりませんでした。" 