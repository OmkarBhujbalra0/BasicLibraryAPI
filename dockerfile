FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]