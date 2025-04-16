from typing import Any
import asyncio
import httpx
import os
import logging
from mcp.server.fastmcp import FastMCP

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("fess-mcp-server")

# Initialize FastMCP server
mcp = FastMCP("fess-mcp")

# Constants
FESS_API_BASE = os.getenv("FESS_API_BASE", "http://host.docker.internal:8080/api/v1")
USER_AGENT = "fess-search-app/1.0"

logger.info(f"FESS API Base URL: {FESS_API_BASE}")

async def check_fess_connection() -> bool:
    """FESSサーバーへの疎通確認を行います"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    health_check_url = f"{FESS_API_BASE}/health"
    logger.info(f"Checking connection to FESS server: {health_check_url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(health_check_url, headers=headers, timeout=5.0)
            if response.status_code == 200:
                logger.info("Successfully connected to FESS server")
                return True
            else:
                logger.error(f"FESS server returned status code: {response.status_code}")
                return False
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to FESS server: {str(e)}")
            return False
        except httpx.TimeoutException:
            logger.error("Connection to FESS server timed out")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while checking FESS connection: {str(e)}")
            return False

async def make_search_request(query: str) -> dict[str, Any] | None:
    """Make a request to the FESS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    url: str = f"{FESS_API_BASE}/documents?q=" + query
    logger.info(f"Making request to FESS API: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            logger.info("Sending request to FESS server...")
            response = await client.get(url, headers=headers, timeout=30.0)
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"FESS API returned error status: {response.status_code}")
                logger.error(f"Response body: {response.text}")
                return None
                
            response.raise_for_status()
            logger.info("Successfully received response from FESS server")
            return response.json()
            
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to FESS server: {str(e)}")
            return None
        except httpx.TimeoutException:
            logger.error("Request to FESS server timed out")
            return None
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            return None

@mcp.tool()
async def get_fess_search_results(query: str) -> str:
    """オープンソース検索エンジンFESSを用いて、webに一般公開されていない情報を検索します。

    Args:
        query: 検索クエリ。調べたい事に関する単語や用語など。複数の検索語がすべて含まれるドキュメントを検索したい場合には AND 検索を利用します。AND を省略してスペース区切りで検索語入力欄に複数単語を記述した場合も AND 検索になります。AND 検索を利用する場合は検索語間に AND を記述します。AND は半角大文字で記述して、前後にスペースが必要になります。AND は省略することも可能です。たとえば、「検索語1」と「検索語2」が含まれるドキュメントを検索したい場合は以下のように検索フォームに入力します。検索語1 AND 検索語2。このようにANDで複数語をつなぐことも可能です。検索語のどれかが含まれるドキュメントを検索したい場合には OR 検索を利用します。検索語入力欄に複数単語を記述した場合、デフォルトでは AND 検索になります。OR 検索を利用する場合は検索語間に OR を記述します。OR は半角大文字で記述して、前後にスペースが必要になります。たとえば、「検索語1」と「検索語2」のどちらかが含まれるドキュメントを検索したい場合は以下のように検索フォームに入力します。検索語1 OR 検索語2。OR で複数語をつなぐことも可能です。ある単語を含まないドキュメントを検索する場合に NOT 検索が利用できます。NOT 検索は含まない単語の前に NOT を付けて検索します。NOT は半角大文字で、前後にスペースが必要です。たとえば、「検索語1」が含まれるが「検索語2」を含まないドキュメントを検索したい場合は以下のように入力して検索します。検索語1 NOT 検索語2。検索語内で 1文字または複数文字のワイルドカードを利用することができます。 ? は 1文字のワイルドカードとして指定でき、*は複数文字のワイルドカードとして指定することができます。 ワイルドカードを利用できる対象は単語になります。 文に対するワイルドカード検索はできません。文字のワイルドカードを利用する場合は次のように ? を利用します。te?t の場合は、textやtestなど、1 文字のワイルドカードとして扱われます。複数文字のワイルドカードを利用する場合は以下のように * を利用します。test* の場合は、test、testsやtesterなど、複数文字のワイルドカードとして扱われます。また、te*t のように検索語内に利用することもできます。ブースト検索を利用するためには、検索語の後に「^ブースト値」という形式でブースト値 (重み付け値) を指定します。たとえば、「りんご みかん」を検索したい場合に「りんご」がより含まれるページを検索したい場合は次のように検索フォームに入力します。りんご^100 みかん。ブースト値は 1 以上の整数を指定します。        
    """
    logger.info(f"Received search query: {query}")
    results = await make_search_request(query)
    
    if not results:
        logger.warning("No results returned from FESS server")
        return "検索結果が見つかりませんでした。"
    
    if "data" not in results:
        logger.warning("No 'data' field in FESS response")
        return "検索結果が見つかりませんでした。"
    
    logger.info(f"Found {len(results['data'])} results")
    
    formatted_results = []
    references = []
    
    for i, result in enumerate(results["data"], 1):
        content = result["content_description"].replace("<strong>", "").replace("</strong>", "")
        digest = result["digest"].replace("<strong>", "").replace("</strong>", "")
        title = result.get("title", "タイトルなし")
        url_link = result.get("url_link", "URLなし").replace("file//","")
        last_modified = result.get("last_modified", "最終更新日不明")
        formatted_results.append(f"[{i}] {content} {digest}")
        references.append(f"[{i}] \"{title}\", {url_link}, {last_modified}")
    
    # 検索結果と参考文献を結合
    output = "\n\n".join(formatted_results)
    output += "\n\n【参考文献】\n" + "\n".join(references)
    return output.encode('utf-8', errors='replace').decode('utf-8')

if __name__ == "__main__":
    logger.info("Starting FESS MCP Server...")
    
    # FESSサーバーへの疎通確認
    connection_ok = asyncio.run(check_fess_connection())
    if not connection_ok:
        logger.error("Failed to connect to FESS server. Server will start but may not function properly.")
    else:
        logger.info("FESS server connection check passed. Server is ready to handle requests.")
    
    # Initialize and run the server
    #mcp.run(transport='stdio')
    mcp.run(transport='sse')
