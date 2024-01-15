FROM python:3.9-slim
WORKDIR /app
COPY . .

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]