FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["sh", "-c", "export FLASK_SECRET_KEY=\"${FLASK_SECRET_KEY:-$(python -c 'import secrets; print(secrets.token_urlsafe(48))')}\"; exec gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile - --error-logfile - app:app"]
