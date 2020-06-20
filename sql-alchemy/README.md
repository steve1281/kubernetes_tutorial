# sql-alchemy, postgres, helm and kuberenetes

link: https://www.youtube.com/watch?v=4bIB86LRX7I
(well, inspired by?)

## installation
```
$ virtual env
$ source env/bin/activate
$ pip install Flask-SqlAlchemy
$ pip install psycopg2-binary   # binary to avoid having to install postgres locally
                                # in order to build it, they need libs and such on your dev box
                                # which is a violation of container law, imho.
$ pip install flask
$ pip install flask_sqlalchemy  # ok, not sure WHY I had to run this?

# needed bitnami repo to get non-deprecated postgresql 
$ helm repo add bitnami https://charts.bitnami.com/bitnami


```

## install postgres
```
$ helm install bitnami/postgresql --generate-name
NAME: postgresql-1592677916
LAST DEPLOYED: Sat Jun 20 14:31:58 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
** Please be patient while the chart is being deployed **

PostgreSQL can be accessed via port 5432 on the following DNS name from within your cluster:

    postgresql-1592677916.default.svc.cluster.local - Read/Write connection

To get the password for "postgres" run:

    export POSTGRES_PASSWORD=$(kubectl get secret --namespace default postgresql-1592677916 -o jsonpath="{.data.postgresql-password}" | base64 --decode)

To connect to your database run the following command:

    kubectl run postgresql-1592677916-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:11.8.0-debian-10-r33 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host postgresql-1592677916 -U postgres -d postgres -p 5432


To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/postgresql-1592677916 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432

```
## post-install
```
$ echo $(kubectl get secret --namespace default postgresql-1592677916 -o jsonpath="{.data.postgresql-password}" | base64 --decode)
uU7PaQAoNI

$ kubectl port-forward --namespace default svc/postgresql-1592677916 5432:5432 &

$ kubectl run postgresql-1592677916-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:11.8.0-debian-10-r33 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host postgresql-1592677916 -U postgres -d postgres -p 5432
If you don't see a command prompt, try pressing enter.[ed. This means, press enter]

postgres=# 
exit

Build the initial database :

$ python
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from sqlalchemy import create_engine
>>> db_string = "postgres://postgres:uU7PaQAoNI@127.0.0.1:5432/postgres" # postgres is there by default.
>>> db = create_engine(db_string)
>>> conn = db.connect()
>>> conn.execute("commit") # need to commit before starting a new transaction
<sqlalchemy.engine.result.ResultProxy object at 0x7f8d5c6a2a90>
>>> conn.execute("create database alchemy")
<sqlalchemy.engine.result.ResultProxy object at 0x7f8d5c644fd0>
>>> conn.close()
>>> quit()

Back on our other terminal, see the forwarding happening:

  Forwarding from 127.0.0.1:5432 -> 5432
  Forwarding from [::1]:5432 -> 5432
  Handling connection for 5432
  Handling connection for 5432

```
## Connection strings examples from demo.
```
These are helpful, if not accurate.

postgressql://scott:tiger@localhost/mydatabase
mysql://scott:tiger@localhost/mydatabase
oracle://scott:tiger@127.0.01:1521/sidname
```


## back to the demo
```
And he works in mysql, prefer to use postgres
So, above you'll find I set up postgres and added a database called alchemy.

We have out connection above, and he uses the dbname of ...alchemy.
(skip to 3:27)
vi Main.py # or code, or pycharm, or emacs. Wait, not emacs.

We add a model descendant, called User.  (see code)

Then, back into python for more manual hacking
$ python
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from Main import db
>>> db.create_all()
>>> exit()

Check that table was created:

$ kubectl run postgresql-1592677916-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:11.8.0-debian-10-r33 --env="PGPASSWORD=uU7PaQAoNI" --command -- psql --host postgresql-1592677916 -U postgres -d postgres -p 5432
If you don't see a command prompt, try pressing enter.

postgres=# \list
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
-----------+----------+----------+-------------+-------------+-----------------------
 alchemy   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(4 rows)

postgres=# \connect alchemy
You are now connected to database "alchemy" as user "postgres".
alchemy=# \dt
        List of relations
 Schema | Name | Type  |  Owner   
--------+------+-------+----------
 public | user | table | postgres
(1 row)

Hmm. At this point in the demo, he re-uses his code to create another table.
He struggles. (session needs to be committed?)
And thats the entire demo.
```

# wrap up
```
This demo is pretty much trivial, but useful when your getting started.
Also, it shows some helm and kube magic, and thats always good.
```

