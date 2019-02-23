FROM python:3.6-alpine

RUN adduser -D aquisitor

WORKDIR /home/aquisitor

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY aquisitor.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP aquisitor.py

RUN chown -R aquisitor:aquisitor ./
USER aquisitor

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
