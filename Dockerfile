FROM python:3.9-slim
WORKDIR /app
COPY . .

EXPOSE 80

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

