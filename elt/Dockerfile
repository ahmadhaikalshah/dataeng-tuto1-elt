FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client-15 cron && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY start.sh /app/start.sh
COPY elt_script.py /app/elt_script.py
COPY elt_done_signal.py /app/elt_done_signal.py

RUN chmod +x /app/start.sh

EXPOSE 8686

CMD [ "/bin/bash", "/app/start.sh" ]