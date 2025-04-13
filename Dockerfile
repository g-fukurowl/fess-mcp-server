# ベースイメージとしてPython 3.10を使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# PATHにuvを追加
ENV PATH="/root/.cargo/bin:${PATH}"

# 依存関係をコピー
COPY pyproject.toml .

# 依存関係をインストール（詳細なエラーメッセージを表示）
RUN pip install --verbose -e .

# アプリケーションコードをコピー
COPY . .

# 環境変数を設定
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HOST=0.0.0.0

# ポートを公開
EXPOSE 8000

# fess_mcp_server.pyを実行
CMD ["python", "fess_mcp_server.py"] 