## setup
```
    virtualenv env
    pip3 install flask
    source env/bin/activate
```

## run
```
    python3 server.py
```

## test
```
    curl localhost:5000
    foo

then look at output in log.log
    cat log.log
    [2020-06-11 23:04:58,336] {/home/steve/projects/kuber-demos/flask-logger/logger.py:24} WARNING - ('A warning occurred (42 apples)',)
    [2020-06-11 23:04:58,336] {/home/steve/projects/kuber-demos/flask-logger/logger.py:27} ERROR - ('An error occurred',)

```

