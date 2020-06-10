
# How to get this running.

From a fresh clone you will need to setup your virtual env and initialize the database.

## setup virtualenv
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt 
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
PRODUCTION_MODE - launches the app using  waitress instead of flask dev 

These are used in the docker file:

steve@kube:~/projects/kuber-demos/flask-demo$ docker exec -it f244e8ac637f /bin/bash
root@f244e8ac637f:/usr/src/app# env | grep FLASK
FLASK_DEBUG_MODE=False
FLASK_HOST_IP_ADDRESS=0.0.0.0
FLASK_PORT_NUMBER=80
```

## configmap instead of  environment variables

```
from the demo link: https://www.youtube.com/watch?v=SJU8l3UmKZU

Use the command to refresh as needed:
$ kubectl apply -f deployment.yml

we appended to our existing deployment.yml file
a configuration:

apiVersion: v1
kind: ConfigMap
metadata:
  name: configvariable
  namespace: default
data:
  FLASK_DEBUG_MODE : "True"
  FLASK_HOST_IP_ADDRESS : "0.0.0.0"
  FLASK_PORT_NUMBER : "80"

First note, the FLASK_DEBUG_MODE is different than what was in the Dockerfile.
(so if this works as intended, we should see the ENV variable change)


We also added the env assignment:

          env:
            - name: FLASK_DEBUG_MODE
              valueFrom:
                configMapKeyRef:
                  name: configvariable
                  key: FLASK_DEBUG_MODE
            - name: FLASK_HOST_IP_ADDRESS
              valueFrom:
                configMapKeyRef:
                  name: configvariable
                  key: FLASK_HOST_IP_ADDRESS
            - name: FLASK_PORT_NUMBER
              valueFrom:
                configMapKeyRef:
                  name: configvariable
                  key: FLASK_PORT_NUMBER
      volumes:

Second note, the name to put in the ENV is name: . It takes the value from the
ConfigMap.

Checking if this worked:

root@taskdeployment-7d95f5bc99-f2p7x:/usr/src/app# env | grep FLASK
FLASK_DEBUG_MODE=True
FLASK_HOST_IP_ADDRESS=0.0.0.0
FLASK_PORT_NUMBER=80
root@taskdeployment-7d95f5bc99-f2p7x:/usr/src/app# 

So thats good.

Next, lets mount the config as a volume - which I think is more useful.

add a mount point:

          volumeMounts:
            - name: dbase-storage
              mountPath: /usr/src/app/dbase
            - name: config-values
              mountPath: /usr/src/app/config

and hook in our configMap:
      volumes:
        - name: dbase-storage
          persistentVolumeClaim:
            claimName: dbase-pv-storage
        - name: config-values
          configMap:
            name: configvariable

and verify:

root@taskdeployment-76cd486744-9kkxd:/usr/src/app# ls -la config
total 12
drwxrwxrwx 3 root root 4096 Jun 10 02:38 .
drwxr-xr-x 1 root root 4096 Jun 10 02:39 ..
drwxr-xr-x 2 root root 4096 Jun 10 02:38 ..2020_06_10_02_38_58.858240929
lrwxrwxrwx 1 root root   31 Jun 10 02:38 ..data -> ..2020_06_10_02_38_58.858240929
lrwxrwxrwx 1 root root   23 Jun 10 02:38 FLASK_DEBUG_MODE -> ..data/FLASK_DEBUG_MODE
lrwxrwxrwx 1 root root   28 Jun 10 02:38 FLASK_HOST_IP_ADDRESS -> ..data/FLASK_HOST_IP_ADDRESS
lrwxrwxrwx 1 root root   24 Jun 10 02:38 FLASK_PORT_NUMBER -> ..data/FLASK_PORT_NUMBER

root@taskdeployment-76cd486744-9kkxd:/usr/src/app# cat config/FLASK_HOST_IP_ADDRESS 
0.0.0.0


```
