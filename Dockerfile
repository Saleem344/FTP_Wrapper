FROM python:3

WORKDIR /app/ftp
RUN mkdir /app/ftp/ftp_push
RUN mkdir /app/ftp/ftp_pushed
RUN mkdir /app/ftp/logs

COPY requirements.txt ./
RUN apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
