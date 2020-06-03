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
            







 
