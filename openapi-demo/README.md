virtualenv env

$ cat .gitignore 
env/
__pycache__

source env/bin/activate
pip3 install connexion


mkdir -p server/openapi
mkdir -p server/api

touch server/__init__.py
touch server/api/__init__.py
touch server/server.py
touch server/api/api.py
touch server/openapi/openapi.yaml

server.py:

import connexion

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapi.yaml')
app.run(port=8080)

Build the openapi.yaml

docker run -d -p 8085:8080 swaggerapi/swagger-editor

openapi.yaml:
openapi: 3.0.0
info:
  version: 1.0.0
  description: Simple Example
  title: Simple Example

paths:
  /version:
    get:
      operationId: api.version
      description: Display the version of this service.
      responses:
        200:
          description: Successfully found and returned version
          content:
            text/plain:
              schema:
                type: string
                example: 1.0.0 (latest)
        

Modify the __init__.py in the api folder:

$ cat server/api/__init__.py 
from .api import *

And add in a simple end point:

$ cat server/api/api.py
def version():
    return "1.0.1 (latest)\n"


