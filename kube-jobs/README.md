# demo kuberenetes jobs and cronjobs
link: https://www.youtube.com/watch?v=uJKE0d6Y_yg&list=PLGV4LXy81abYS_LIaO9LLt7uKY_jK7I6S&index=5&t=1594s

```
Using two README files, JOBS and CRONJOBS.  The demo does JOBS first.

```

## setup
```
need a clean kube, so 
minikube start
$ helm list
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d
```

## demo - what I am not doing.
```
He uses vagrant. I don't
I use minikube; see setup above.
Not copying config files
or any of that
```

## go do README_JOB.md

## go do README_CRONJOB.md

## conclusions/notes
```
Need some tools for monitoring/log extraction and collection/cleanup
Also, need to think about injecting values - maybe helm can help with this.

```

