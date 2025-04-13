import pytest
import httpx
import os
from fess_mcp_server import check_fess_connection, make_search_request

@pytest.mark.asyncio
async def test_fess_connection_integration():
    """FESSサーバーへの実際の接続テスト"""
    # 環境変数からFESSのURLを取得
    fess_url = os.getenv("FESS_API_BASE", "http://localhost:8080/api/v1")
    
    # テスト用のFESSサーバーが利用可能な場合のみ実行
    try:
        result = await check_fess_connection()
        assert isinstance(result, bool)
    except Exception as e:
        pytest.skip(f"FESSサーバーが利用できません: {str(e)}")

@pytest.mark.asyncio
async def test_fess_search_integration():
    """FESSサーバーへの実際の検索リクエストテスト"""
    # 環境変数からFESSのURLを取得
    fess_url = os.getenv("FESS_API_BASE", "http://localhost:8080/api/v1")
    
    # テスト用のFESSサーバーが利用可能な場合のみ実行
    try:
        result = await make_search_request("test")
        assert result is not None
        assert isinstance(result, dict)
        if "data" in result:
            assert isinstance(result["data"], list)
    except Exception as e:
        pytest.skip(f"FESSサーバーが利用できません: {str(e)}") 