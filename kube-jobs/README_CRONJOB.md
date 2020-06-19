# demo kuberenetes jobs and cronjobs
link: https://www.youtube.com/watch?v=uJKE0d6Y_yg&list=PLGV4LXy81abYS_LIaO9LLt7uKY_jK7I6S&index=5&t=1594s

## setup
```
see README.md
```

## demo - around 17:57
```
cron jobs are similair to unix.

$ cat cron.yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: helloworld-cron
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: busybox
            image: busybox
            command: ["echo", "Hello Kubernetes!!"]
          restartPolicy: Never


Quick cron review:

  minute hour day month day_of_the_week
  *      *    *   *     *

So 5 stars means run every single minute.
Also, can do stuff like

  */5 * * * *
Every five minutes.

  *30 * * * * 
On the half hour

  *0 * * * 1,2,3
On the hour, on 1st, 2nd and 3rd days of the week.
(week starts on Monday)

$ kubectl create -f cron.yaml 
cronjob.batch/helloworld-cron created

Look at the monitor terminal (watch kubectl get all)
(after 2 minutes)

Every 2.0s: kubectl get all                                                                             kube: Fri Jun 19 11:21:35 2020

NAME                                   READY   STATUS      RESTARTS   AGE
pod/helloworld-cron-1592580000-cf4j6   0/1     Completed   0          89s
pod/helloworld-cron-1592580060-l8c9h   0/1     Completed   0          28s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   12d

NAME                                   COMPLETIONS   DURATION   AGE
job.batch/helloworld-cron-1592580000   1/1           5s         89s
job.batch/helloworld-cron-1592580060   1/1           4s         28s

NAME                            SCHEDULE    SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/helloworld-cron   * * * * *   False     0        35s             103s

If you wait couple more minutes, you'll see more dead pods.

Lets look at the description

$ kubectl describe cronjob helloworld-cron
Name:                          helloworld-cron
Namespace:                     default
Labels:                        <none>
Annotations:                   <none>
Schedule:                      * * * * *
Concurrency Policy:            Allow
Suspend:                       False
Successful Job History Limit:  3
Failed Job History Limit:      1
Starting Deadline Seconds:     <unset>
Selector:                      <unset>
Parallelism:                   <unset>
Completions:                   <unset>
Pod Template:
  Labels:  <none>
  Containers:
   busybox:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      echo
      Hello Kubernetes!!
    Environment:     <none>
    Mounts:          <none>
  Volumes:           <none>
Last Schedule Time:  Fri, 19 Jun 2020 11:24:00 -0400
Active Jobs:         <none>
Events:
  Type    Reason            Age    From                Message
  ----    ------            ----   ----                -------
  Normal  SuccessfulCreate  4m49s  cronjob-controller  Created job helloworld-cron-1592580000
  Normal  SawCompletedJob   4m39s  cronjob-controller  Saw completed job: helloworld-cron-1592580000, status: Complete
  Normal  SuccessfulCreate  3m48s  cronjob-controller  Created job helloworld-cron-1592580060
  Normal  SawCompletedJob   3m38s  cronjob-controller  Saw completed job: helloworld-cron-1592580060, status: Complete
  Normal  SuccessfulCreate  2m48s  cronjob-controller  Created job helloworld-cron-1592580120
  Normal  SawCompletedJob   2m38s  cronjob-controller  Saw completed job: helloworld-cron-1592580120, status: Complete
  Normal  SuccessfulCreate  108s   cronjob-controller  Created job helloworld-cron-1592580180
  Normal  SawCompletedJob   98s    cronjob-controller  Saw completed job: helloworld-cron-1592580180, status: Complete
  Normal  SuccessfulDelete  97s    cronjob-controller  Deleted job helloworld-cron-1592580000
  Normal  SuccessfulCreate  47s    cronjob-controller  Created job helloworld-cron-1592580240
  Normal  SawCompletedJob   37s    cronjob-controller  Saw completed job: helloworld-cron-1592580240, status: Complete
  Normal  SuccessfulDelete  37s    cronjob-controller  Deleted job helloworld-cron-1592580060

Pretty much what you would expect.

NOTE: it keeps (by default) the last three successful (3) pods.  In terms of log collection, this is important to know.
      Also, keeps the failed pod.

And cleanup:
$ kubectl delete cronjob helloworld-cron 
cronjob.batch "helloworld-cron" deleted

NOTE: sometimes it doesn't clean up everything. (my thought here is that it won't kill a job in flight)
      In this case, you need to manually delete. So, for example, kubectl delete pods --all
      (um, don't do this in a real system, it will kill everything. bad demo)


```

## modify history
```
successfulJobsHistoryLimit: 0 # this by default was 3
failedJobsHistoryLimit: 0 # this by default is 1

By setting to 0, we lost our ability to query the pods for logs.
```

## pause/suspend running job
```
you want to diagnosis
so you want the cronjob to suspend
won't stop anything already going, but will stop future jobs

suspend: true

edit yaml, and apply
there is also a command line approach
edit the yaml is auditable.

note the different command:

$ kubectl apply -f cron.job


Observe that SUSPEND becomes true
And no new jobs are spawned

from the commandline
YOU CAN PATCH RUNNING JOBS!!!

$ kubectl patch cronjob helloworld-cron -p '{"spec":{"suspend":false}}'
```

## concurrency
```
concurrencyPolicy Allow Forbid Replace
default Allow

Question is: do you want the cronjob to launch while another cronjob is already running?
Allow - it will launch another
Forbid - second job will not launch
Replace - kill first, start next one


```

