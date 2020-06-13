# Instructions for adding helm to the VM

```
link: https://helm.sh/docs/intro/quickstart/

Note: You must already have kubernetes installed.
      You must already have kubectl installed.
```

## start up kube
```

steve@kube:~/projects/kuber-demos$ minikube start
😄  minikube v1.11.0 on Ubuntu 20.04
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.18.3 on Docker 19.03.2 ...
    ▪ kubeadm.pod-network-cidr=10.244.0.0/16
🔎  Verifying Kubernetes components...
🌟  Enabled addons: dashboard, default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube"

steve@kube:~/projects/kuber-demos$ kubectl config current-context
minikube
```

## install
```
steve@kube:~/projects/kuber-demos$ sudo snap install helm --classic
[sudo] password for steve: 
helm 3.2.3 from Snapcrafters installed

steve@kube:~/projects/kuber-demos$ helm version
version.BuildInfo{Version:"v3.2.3", GitCommit:"8f832046e258e2cb800894579b1b3b50c2d83492", GitTreeState:"clean", GoVersion:"go1.13.12"}

note: I could have wget the binary (see link) but this is easier.
```

## add a helm repository
```
I have no reason not to add the recommended one; at work it would be different of course.

steve@kube:~/projects/kuber-demos$ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
"stable" has been added to your repositories

steve@kube:~/projects/kuber-demos$ helm search repo stable
NAME                                    CHART VERSION   APP VERSION             DESCRIPTION                                       
stable/aerospike                        0.3.2           v4.5.0.5                A Helm chart for Aerospike in Kubernetes          
stable/airflow                          7.1.5           1.10.10                 Airflow is a platform to programmatically autho...
...
stable/weave-scope                      1.1.10          1.12.0                  A Helm chart for the Weave Scope cluster visual...
stable/zeppelin                         1.1.0           0.7.2                   Web-based notebook that enables data-driven, in...
stable/zetcd                            0.1.9           0.0.3                   CoreOS zetcd Helm chart for Kubernetes            

A long-ish list.
```

## sanity check
```

steve@kube:~/projects/kuber-demos$ helm repo update # get latest
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈ Happy Helming!⎈ 

steve@kube:~/projects/kuber-demos$ helm install stable/mysql --generate-name
NAME: mysql-1592074759
LAST DEPLOYED: Sat Jun 13 14:59:22 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
MySQL can be accessed via port 3306 on the following DNS name from within your cluster:
mysql-1592074759.default.svc.cluster.local

To get your root password run:

    MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default mysql-1592074759 -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)

To connect to your database:

1. Run an Ubuntu pod that you can use as a client:

    kubectl run -i --tty ubuntu --image=ubuntu:16.04 --restart=Never -- bash -il

2. Install the mysql client:

    $ apt-get update && apt-get install mysql-client -y

3. Connect using the mysql cli, then provide your password:
    $ mysql -h mysql-1592074759 -p

To connect to your database directly from outside the K8s cluster:
    MYSQL_HOST=127.0.0.1
    MYSQL_PORT=3306

    # Execute the following command to route the connection:
    kubectl port-forward svc/mysql-1592074759 3306

    mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_ROOT_PASSWORD}

steve@kube:~/projects/kuber-demos$ helm list
NAME            	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART      	APP VERSION
mysql-1592074759	default  	1       	2020-06-13 14:59:22.551117401 -0400 EDT	deployed	mysql-1.6.4	5.7.30     

steve@kube:~/projects/kuber-demos$ kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
mysql-1592074759   1/1     1            1           3m34s

steve@kube:~/projects/kuber-demos$ kubectl get services
NAME               TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes         ClusterIP      10.96.0.1       <none>        443/TCP          6d15h
mysql-1592074759   ClusterIP      10.96.227.140   <none>        3306/TCP         3m59s

steve@kube:~/projects/kuber-demos$ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
mysql-1592074759-784b5747f9-gwgbr   1/1     Running   0          4m23s

For now, just uninstall:

steve@kube:~/projects/kuber-demos$ helm uninstall mysql-1592074759
release "mysql-1592074759" uninstalled

steve@kube:~/projects/kuber-demos$ helm list
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION

```

## whats next
```
Next, we will move to building something more interesting; stay tuned for a helm-example.
```

