FROM python:3.12-slim

WORKDIR /ntumakans

RUN useradd -ms /bin/bash web_dev


COPY . .
RUN pip install -r requirements.txt

RUN chmod 444 /ntumakans/company_secrets/secret.txt

USER web_dev
EXPOSE 5000

CMD ["python", "app.py"]
