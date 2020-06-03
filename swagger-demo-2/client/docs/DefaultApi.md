# swagger_client.DefaultApi

All URIs are relative to *https://dev.foo.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**employees_get**](DefaultApi.md#employees_get) | **GET** /employees | 
[**employees_id_get**](DefaultApi.md#employees_id_get) | **GET** /employees/{id} | 
[**employees_post**](DefaultApi.md#employees_post) | **POST** /employees | 

# **employees_get**
> Employees employees_get(body_limit=body_limit, page_limit=page_limit)



Obtain information about employees from the HR database

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body_limit = 56 # int | The amount of employes returned (optional)
page_limit = 56 # int | The pages to return employees info returned (optional)

try:
    api_response = api_instance.employees_get(body_limit=body_limit, page_limit=page_limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->employees_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body_limit** | **int**| The amount of employes returned | [optional] 
 **page_limit** | **int**| The pages to return employees info returned | [optional] 

### Return type

[**Employees**](Employees.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **employees_id_get**
> Employee employees_id_get(id)



Obtain information about specific employee

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
id = 56 # int | The ID of the employee

try:
    api_response = api_instance.employees_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->employees_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The ID of the employee | 

### Return type

[**Employee**](Employee.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **employees_post**
> employees_post(body)



Creates a new employee in the database

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.Employee() # Employee | 

try:
    api_instance.employees_post(body)
except ApiException as e:
    print("Exception when calling DefaultApi->employees_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Employee**](Employee.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

