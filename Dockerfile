FROM python:3.11

WORKDIR /app

COPY requirements-prod.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements-prod.txt

COPY . .

RUN python ml/scripts/download_models.py

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]