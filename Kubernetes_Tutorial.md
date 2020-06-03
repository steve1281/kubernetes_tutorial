# Following a online tutorial/demo
link: https://www.youtube.com/watch?v=1xo-0gCVhTU

## microservices vs monolithic
```
monolithic is a traditional three teir: UI -- business logic --- data
  one UI
  simple architecture

microservices:
  one UI
  many services, with well defined REST API
  many languages; using REST API
  many databases; using REST API
  able to scale - often dynamically
  one microservice failure doesn't kill the system
  works well with containers
  complex networking
  overhead - a lot of setup, knowledge (containers, orchestration)
```

## docker
```
What is it?
  container of choice - big and popular 
  eliminates the problem of system configuration/setup
  package software so it can be run anywhere
  its NOT a virtual machine
  they share some of the same ideas
  in a VM you have to package the entire OS and libs and app
  in a docker APP and libs only - docker emulates the OS for you
  docker allows sharing of bins and libs and OS etc - cuts downs in size

You create a Dockerfile - a defination
You build an image from a Dockerfile
You can then "run" that image on any computer with docker on it
Very popular right now.
```

## kubernetes
```
Container Orchestration
there are many of these!, kubernetes is just popular

How you would like to configure you microserver
makes it happen across many computers at once
instead of ssh your computers, do setup, you can just use kubernetes
give it a declarted state - a "deployment" and it will do it for you

Vocabulary
  node - instance of a computer running kube
  pod - runs one or more containers,lives on a nodes
  service - handles requests, usually a load balancer
  deployment - defines a desired state - I want three copies of X, set up as Y

deployment file, typically a yaml file, declares desired state
  could have a kind of : pod, deployment, service, etc
 
```

## DEMO #1 : tutum/hello-world
```
Recall link: https://www.youtube.com/watch?v=1xo-0gCVhTU&t=1485s is 2017; there have been some changes.

Note: steve is a member of sudo and docker. So, I don't sudo everything like he does in the demo.

For reference later, get my ip:
  $ ifconfig | grep enp0s3 -A1
  enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.100.178  netmask 255.255.255.0  broadcast 192.168.100.255

From this point I am working in visual code; I created a folder ~/projects/docker-demo to work from.
  $ mkdir -p ~/projects/kube-demo
  $ cd ~/projects/kube-demo
  $ code .
Inside visual code, open a terminal. I enter all my commands there.

Some docker:

  $ docker run hello-world
  (this will pull and run simplest thing ever.)

  docker run -p 3000:80 tutum/hello-world
  (open in web browser, localhost:3000, for nice web page with info on package running)
  (or from my host system: http://192.168.100.178:3000/ since I bridged a VM and thats the IP it got)

  docker run -d -p 3000:80 tutum/hello-world
  (so launch in detached mode)
  a654b919db9ecd904a9f6455d0e86df1127a9874c1d67876d3b7d69ee4d11439
  (and open the web page and see..My hostname is a654b919db9e ...)
  (and check the docker ps)
  docker ps | grep tutum
  a654b919db9e        tutum/hello-world      "/bin/sh -c 'php-fpm…" ...   0.0.0.0:3000->80/tcp   interesting_panini

  (he goes on to spawn a few, on 3001, 3002)
  steve@kubernetes-master:~/projects/docker-demo$ docker run -d -p 3001:80 tutum/hello-world
  ea8b360b77aeafe6ea26015c4c602f61a20a785553a35bb668a115659c41982d
  
  steve@kubernetes-master:~/projects/docker-demo$ docker run -d -p 3002:80 tutum/hello-world
  4ca19bf468624491eb11e27c760b05f749b27f54c2dff1c262dfa20c16373d42
  
  (and go look at the url, on the different ports, to see them running)
  (and yes, they work.)

  (and kill them:)
  docker kill a654b919db9e ea8b360b77ae 4ca19bf46862
  (and note the web pages no longer work)

Next deploy on kubernetes
  start minikube if its not already running
  $ minikube start
  from the terminal, $ touch deployment.yml
  click on new file deployment.yml (NOTE: had to modify from the demo!)

---
kind: Service
apiVersion: v1
metadata:
  name: helloworldservice
spec:
  selector:
    app: hello-world
  ports:
    - protocol: "TCP"
      # Port accessible inside cluster
      port: 8080
      # Port to forward to inside the pod
      targetPort: 80
      # Port accessible outside cluster
      nodePort: 30001
  type: LoadBalancer


---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 5
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
        - name: hello-world
          image: tutum/hello-world
          ports:
            - containerPort: 80

Then we can create it. (after you create it, you can change it with apply)

$ kubectl create -f deployment.yml
service/helloworldservice created
deployment.apps/hello-world created

And you can see these in your GUI

$ minikube dashboard
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:45459/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...

You'll see 5 hello worlds running :-)

Or, from command line:

$ kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
hello-world-684b8bc4fc-5lppr   1/1     Running   0          6m7s
hello-world-684b8bc4fc-6fh2h   1/1     Running   0          6m7s
hello-world-684b8bc4fc-8g8sc   1/1     Running   0          6m7s
hello-world-684b8bc4fc-926g9   1/1     Running   0          6m7s
hello-world-684b8bc4fc-qwmqv   1/1     Running   0          6m7s

$ kubectl get deployments
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
hello-world   5/5     5            5           7m12s

$ minikube ip
172.17.0.3

So, from within my VM, I can hit: http://172.17.0.3:30001/ and see the tutum hello-world.
And, if I hit it a lot, the hostname will change as the load balancer kicks in.
ie)
$ curl http://172.17.0.3:30001/ | grep hostname
        <h3>My hostname is hello-world-684b8bc4fc-8g8sc</h3>                    <h3>Links found</h3>
$ curl http://172.17.0.3:30001/ | grep hostname
        <h3>My hostname is hello-world-684b8bc4fc-5lppr</h3>                    <h3>Links found</h3>

So, it moves it around - sticky loadbalancing. Nice and stateless and RESTfull :-)

If you crash a one (go to the gui and delete a pod to test) kubernetes will start another.

From the gui, you can go to Deployments and scale. 

And clean up stuff.
   $ kubectl get deployments
   $ kubectl delete service/helloworldservice
   $ kubectl get deployments
   $ kubectl delete deployment/hello-world
   $ kubectl get pods

Worth noting, in "real" kubernetes, this don't work - you need to "drain" the service, with a bunch of flags. 
(Nasty, and out of scope for now.)
```

## DEMO#2 : Custom docker
```
NOTE: this demo uses a public repository for its docks, and for this I will too. 
You will need a personal docker user/password to use this.
link: https://hub.docker.com/

Demo is a little dated; I had to tweak it a bit.

Make a new directory: 
$ mkdir -p ~/projects/kube-demo-2
and launch code: 
$ code .

$ npm init
press return for everything

$ npm i express --save

$ touch index.js

Edit the file:

'use strict';

const express = require('express');

// Constants
const PORT = 8080
const HOST = '0.0.0.0'

//APP
const app = express();
app.get('/', (req, res) => {
    res.send('Hello world\n');
   
})

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);


Next, need to make a container. Create a Dockerfile
$ touch Dockerfile
edit the Dockerfile:

from node:carbon

# Create a working directory
WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "start"]

(carbon... we can probably can and should go more recent that node:carbon, but really it makes no difference for an image this simple)
Next, we will create a .dockerignore for files we dont want copied
$ touch .dockerignore
edit it
docker build -t steve1281/exampleapp:v1.0.0 .
... and wait ...
 ---> a12050b02fe6
Successfully built a12050b02fe6
Successfully tagged steve1281/exampleapp:v1.0.0

$ docker run -p 8080:8080 steve1281/exampleapp:v1.0.0
> kube-demo-2@1.0.0 start /usr/src/app
> node index.js

Running on http://0.0.0.0:8080

In another window, or a browser, on the VM, go ahead an get http://localhost:8080
$ curl localhost:8080
Hello world

So that works.
Push it to docker

$ docker login
username:
password

$ docker push steve1281/exampleapp:v1.0.0

Now we need to run it in kubernetes.
Create a deployment.yml
$ touch deployment.yml
edit it

---
kind: Service
apiVersion: v1
metadata:
  name: exampleservice
spec:
  selector:
    app: myapp
  ports:
    - protocol: "TCP"
      # Port accessible inside cluster
      port: 8081
      # Port to forward to inside the pod
      targetPort: 8080
      # Port accessible outside cluster
      nodePort: 30002
  type: LoadBalancer



---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myappdeployment
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: steve1281/exampleapp:v1.0.0
          ports:
            - containerPort: 8080


And create the service:

$ kubectl create -f deployment.yml 
service/exampleservice created
deployment.apps/myappdeployment created

$ curl http://172.17.0.3:30002/
Hello world

Yay. Done.

```




