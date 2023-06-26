FROM ubuntu:latest
LABEL authors="brandbold"

ENTRYPOINT ["top", "-b"]

FROM python:latest

WORKDIR ./api /api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
