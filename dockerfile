FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -u manage.py collectstatic --noinput --clear 

COPY run.sh /run.sh
RUN chmod +x /run.sh


RUN useradd limitado -s /bin/bash
USER limitado

EXPOSE 8000

ENTRYPOINT ["/run.sh"]
