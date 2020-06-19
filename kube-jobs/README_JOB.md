# demo kuberenetes jobs 
link: https://www.youtube.com/watch?v=uJKE0d6Y_yg&list=PLGV4LXy81abYS_LIaO9LLt7uKY_jK7I6S&index=5&t=1594s

## setup
```
see README.md
```

## demo - around 2:57
```
$ kubectl cluster-info
Kubernetes master is running at https://172.17.0.2:8443
KubeDNS is running at https://172.17.0.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

$ kubectl version --short
Client Version: v1.18.3
Server Version: v1.18.3

NOTE: Demo uses v1.13.0; watch out for that.

$ kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
minikube   Ready    master   12d   v1.18.3

NOTE: demo is "real" kubernetes; he has a master and two workers. Watch out for that.

```

## demo - discussion 
```
normal use case for cluster would be to delpoy applciation that runs continusly
define replicas
if node goes down
the replica set will make sure pods are created 
so application is always up

jobs ... they just run, complete, and goes away

```

## demo - continues 4:27
```
NOTE: I am not going use his filenames.
so 

$ mkdir yamls
$ cat job.yaml 
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
        command: ["echo", "Hello Kubernetes!!!"]
      restartPolicy: Never

OK, so we set up another terminal to monitor this:
$ watch kubectl get all
Every 2.0s: kubectl get all                                                                             kube: Fri Jun 19 09:40:27 2020

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

$ kubectl create -f job.yaml
job.batch/helloworld created

Now we look at monitoring terminal, and see:

Every 2.0s: kubectl get all                                                                             kube: Fri Jun 19 09:41:29 2020

NAME                   READY   STATUS      RESTARTS   AGE
pod/helloworld-bvqgj   0/1     Completed   0          11s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

NAME                   COMPLETIONS   DURATION   AGE
job.batch/helloworld   1/1           3s         11s

Lets look at the logs from the pod:

$ kubectl logs pod/helloworld-bvqgj
Hello Kubernetes!!!


Describe job:
$ kubectl describe job helloworld
Name:           helloworld
Namespace:      default
Selector:       controller-uid=82bfc11a-c8ba-416e-b137-492a1639e7ab
Labels:         controller-uid=82bfc11a-c8ba-416e-b137-492a1639e7ab
                job-name=helloworld
Annotations:    <none>
Parallelism:    1
Completions:    1
Start Time:     Fri, 19 Jun 2020 09:41:18 -0400
Completed At:   Fri, 19 Jun 2020 09:41:21 -0400
Duration:       3s
Pods Statuses:  0 Running / 1 Succeeded / 0 Failed
Pod Template:
  Labels:  controller-uid=82bfc11a-c8ba-416e-b137-492a1639e7ab
           job-name=helloworld
  Containers:
   busybox:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      echo
      Hello Kubernetes!!!
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age    From            Message
  ----    ------            ----   ----            -------
  Normal  SuccessfulCreate  4m39s  job-controller  Created pod: helloworld-bvqgj
  Normal  Completed         4m36s  job-controller  Job completed


NOTE: The completed job doesn't clean up itself (which is good, since we want to pull the logs)
So clean up:

$ kubectl delete job helloworld
job.batch "helloworld" deleted

And on our monitoring screen, you can see its all gone now:

Every 2.0s: kubectl get all                                                                             kube: Fri Jun 19 09:48:52 2020

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

This ends the first part of the demo.

```

## showing restarts
```
he adds a sleep to the job, so that it runs a long time,
kills the pod, and shows that kerbentes tries again

      command: ["sleep", "60"]
```

## demo sequence
```
Next, he want to run this multiple times.
Under the spec, add 

  completions: 2

and put back the echo.

This will run the job twice, in sequence. (not parrallel)

$ cat job_seq.yaml 
apiVersion: batch/v1
kind: Job
metadata:
  name: helloworld
spec: 
  completions: 2
  template:
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ["echo", "Hello Kubernetes!!!"]
      restartPolicy: Never

$ kubectl create -f job_seq.yaml 
job.batch/helloworld created
$ kubectl describe job helloworld
Name:           helloworld
Namespace:      default
Selector:       controller-uid=a098cd61-4764-498b-8b5a-561358030daa
Labels:         controller-uid=a098cd61-4764-498b-8b5a-561358030daa
                job-name=helloworld
Annotations:    <none>
Parallelism:    1
Completions:    2
Start Time:     Fri, 19 Jun 2020 09:59:17 -0400
Completed At:   Fri, 19 Jun 2020 09:59:25 -0400
Duration:       8s
Pods Statuses:  0 Running / 2 Succeeded / 0 Failed
Pod Template:
  Labels:  controller-uid=a098cd61-4764-498b-8b5a-561358030daa
           job-name=helloworld
  Containers:
   busybox:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      echo
      Hello Kubernetes!!!
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age    From            Message
  ----    ------            ----   ----            -------
  Normal  SuccessfulCreate  2m36s  job-controller  Created pod: helloworld-vf7ff
  Normal  SuccessfulCreate  2m32s  job-controller  Created pod: helloworld-wnw7p
  Normal  Completed         2m28s  job-controller  Job completed
$ kubectl delete job helloworld
job.batch "helloworld" deleted
```

## Next, parrallellism
```
Add:
  parallelism: 2

Just under the completions: 2

So, this will run two jobs at once.
```

## Back off limit
```
In the case of a command failure...
So create a "bad" job:
We know from before, if a job exits with a failure, kube will restart.
This is not good in a production environment.

So, add backoffLimit: 2
$ cat job_broken.yaml 
apiVersion: batch/v1
kind: Job
metadata:
  name: helloworld
spec: 
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ["ls", "/nonexistantdir"]
      restartPolicy: Never

This will retry three times, and then fail.
Every 2.0s: kubectl get all                                                                             kube: Fri Jun 19 10:15:14 2020

NAME                   READY   STATUS   RESTARTS   AGE
pod/helloworld-66d4b   0/1     Error    0          2m11s
pod/helloworld-dv57s   0/1     Error    0          2m1s
pod/helloworld-hp6sk   0/1     Error    0          101s
pod/helloworld-p6n5h   0/1     Error    0          2m15s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

NAME                   COMPLETIONS   DURATION   AGE
job.batch/helloworld   0/1           2m15s      2m15s

$ kubectl describe job helloworld
Name:           helloworld
Namespace:      default
Selector:       controller-uid=0d1cb83a-323d-4ef4-a773-70db5b4d8f1a
Labels:         controller-uid=0d1cb83a-323d-4ef4-a773-70db5b4d8f1a
                job-name=helloworld
Annotations:    <none>
Parallelism:    1
Completions:    1
Start Time:     Fri, 19 Jun 2020 10:12:59 -0400
Pods Statuses:  0 Running / 0 Succeeded / 4 Failed
Pod Template:
  Labels:  controller-uid=0d1cb83a-323d-4ef4-a773-70db5b4d8f1a
           job-name=helloworld
  Containers:
   busybox:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      ls
      /nonexistantdir
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type     Reason                Age    From            Message
  ----     ------                ----   ----            -------
  Normal   SuccessfulCreate      2m53s  job-controller  Created pod: helloworld-p6n5h
  Normal   SuccessfulCreate      2m49s  job-controller  Created pod: helloworld-66d4b
  Normal   SuccessfulCreate      2m39s  job-controller  Created pod: helloworld-dv57s
  Normal   SuccessfulCreate      2m19s  job-controller  Created pod: helloworld-hp6sk
  Warning  BackoffLimitExceeded  99s    job-controller  Job has reached the specified backoff limit


So we can see that it has given up.

And clean up
$ kubectl delete job helloworld
job.batch "helloworld" deleted

```

## Timeout the job 
```
Next we want to terminate the job after a set amount of time. 

Kube call this activeDeadlineSeconds

$ cat job_too_long.yaml 
apiVersion: batch/v1
kind: Job
metadata:
  name: helloworld
spec: 
  activeDeadlineSeconds: 10
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ["sleep", "60"]
      restartPolicy: Never

Every 2.0s: kubectl get all                                                                             kube: Fri Jun 19 10:24:03 2020

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

NAME                   COMPLETIONS   DURATION   AGE
job.batch/helloworld   0/1           75s        75s



Note: The job was terminated after 10 seconds (you can watch this happen) 
      Also, kube it did NOT retry.

s$ kubectl describe job helloworld
Name:                     helloworld
Namespace:                default
Selector:                 controller-uid=08202e90-0bee-4fff-983f-6dff6950704a
Labels:                   controller-uid=08202e90-0bee-4fff-983f-6dff6950704a
                          job-name=helloworld
Annotations:              <none>
Parallelism:              1
Completions:              1
Start Time:               Fri, 19 Jun 2020 10:22:48 -0400
Active Deadline Seconds:  10s
Pods Statuses:            0 Running / 0 Succeeded / 1 Failed
Pod Template:
  Labels:  controller-uid=08202e90-0bee-4fff-983f-6dff6950704a
           job-name=helloworld
  Containers:
   busybox:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sleep
      60
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type     Reason            Age    From            Message
  ----     ------            ----   ----            -------
  Normal   SuccessfulCreate  3m13s  job-controller  Created pod: helloworld-tfhjk
  Normal   SuccessfulDelete  3m3s   job-controller  Deleted pod: helloworld-tfhjk
  Warning  DeadlineExceeded  3m3s   job-controller  Job was active longer than specified deadline

Note the DeadlineExceeded.

And cleanup.

$ kubectl delete job helloworld
job.batch "helloworld" deleted
```


