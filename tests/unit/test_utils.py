import json
from typing import Any, Dict

def create_mock_fess_response(num_results: int = 1) -> Dict[str, Any]:
    """FESS APIのモックレスポンスを作成します"""
    results = []
    for i in range(num_results):
        result = {
            "content_description": f"テストコンテンツ {i+1}",
            "title": f"テストタイトル {i+1}",
            "url_link": f"http://example.com/doc{i+1}",
            "last_modified": "2024-01-01T00:00:00Z"
        }
        results.append(result)
    
    return {
        "data": results
    }

def create_mock_fess_error_response() -> Dict[str, Any]:
    """FESS APIのエラーレスポンスを作成します"""
    return {
        "error": {
            "message": "Internal Server Error",
            "code": 500
        }
    } 