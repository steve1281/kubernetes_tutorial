# nginx - lets start up a web server, and allow access to web pages remotely

```
this example will 
1. use helm to deploy a nginx server
2. use dryrun to capture the yaml
3. modify that yaml to allow us to mount path from minikube to nginx
4. execute a kubectl to mount a local path to minikube
5. allow us to modify local files and change the website

```

## setup/cleanup
```
Start the kube, remove any old work.

$ minikube start
😄  minikube v1.11.0 on Ubuntu 20.04
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.18.3 on Docker 19.03.2 ...
    ▪ kubeadm.pod-network-cidr=10.244.0.0/16
🔎  Verifying Kubernetes components...
🌟  Enabled addons: dashboard, default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube"

What was already running?

$ helm list
NAME                 	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART            	APP VERSION
mysql-1592664037     	default  	1       	2020-06-20 10:40:41.234717039 -0400 EDT	deployed	mysql-1.6.4      	5.7.30     
postgresql-1592677916	default  	1       	2020-06-20 14:31:58.424597896 -0400 EDT	deployed	postgresql-8.10.6	11.8.0     

Remove it.

$ helm uninstall mysql-1592664037 postgresql-1592677916
release "mysql-1592664037" uninstalled
release "postgresql-1592677916" uninstalled

Verify its clean (give it a minute or two)

$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   14d

All clean.
```
## Find a repo to hijack/modify
```
$ helm repo update

$ helm search repo nginx
NAME                            	CHART VERSION	APP VERSION	DESCRIPTION                                       
bitnami/nginx                   	6.0.1        	1.19.0     	Chart for the nginx server                        
bitnami/nginx-ingress-controller	5.3.24       	0.33.0     	Chart for the nginx Ingress controller            
stable/nginx-ingress            	1.40.1       	0.32.0     	An nginx Ingress controller that uses ConfigMap...
stable/nginx-ldapauth-proxy     	0.1.4        	1.13.5     	nginx proxy with ldapauth                         
stable/nginx-lego               	0.3.1        	           	Chart for nginx-ingress-controller and kube-lego  
bitnami/kong                    	1.2.2        	2.0.4      	Kong is a scalable, open source API layer (aka ...
stable/gcloud-endpoints         	0.1.2        	1          	DEPRECATED Develop, deploy, protect and monitor...

$ helm install bitnami/nginx --generate-name
NAME: nginx-1592765406
LAST DEPLOYED: Sun Jun 21 14:50:08 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Get the NGINX URL:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc --namespace default -w nginx-1592765406'

  export SERVICE_IP=$(kubectl get svc --namespace default nginx-1592765406 --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
  echo "NGINX URL: http://$SERVICE_IP/"

Or, just run:
$ minikube service nginx-1592765406 --url
http://172.17.0.2:32557
http://172.17.0.2:31462

Test on the http:

$ curl http://172.17.0.2:32557
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

And kill the current deployment:
$ helm list
NAME            	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART      	APP VERSION
nginx-1592765406	default  	1       	2020-06-21 14:50:08.671208146 -0400 EDT	deployed	nginx-6.0.1	1.19.0     

$ helm uninstall nginx-1592765406
release "nginx-1592765406" uninstalled

```

## Use dryrun to get a deployment file
```
But we want to mess this. So lets capture the yaml:
www
$ helm install bitnami/nginx --generate-name --dry-run > deployment.yaml

Edit the dryrun. Remove the block of crud on the top, and the block on the bottom.

Deploy it use kubectl

$ kubectl create -f deployment.yaml 
configmap/nginx-1592766463-server-block created
service/nginx-1592766463 created
deployment.apps/nginx-1592766463 created

Check that it deployed ok:
$ kubectl get all
NAME                                   READY   STATUS    RESTARTS   AGE
pod/nginx-1592766463-f96b4dbcf-twvmm   1/1     Running   0          35s

NAME                       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
service/kubernetes         ClusterIP      10.96.0.1      <none>        443/TCP                      14d
service/nginx-1592766463   LoadBalancer   10.106.74.70   <pending>     80:32246/TCP,443:31514/TCP   35s

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-1592766463   1/1     1            1           35s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-1592766463-f96b4dbcf   1         1         1       35s

Curl check:
$ minikube service nginx-1592766463 --url
http://172.17.0.2:32246
http://172.17.0.2:31514

$ curl http://172.17.0.2:32246
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

Good stuff!

Delete this deployment/service/app:

$ kubectl delete -f deployment.yaml
configmap "nginx-1592766463-server-block" deleted
service "nginx-1592766463" deleted
deployment.apps "nginx-1592766463" deleted

And verify:
$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   14d

Perfect.
```

## Now we can change the deployment
```

Now, lets create a mount inside minikube that the pods should be able to access.
$ mkdir www
$ cd www
$ minikube mount $(pwd):/var/www/html
📁  Mounting host path /home/steve/projects/kuber-demos/nginx-example/www into VM as /var/www/html ...
    ▪ Mount type:   <no value>
    ▪ User ID:      docker
    ▪ Group ID:     docker
    ▪ Version:      9p2000.L
    ▪ Message Size: 262144
    ▪ Permissions:  755 (-rwxr-xr-x)
    ▪ Options:      map[]
    ▪ Bind Address: 172.17.0.1:33079
🚀  Userspace file server: ufs starting
✅  Successfully mounted /home/steve/projects/kuber-demos/nginx-example/www to /var/www/html

📌  NOTE: This process must stay alive for the mount to be accessible ...


Open a new terminal.
in the www folder yur created, build an index.html, for example:

$ ed index.html
index.html: No such file or directory
a
<html>
<head>
<title> Put a title here</title>
</head>
<body>
<h1>Put some body here</h1>
</body>
</html>
.
w
106
q

$ cd ..
$ cp deployment.yaml deployment-dev.yaml

NOTE: this particular nginx puts the web src in a folder called /app. 

add in:
         - mountPath: /app
         name: www-src
     volumes:
     - name: www-src
     hostPath:
       path: /var/www/html
(see deployment-dev.yaml)

$ kubectl create -f deployment-dev.yaml 
configmap/nginx-1592766463-server-block created
service/nginx-1592766463 created
deployment.apps/nginx-1592766463 created

$ kubectl create -f deployment-dev.yaml 
configmap/nginx-1592766463-server-block created
service/nginx-1592766463 created
deployment.apps/nginx-1592766463 created

$ kubectl get all
NAME                                    READY   STATUS    RESTARTS   AGE
pod/nginx-1592766463-86b97bc7b7-dgcbs   1/1     Running   0          11s

NAME                       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
service/kubernetes         ClusterIP      10.96.0.1      <none>        443/TCP                      14d
service/nginx-1592766463   LoadBalancer   10.110.57.69   <pending>     80:30978/TCP,443:31171/TCP   11s

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-1592766463   1/1     1            1           11s

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-1592766463-86b97bc7b7   1         1         1       11s
$ minikube service nginx-1592766463 --url
http://172.17.0.2:30978
http://172.17.0.2:31171

$ curl http://172.17.0.2:30978
<html>
<head>
<title> Put a title here</title>
</head>
<body>
<h1>Put some body here</h1>
</body>
</html>

So now, we can modify the index.html in our www folder...

vi www/index.html
... make some changes ...
and you will see them right away.

```

## wrap up
```
This is a bit hacky I think, and we could probably do a better/(easier?) job messing with Docker direcly.
Still, some could info here, wrt to techniques.
```

