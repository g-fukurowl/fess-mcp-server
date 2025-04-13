# Fess MCP Server

Fess MCP Server は、 Fess 検索エンジンと連携するためのミドルウェアサーバーです。
Claude for Desktop などの MCP クライアントの設定に登録することで、エージェントに Fess を用いて情報を得る能力を与えます。Fess は Apache ライセンスで提供されるオープンソースの全文検索サーバーです。商用サポートも提供されています。詳細は公式Webサイトを参照してください。
https://fess.codelibs.org/ja/


# セットアップ

## Fess のセットアップ
Fess サーバ自体のセットアップ手順については Fess の公式ドキュメントを参照してください。
https://qiita.com/g_fukurowl/items/a00dbbad737d3e775108

また、下記の記事も参考になるかもしれません。
https://qiita.com/g_fukurowl/items/a00dbbad737d3e775108

## Fess MCP Server のセットアップ
### Docker を利用する場合
下記コマンドで起動します。

```bash
docker-compose up -d
```

### Docker を利用しない場合
ここではuvを使う場合のセットアップ手順を示します。
uvは高速なPythonパッケージマネージャーです。必須ではありませんが利用をおすすめします。

```powershell
# uvをインストールする
irm https://astral.sh/uv/install.ps1 | iex
```

```powershell
# 仮想環境を有効化する
.\.venv\Scripts\activate.bat
```

```powershell
# 依存ライブラリをインストールする
uv pip install -e .
```

```powershell
# MCPサーバを起動する
uv run .\fess_mcp_server.py
```

## 設定
### Fess サーバとの接続設定
Fess MCP Server がアクセスする Fess サーバの URL は環境変数 Fess_API_BASE として設定されています。
Fess MCP Server を起動する前にご使用の環境に合わせてこの変数を書き換えてください。
Docker コンテナとして起動する場合は docker-compose.yaml を編集し、当該の設定を変更してください。

### Claude for Desktop との接続設定
Fess MCP Server はデフォルトでポート8000で起動します。
Fess MCP Server がローカルホスト上でポート8000で動作している場合は、下記のよう claude_desktop_config.json を編集してください。
```json
{
  "mcpServers": {
    "fess-search-sse": {
        "command": "npx",
        "args": [
          "-y",
          "mcp-remote",
          "http://localhost:8000/sse"
        ]
      }
  }
}
```

## テスト

### Docker を利用しない場合
ここではuvを使う場合のセットアップ手順を示します。

```powershell
# 開発用依存関係のインストール:
uv pip install -e ".[test]"
```

```powershell
# ユニットテストの実行:
uv run pytest -v tests/unit/ -s
```

```powershell
# 統合テストの実行 (Fessサーバと正常に通信可能である必要があります):
uv run pytest -v tests/integration/ -s
```

```powershell
# カバレッジレポートの生成:
uv run pytest --cov=fess_mcp_server --cov-report=html
```

### Dockerコンテナでのテスト実行

```powershell
# テスト用のDockerイメージをビルド:
docker build -t fess-mcp-server-test -f Dockerfile.test .
```

```powershell
# ユニットテストの実行:
docker run --rm fess-mcp-server-test pytest -v tests/unit/ -s
```

```powershell
# 統合テストの実行 (Fessサーバと正常に通信可能である必要があります):
docker run --rm --network host fess-mcp-server-test pytest -v tests/integration/ -s
```

```powershell
# カバレッジレポートの生成:
docker run --rm -v ${PWD}/coverage:/app/coverage fess-mcp-server-test pytest --cov=fess_mcp_server --cov-report=html
```


### テストの実行オプション

- `-v`: 詳細な出力を表示
- `-s`: 標準出力を表示
- `--cov`: カバレッジレポートを生成
- `--cov-report=html`: HTML形式のカバレッジレポートを生成



## ライセンス

MIT License
