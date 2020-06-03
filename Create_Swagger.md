# Building an API with Swagger

Simple creation of yaml file using swagger editor.
I am working in a unbuntu 20.04 with docker etc installed.

Using online tutorial:
link: https://www.youtube.com/watch?v=6kwmW_p_Tig

## start by installing the swagger editor

```
$ docker pull swaggerapi/swagger-editor
$ docker run -d -p 8085:8080 swaggerapi/swagger-editor

Now you can access the editor on:
http://localhost:8085
```

## Pre-amble and Notes
```
We are interested in the OpenAPI specificiation (as opposed to the swagger API). 

link: https://www.youtube.com/watch?v=6kwmW_p_Tig

RESTful - Allow machines/tools to integrate with API
Allow humans to implement API code
Allow humans to read and generate API documentation and test cases


Some terms:

  OpenAPI
  Swagger - tools built around OpenAPI
  OAS
  OAI

The layers of 3.0:

  OpenAPI 3.0 - Layers
  
  [       info       ]
  [ servers][security]
  [       paths      ]
  [tags][externalDocs]
  [   components     ]


Supported Parameters:
  * Query (users?id=3)
  * Path (users/id/3)
  * Header (X-custom-users=3)
  * Cookies(cookie: users=3)

New/Altered from 2.0:
  RequestBody
  Serialization support by defining media types

  Content Negotiation 

  content:
    appliciation/json
       schema:
         $ref: '#/components/schemas/Employees'
    application/xml
       schema:
        $ref: '#/components/schemas/Employees'
```


## DEMO

HR API demo. obtain info for employees, or post

### Required actions:
```
One resource, Employee

GET - gives info for an array of employees; parameters: bodyLimit, pageLimit. responses: 200 payload: ID, Name, Title
GET - gives specific employee information; parameters: ID, responses: 200 payload: ID, Name, Title
POST - allows adding new employee, parameters: payload: ID, Name, Title, responses: 200
```

### Build the initial yaml
```
The demo uses swaggerhub. There is a cost to using swaggerhub; I will try to just use the swagger-editor instead.

OpenAPI Version: 3.0.0
Name: HR_API_OAS3.0
Version: 1.0.0
Title: HR API
Description: Simple Example of an HR API

So open: http://localhost:8085  

Initial yml:
Note: YAML is the preferred approached. (JSON is also available)

openapi: 3.0.0
info:
  version: '1.0.0'
  title: 'HR API'
  description: 'Simple Example of an HR API'
paths: {}
```

### Next. lets layout metadata: 
```
openapi: 3.0.0
info:
  version: '1.0.0'
  title: 'HR API'
  description: 'Simple Example of an HR API'
  termsOfService: https://www.gnu.org/licenses/gpl-3.0.en.html
  contact:
    name: Steve
    url:  https://github.com/steve1281/kubernetes_tutorial
    email: steve1281@hotmail.com
  license:
    name: Steve License
    url: https://www.gnu.org/licenses/gpl-3.0.en.html

servers: 
  - url: https://dev.foo.com/v1
    description: Dev Server
  - url: https://prod.foo.com/v1
    description: Prod Server
    
paths: {}
```

### Next. define the operations:
```
openapi: 3.0.0
info:
  version: '1.0.0'
  title: 'HR API'
  description: 'Simple Example of an HR API'
  termsOfService: https://www.gnu.org/licenses/gpl-3.0.en.html
  contact:
    name: Steve
    url:  https://github.com/steve1281/kubernetes_tutorial
    email: steve1281@hotmail.com
  license:
    name: Steve License
    url: https://www.gnu.org/licenses/gpl-3.0.en.html

servers: 
  - url: https://dev.foo.com/v1
    description: Dev Server
  - url: https://prod.foo.com/v1
    description: Prod Server
    
paths: 
  /employees:
    get:
      description: Obtain information about employees from the HR database
      parameters: 
        - name: bodyLimit
          in: query
          description: The amount of employes returned
          schema:
            type: integer
            minimum: 10
            maximum: 20
            example: 15
            
        - name: pageLimit
          in: query
          description: The pages to return employees info returned
          schema:
            type: integer
            minimum: 1
            maximum: 5
            example: 2
      responses:
        200:
          description: Successful pull of employee info
          content:
            application/json:
              schema:
                type: array
                items:
                  properties:
                    id: 
                      type: integer
                      example: 4
                    employee name:
                      type: string
                      example: John Smith
                    employee title:
                      type: string
                      example: Programmer
      
    post:
      description: Creates a new employee in the database
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                id: 
                  type: integer
                  example: 4
                employee name:
                  type: string
                  example: John Smith
                employee title:
                  type: string
                  example: Programmer
      responses:
        200:
          description: Successful employee creation.
                      
  /employees/{id}:
    get:
      description: Obtain information about specific employee
      parameters: 
        - in: path
          name: id
          required: true
          description: The ID of the employee
          schema:
            type: integer
            example: 54
      responses:
        200:
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  id: 
                    type: integer
                    example: 4
                  employee name:
                    type: string
                    example: John Smith
                  employee title:
                    type: string
                    example: Programmer        
```

### Simplify using components        

OK, so way too much repeated stuff!
We can add components (classes basically) to simplify:

```
openapi: 3.0.0
info:
  version: '1.0.0'
  title: 'HR API'
  description: 'Simple Example of an HR API'
  termsOfService: https://www.gnu.org/licenses/gpl-3.0.en.html
  contact:
    name: Steve
    url:  https://github.com/steve1281/kubernetes_tutorial
    email: steve1281@hotmail.com
  license:
    name: Steve License
    url: https://www.gnu.org/licenses/gpl-3.0.en.html

servers: 
  - url: https://dev.foo.com/v1
    description: Dev Server
  - url: https://prod.foo.com/v1
    description: Prod Server
    
paths: 
  /employees:
    get:
      description: Obtain information about employees from the HR database
      parameters: 
        - name: bodyLimit
          in: query
          description: The amount of employes returned
          schema:
            type: integer
            minimum: 10
            maximum: 20
            example: 15
            
        - name: pageLimit
          in: query
          description: The pages to return employees info returned
          schema:
            type: integer
            minimum: 1
            maximum: 5
            example: 2
      responses:
        200:
          description: Successful pull of employee info
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Employees"
      
    post:
      description: Creates a new employee in the database
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Employee'
              
      responses:
        200:
          description: Successful employee creation.
                      
  /employees/{id}:
    get:
      description: Obtain information about specific employee
      parameters: 
        - in: path
          name: id
          required: true
          description: The ID of the employee
          schema:
            type: integer
            example: 54
      responses:
        200:
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Employee'    
        
components:
  schemas:
    Employee:
      type: object
      description: Model containing employee info
      properties:
        id: 
          type: integer
          example: 4
        employee name:
          type: string
          example: John Smith
        employee title:
          type: string
          example: Programmer      
          
    Employees:
      description: Model of an array of Employee
      type: array
      items:
        $ref: '#/components/schemas/Employee'
```

### Final thoughts
```
Need to create a second demo on this, that takes this API and implements it
```
            
## Demo# 2
```
Yes, well there is no actual thing to work from online, so lets wing it and see what happens.

First, go ahead and create a folder for this work
$ mkdir ~/projects/kuber-demos/swagger-demo-2
$ mkdir ~/projects/kuber-demos/swagger-demo-2/server
$ mkdir ~/projects/kuber-demos/swagger-demo-2/client

Then, from the swagger-editor, create the zip files for the python client and server.
Then, extract them to the server and client folders above.

This will generate an obscene amount of crap.

steve@kube:~/projects/kuber-demos/swagger-demo-2$ tree
.
├── client
│   ├── docs
│   │   ├── DefaultApi.md
│   │   ├── Employee.md
│   │   └── Employees.md
│   ├── git_push.sh
│   ├── README.md
│   ├── requirements.txt
│   ├── setup.py
│   ├── swagger_client
│   │   ├── api
│   │   │   ├── default_api.py
│   │   │   └── __init__.py
│   │   ├── api_client.py
│   │   ├── configuration.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── employee.py
│   │   │   ├── employees.py
│   │   │   └── __init__.py
│   │   └── rest.py
│   ├── test
│   │   ├── __init__.py
│   │   ├── test_default_api.py
│   │   ├── test_employee.py
│   │   └── test_employees.py
│   ├── test-requirements.txt
│   └── tox.ini
└── server
    ├── Dockerfile
    ├── git_push.sh
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    ├── swagger_server
    │   ├── controllers
    │   │   ├── authorization_controller.py
    │   │   ├── default_controller.py
    │   │   └── __init__.py
    │   ├── encoder.py
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── models
    │   │   ├── base_model_.py
    │   │   ├── employee.py
    │   │   ├── employees.py
    │   │   └── __init__.py
    │   ├── swagger
    │   │   └── swagger.yaml
    │   ├── test
    │   │   ├── __init__.py
    │   │   └── test_default_controller.py
    │   └── util.py
    ├── test-requirements.txt
    └── tox.ini

12 directories, 43 files

```

### The server first

```
According the the README in the server folder, we can dock this easily enough.
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server

So lets try
The build worked ok.

But the run fails with ImportError: cannot import name 'FileStorage'
Looks like: https://github.com/zalando/connexion/issues/1149
Which kinda sucks.
So we modify the requirements.txt as recommended:

  Werkzeug==0.15.6
  Flask==1.1.1
  connexion==1.5.3
  # connexion == 2.2.0
  python_dateutil == 2.6.0
  setuptools >= 21.0.0

And retry.
and failed with:

jsonschema.exceptions.ValidationError: 'components', 'openapi', 'servers' do not match any of the regexes:

Ok, this is due to connexion being to old. Excellent.
First, just try going back to 2.2.0

steve@kube:~/projects/kuber-demos/swagger-demo-2/server$ docker run -p 8080:8080 swagger_server
The swagger_ui directory could not be found.
    Please install connexion with extra install: pip install connexion[swagger-ui]
    or provide the path to your local installation by passing swagger_path=<your path>

The swagger_ui directory could not be found.
    Please install connexion with extra install: pip install connexion[swagger-ui]
    or provide the path to your local installation by passing swagger_path=<your path>

 * Serving Flask app "__main__" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)

Well, there are some errors here. but maybe thats ok?
Lets try a GET. Keep in mind I have yet to write any code. so...

steve@kube:~/projects/kuber-demos/swagger-demo-2/server$ curl -X GET "http://localhost:8080/v1/employees?bodyLimit=15&pageLimit=2" -H  "accept: application/json"
"do some magic!"


That actually looks correct; I see generated code:

def employees_get(body_limit=None, page_limit=None):  # noqa: E501
    """employees_get

    Obtain information about employees from the HR database # noqa: E501

    :param body_limit: The amount of employes returned
    :type body_limit: int
    :param page_limit: The pages to return employees info returned
    :type page_limit: int

    :rtype: Employees
    """
    return 'do some magic!'

Lets try the other get:
curl -X GET "http://localhost:8080/v1/employees/1" -H  "accept: application/json"


Well, that failed with:
```
[2020-06-03 18:07:21,854] ERROR in app: Exception on /v1/employees/1 [GET]
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/site-packages/flask/app.py", line 2446, in wsgi_app
    response = self.full_dispatch_request()
  File "/usr/local/lib/python3.6/site-packages/flask/app.py", line 1951, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/usr/local/lib/python3.6/site-packages/flask/app.py", line 1820, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/usr/local/lib/python3.6/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/usr/local/lib/python3.6/site-packages/flask/app.py", line 1949, in full_dispatch_request
    rv = self.dispatch_request()
  File "/usr/local/lib/python3.6/site-packages/flask/app.py", line 1935, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/usr/local/lib/python3.6/site-packages/connexion/decorators/decorator.py", line 48, in wrapper
    response = function(request)
  File "/usr/local/lib/python3.6/site-packages/connexion/decorators/uri_parsing.py", line 143, in wrapper
    response = function(request)
  File "/usr/local/lib/python3.6/site-packages/connexion/decorators/validation.py", line 347, in wrapper
    return function(request)
  File "/usr/local/lib/python3.6/site-packages/connexion/decorators/parameter.py", line 126, in wrapper
    return function(**kwargs)
TypeError: employees_id_get() got an unexpected keyword argument 'id_'
172.17.0.1 - - [03/Jun/2020 18:07:21] "GET /v1/employees/1 HTTP/1.1" 500 

Will try manually changing parameter to id_ and see what happens.

```
So that fixed that. 

steve@kube:~/projects/kuber-demos/swagger-demo-2/server$ curl -X GET "http://localhost:8080/v1/employees/1" -H  "accept: application/json"
"do some magic!"

One more to do, the POST.

steve@kube:~/projects/kuber-demos/swagger-demo-2/server$ curl -X POST "http://localhost:8080/v1/employees" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"id\":4,\"employee name\":\"John Smith\",\"employee title\":\"Programmer\"}"
"do some magic!"

Guess that the server working. Kinda flaky, and SSL doesn't work at all. Several hacks later sort of thing.

### The client
Launch the server someplace
$ docker run -p 8080:8080 swagger_server

On another terminal (or launch it with a -d ). Switch to the client dir.

$ cd ~/projects/kuber-demos/swagger-demo-2/client

MORE on this to COME. 

