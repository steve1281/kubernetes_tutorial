# example helm i3.x

follow : https://opensource.com/article/20/5/helm-charts
(the developer who did the demo is Jessica Cherry - hence the name cherry in the demo)

## make sure kubernetes is running
```
minikube start

steve@kube:~/projects/kuber-demos/helm-example$ minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

## create helm boiler
```
steve@kube:~/projects/kuber-demos/helm-example$ helm create buildachart
Creating buildachart
steve@kube:~/projects/kuber-demos/helm-example$ tree
.
└── buildachart
    ├── charts
    ├── Chart.yaml
    ├── templates
    │   ├── deployment.yaml
    │   ├── _helpers.tpl
    │   ├── hpa.yaml
    │   ├── ingress.yaml
    │   ├── NOTES.txt
    │   ├── serviceaccount.yaml
    │   ├── service.yaml
    │   └── tests
    │       └── test-connection.yaml
    └── values.yaml

4 directories, 10 files
steve@kube:~/projects/kuber-demos/helm-example$ 

```

## what did we make
```
lots of files

Chart.yaml outlines the helm chart structure.
templates/ holds the configurations for your application
charts/ stores any downloaded templates
values.yaml stores the default overloads for the template files

```

## modifications to value.yaml
```
set the pullPolicy to Always

etc

```

## install
```
steve@kube:~/projects/kuber-demos/helm-example$ helm install my-cherry-chart buildachart/ --values buildachart/values.yaml 
NAME: my-cherry-chart
LAST DEPLOYED: Sat Jun 13 20:34:20 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services cherry-chart)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```

## testing
```
steve@kube:~/projects/kuber-demos/helm-example$   export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services cherry-chart)
steve@kube:~/projects/kuber-demos/helm-example$   export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
steve@kube:~/projects/kuber-demos/helm-example$   echo http://$NODE_IP:$NODE_PORT
http://172.17.0.2:31109

steve@kube:~/projects/kuber-demos/helm-example$ curl http://172.17.0.2:31109
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
```

# whats next
```
this wasn't too exciting. the resulting boilerplate is mostly unused and unclear.
plus we didn't write any code, instead we just used a pre-existing chart (nginx).

Need an example of a nice python flask application - stay tuned.

```
