# Build a really simple example of a flask - connexion app
```
note: we are using explicit routing in this example.
```

## setting up
```
virtualenv env
source ./env/bin/activate
pip3 install connexion
```

## build an api
```
docker run -d -p 8085:8080 swaggerapi/swagger-editor
open http://localhost:8085 and create a simple api
link: https://connexion.readthedocs.io/en/latest/routing.html
```

## build an implementation
```
steve@kube:~/projects/kuber-demos/flask-connex/server$ tree
.
├── __init__.py
├── openapi
│   └── openapi.yaml
├── server.py
└── service
    ├── api
    │   ├── hello_world.py
    │   └── __init__.py
    └── __init__.py
```

## run and test
```
(env) steve@kube:~/projects/kuber-demos/flask-connex/server$ python3 server.py
The swagger_ui directory could not be found.
    Please install connexion with extra install: pip install connexion[swagger-ui]
    or provide the path to your local installation by passing swagger_path=<your path>

The swagger_ui directory could not be found.
    Please install connexion with extra install: pip install connexion[swagger-ui]
    or provide the path to your local installation by passing swagger_path=<your path>

 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)


steve@kube:~/projects/kuber-demos$ curl http://localhost:8080/v1/hello_world
good bye world!
```

## notes
```

we didnt do implicit routing.
some notes on that then.
Need to add a resolver:

from connexion.resolver import RestyResolver

app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml', resolver=RestyResolver('api')

and then modules get resolved based on their paths:


paths:
  /:
    get:
       # Implied operationId: api.get
  /foo:
    get:
       # Implied operationId: api.foo.search
    post:
       # Implied operationId: api.foo.post

  '/foo/{id}':
    get:
       # Implied operationId: api.foo.get
    put:
       # Implied operationId: api.foo.put
    copy:
       # Implied operationId: api.foo.copy
    delete:
       # Implied operationId: api.foo.delete

```
