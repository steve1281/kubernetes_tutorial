from python

# Create a working directory
WORKDIR /usr/src/app

# setup environment variables
ENV FLASK_DEBUG_MODE False
ENV DATABASE_LOCATION dbase/
ENV FLASK_PORT_NUMBER 80
ENV FLASK_HOST_IP_ADDRESS 0.0.0.0

# load the needed libraries
RUN pip3 install flask flask-sqlalchemy

# copy the code over - could prune this a lot.
COPY . .

EXPOSE 80

# launch the app at docker run
CMD ["python3", "app.py"]
