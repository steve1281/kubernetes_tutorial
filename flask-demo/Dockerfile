from python

# Create a working directory
WORKDIR /usr/src/app

# setup environment variables
ENV FLASK_DEBUG_MODE False
ENV DATABASE_LOCATION dbase/
ENV FLASK_PORT_NUMBER 80
ENV FLASK_HOST_IP_ADDRESS 0.0.0.0
ENV PRODUCTION_MODE True

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["python3", "app.py"]
