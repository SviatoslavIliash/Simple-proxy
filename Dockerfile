FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x /app/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]