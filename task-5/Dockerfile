FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080 DB_PATH=/data/notes.db
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN useradd --create-home --uid 10001 appuser && mkdir /data && chown appuser /data
USER appuser
VOLUME /data
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request,os;urllib.request.urlopen('http://127.0.0.1:'+os.environ['PORT']+'/health')" || exit 1
CMD ["sh", "-c", "exec gunicorn -b 0.0.0.0:${PORT} --workers 2 --access-logfile - app.main:app"]
