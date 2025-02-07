FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml /app
COPY uv.lock /app
COPY . /app/

RUN uv sync --no-dev --compile-bytecode 

EXPOSE 8881

# CMD ["uv", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8881"] 