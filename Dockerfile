FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-root

COPY resonance_os /app/resonance_os
COPY .env /app/.env

EXPOSE 8000

CMD ["uvicorn", "resonance_os.api.hr_server:app", "--host", "0.0.0.0", "--port", "8000"]
