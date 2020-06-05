
# How to get this running.

From a fresh clone you will need to setup your virtual env and initialize the database.

## setup virtualenv
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

## initialize the database
```
python3
>>> from app import db
>>> db.create_all()
>>> exit()
```

## and run
```
modify the port in the app.py to something other than 80 (todo: ENV this)
python3 app.py
```

## check work
```
Just open http://localhost:5000
```

## dockerized
```
first, set the port in app.py to be 80. (avoids firewall issues)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

then:
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


CAVEAT!  As designed, each flask-demo has its OWN database, and we are loadbalancing.
This means you will get a different pod each time, which means reading and writing is going 
to not work correctly. We need a database service, or someway of syncing between many.

For now, set the replicas: 1

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

We need a single location for the database.

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


