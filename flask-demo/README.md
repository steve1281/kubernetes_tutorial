
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

## dockerized
```
first, set the port in app.py to be 80. (avoids firewall issues)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

then:
  docker build -t steve1281/flask-demo .
  docker run -p 5000:80 steve1281/flask-demo

```

## kubernete...
```
todo
```


