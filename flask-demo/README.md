
# How to get this running.

From a fresh clone you will need to setup your virtual env and initialize the database.

## setup virtualenv
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

## initialize the database
```
python3
>>> from app import db
>>> db.create_all()
>>> exit()
```

## and run
```
python3 app.py
```

## check work
```
Just open http://localhost:5000
```


