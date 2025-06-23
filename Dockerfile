FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8005
CMD ["python", "agratas_mcp_server.py"]
