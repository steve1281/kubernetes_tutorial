from python

# Create a working directory
WORKDIR /usr/src/app

ENV DATABASE_LOCATION dbase/

RUN pip3 install flask flask-sqlalchemy

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
