
# How to get this running.

From a fresh clone you will need to setup your virtual env and initialize the database.

## setup virtualenv
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

## initialize the database
manually:
```
python3
>>> from app import db
>>> db.create_all()
>>> exit()
```
note: the code has been modified to do this for you now.

## and run
```
There are a number of environment settings you could use. 
You don't have to.

python3 app.py
```

## check work
```
Just open http://localhost:5000
```

## dockerized
```
  (assuming you you haven't changed the ENV values in the Dockerfile)
  docker build -t steve1281/flask-demo .
  docker run -p 5000:80 steve1281/flask-demo
```

## kubernete deployment
```
push the docker image up to docker hub

  docker login
  docker push steve1281/flask-demo

Create a deployment.yml 
Start minikube
  minikube start
Build it
  kubectl create -f deployment.yml
Get the ip
  minikube ip
Or:
  minikube service taskservice --url
  http://172.17.0.2:30001

And Open it up in a web browser

If desired, you can remove the service/deployment with:

$ kubectl delete -f deployment.yml
service "taskservice" deleted
deployment.apps "taskdeployment" deleted

Finally, stop kubernetes:
  minikube stop

```

## kubernetes persistant volume
```
link: https://www.youtube.com/watch?v=E8uGIeiaaUQ

Added to deal with multiple database problem. Basically a single location for the database is required.

Keep in mind, when you do stop kubernetes, the data doesn't persist.  Which means, although the services/deployments 
will restart, the data that was saved in the pods is GONE. This INCLUDES the persistent volume. 

When you scale, the containers are new, and any data on the containers is new. 
To get around this, we added a persistent volume to the deployment.yml. 
This will add a shared database location, /dbase/test.db, that all our pods in taskservice will use.

We also modified the python to check for an environment variable, DATABASE_LOCATION, to tell it where to look,
and modified the Dockerfile to set this to /dbase/test.db

with the volume, you can now increase the replica count. Of course only one can write at a time, and we set that in the
deployment.yml file.

```

## environment variables
```
DATABASE_LOCATION - folder to put test.db database. eg) dbase/
FLASK_PORT_NUMBER - port for server. eg 5000
FLASK_HOST_IP_ADDRESS - ip address for the server. eg) 0.0.0.0
FLASK_DEBUG_MODE - debug mode. eg) True

These are used in the docker file:

steve@kube:~/projects/kuber-demos/flask-demo$ docker exec -it f244e8ac637f /bin/bash
root@f244e8ac637f:/usr/src/app# env | grep FLASK
FLASK_DEBUG_MODE=False
FLASK_HOST_IP_ADDRESS=0.0.0.0
FLASK_PORT_NUMBER=80
```

