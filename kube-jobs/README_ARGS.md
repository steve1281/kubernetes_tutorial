# adding expermiment in argument passing
link: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/

This is seperate from the other demo work in this folder.

## as usual, start up minikube
```
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

```

## create a job_args.yaml
```
$ cat job_arg.yaml 
apiVersion: batch/v1
kind: Job
metadata:
  name: helloworld
spec: 
  template:
    spec:
      containers:
      - name: busybox
        image: busybox
        env:
        - name: MESSAGE
          value: "Hello Kerbernetes!!"
        command: ["echo"]
        args: ["$(MESSAGE)"]
      restartPolicy: Never

```

## build/test
```
$ kubectl create -f job_arg.yaml 
job.batch/helloworld created

$ kubectl get all
NAME                   READY   STATUS      RESTARTS   AGE
pod/helloworld-kmxhd   0/1     Completed   0          44s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

NAME                   COMPLETIONS   DURATION   AGE
job.batch/helloworld   1/1           6s         44s

$ kubectl logs pod/helloworld-kmxhd
Hello Kerbernetes!!

$ kubectl delete job helloworld
job.batch "helloworld" deleted

```

## slightly more interesting yaml
``` 
in this example, we put in /bin/sh so we can execute a script

$ cat job_script.yaml 
apiVersion: batch/v1
kind: Job
metadata:
  name: helloworld
spec: 
  template:
    spec:
      containers:
      - name: busybox
        image: busybox
        env:
        - name: MESSAGE
          value: "Hello Kerbernetes!!"
        command: ["/bin/sh"]
        args: ["-c", "while true; do echo $(MESSAGE); sleep 10; done"]
      restartPolicy: Never


$ kubectl create -f job_script.yaml 
job.batch/helloworld created


$ kubectl get all
NAME                   READY   STATUS    RESTARTS   AGE
pod/helloworld-q97xh   1/1     Running   0          18s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

NAME                   COMPLETIONS   DURATION   AGE
job.batch/helloworld   0/1           18s        18s


steve@kube:~/projects/kuber-demos/kube-jobs/yamls$ kubectl logs pod/helloworld-q97xh
Hello Kerbernetes!!
Hello Kerbernetes!!
Hello Kerbernetes!!
Hello Kerbernetes!!
steve@kube:~/projects/kuber-demos/kube-jobs/yamls$ kubectl logs pod/helloworld-q97xh
Hello Kerbernetes!!
Hello Kerbernetes!!
Hello Kerbernetes!!
Hello Kerbernetes!!
Hello Kerbernetes!!

```


