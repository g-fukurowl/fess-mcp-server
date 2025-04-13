# Fess MCP Server

Fess MCP Serverは、Fess検索エンジンと連携するためのミドルウェアサーバーです。

## 機能

- Fess検索エンジンとの連携
- 検索結果のキャッシュ機能
- Dockerコンテナ化対応

## 必要条件

- Python 3.8以上
- Docker
- Docker Compose
- uv (オプション、推奨)

## セットアップ

### uvのインストール（オプション）

uvは高速なPythonパッケージマネージャーです。インストールを推奨します：

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

### プロジェクトのセットアップ

1. リポジトリをクローン:
```bash
git clone https://github.com/g-fukurowl/fess-mcp-server.git
cd fess-mcp-server
```

2. 依存関係のインストール:
```bash
# pipを使用する場合
pip install -e .

# uvを使用する場合（推奨）
uv pip install -e .
```

3. Dockerを使用して起動:
```bash
docker-compose up -d
```

## Windowsでのローカル実行

1. 仮想環境の作成と有効化:
```powershell
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
.\.venv\Scripts\activate.bat
```

2. 依存関係のインストール:
```powershell
# pipを使用する場合
pip install -e .

# uvを使用する場合（推奨）
uv pip install -e .
```

3. サーバーの起動:
```powershell
python fess_mcp_server.py

# uvを使用する場合（推奨）
uv run .\fess_mcp_server.py
```

4. 環境変数の設定（必要に応じて）:
```powershell
$env:PORT=8000
$env:HOST="0.0.0.0"
$env:FESS_URL="http://localhost:8080"
$env:FESS_USERNAME="admin"
$env:FESS_PASSWORD="admin"
```

## テスト

### ローカル環境でのテスト実行

1. 開発用依存関係のインストール:
```powershell
# pipを使用する場合
pip install -e ".[test]"

# uvを使用する場合（推奨）
uv pip install -e ".[test]"
```

2. ユニットテストの実行:
```powershell
# pipを使用する場合
python -m pytest -v tests/unit/ -s

# uvを使用する場合（推奨）
uv run pytest -v tests/unit/ -s
```

3. 統合テストの実行:
```powershell
# pipを使用する場合
python -m pytest -v tests/integration/ -s

# uvを使用する場合（推奨）
uv run pytest -v tests/integration/ -s
```

4. カバレッジレポートの生成:
```powershell
# pipを使用する場合
python -m pytest --cov=fess_mcp_server --cov-report=html

# uvを使用する場合（推奨）
uv run pytest --cov=fess_mcp_server --cov-report=html
```

### Dockerコンテナでのテスト実行

1. テスト用のDockerイメージをビルド:
```powershell
docker build -t fess-mcp-server-test -f Dockerfile.test .
```

2. ユニットテストの実行:
```powershell
docker run --rm fess-mcp-server-test pytest -v tests/unit/ -s
```

3. 統合テストの実行（FESSサーバーが必要な場合）:
```powershell
docker run --rm --network host fess-mcp-server-test pytest -v tests/integration/ -s
```

4. カバレッジレポートの生成:
```powershell
docker run --rm -v ${PWD}/coverage:/app/coverage fess-mcp-server-test pytest --cov=fess_mcp_server --cov-report=html
```

### テストの構成

- `tests/unit/`: ユニットテスト
  - `test_fess_mcp_server.py`: メインのユニットテスト
    - FESSサーバー接続テスト
    - 検索リクエストテスト
    - 検索結果処理テスト
  - `test_utils.py`: テスト用ユーティリティ

- `tests/integration/`: 統合テスト
  - `test_fess_integration.py`: FESSサーバーとの統合テスト
    - 実際のFESSサーバーとの接続テスト
    - 実際の検索リクエストテスト

### テストの詳細

#### ユニットテスト

ユニットテストは、以下のテストケースを含みます：

1. FESSサーバー接続テスト
   - 成功ケース
   - 失敗ケース

2. 検索リクエストテスト
   - 成功ケース
   - エラーケース

3. 検索結果処理テスト
   - 成功ケース
   - 結果なしケース
   - 無効なレスポンスケース

#### 統合テスト

統合テストは、実際のFESSサーバーとの連携をテストします：

1. FESSサーバー接続テスト
2. 検索リクエストテスト

統合テストを実行するには、FESSサーバーが利用可能である必要があります。

### テストの実行オプション

- `-v`: 詳細な出力を表示
- `-s`: 標準出力を表示
- `--cov`: カバレッジレポートを生成
- `--cov-report=html`: HTML形式のカバレッジレポートを生成

## 使用方法

サーバーはデフォルトでポート8000で起動します。

## ライセンス

MIT License
