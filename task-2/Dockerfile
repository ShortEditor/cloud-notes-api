FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PORT=8080 LOG_LEVEL=INFO
EXPOSE 8080
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app.main:app"]
