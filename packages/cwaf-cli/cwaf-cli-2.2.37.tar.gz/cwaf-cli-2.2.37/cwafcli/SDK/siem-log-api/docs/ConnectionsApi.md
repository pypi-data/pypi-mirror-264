# swagger_client.ConnectionsApi

All URIs are relative to *https://api.imperva.com/siem-config-service*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create1**](ConnectionsApi.md#create1) | **POST** /v3/connections/ | Create connection
[**delete1**](ConnectionsApi.md#delete1) | **DELETE** /v3/connections/{connectionId} | Delete connection
[**get1**](ConnectionsApi.md#get1) | **GET** /v3/connections/{connectionId} | Retrieve connection
[**get_all1**](ConnectionsApi.md#get_all1) | **GET** /v3/connections/ | Retrieve all connections
[**update1**](ConnectionsApi.md#update1) | **PUT** /v3/connections/{connectionId} | Overwrite connection

# **create1**
> ConnectionDtoResponse create1(body)

Create connection

Define the details of your log storage repository including the path to the repository and the access credentials Imperva needs to push the logs.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.ConnectionsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConnectionDtoResponse() # ConnectionDtoResponse | JSON body. Schema is identical to the response.

try:
    # Create connection
    api_response = api_instance.create1(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->create1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConnectionDtoResponse**](ConnectionDtoResponse.md)| JSON body. Schema is identical to the response. | 

### Return type

[**ConnectionDtoResponse**](ConnectionDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete1**
> delete1(connection_id)

Delete connection

Deletes a connection according to the connection ID.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.ConnectionsApi(swagger_client.ApiClient(configuration))
connection_id = 'connection_id_example' # str | The unique ID for the connection, assigned by Imperva. To find the connection ID, run GET /v3/connections

try:
    # Delete connection
    api_instance.delete1(connection_id)
except ApiException as e:
    print("Exception when calling ConnectionsApi->delete1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| The unique ID for the connection, assigned by Imperva. To find the connection ID, run GET /v3/connections | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get1**
> ConnectionDtoResponse get1(connection_id)

Retrieve connection

Retrieves details of a specific connection according to the connection ID.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.ConnectionsApi(swagger_client.ApiClient(configuration))
connection_id = 'connection_id_example' # str | The unique ID for the connection, assigned by Imperva. To find the connection ID, run GET /v3/connections

try:
    # Retrieve connection
    api_response = api_instance.get1(connection_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->get1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| The unique ID for the connection, assigned by Imperva. To find the connection ID, run GET /v3/connections | 

### Return type

[**ConnectionDtoResponse**](ConnectionDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all1**
> ConnectionDtoResponse get_all1()

Retrieve all connections

Retrieves details of all connections in the account.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.ConnectionsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve all connections
    api_response = api_instance.get_all1()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->get_all1: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ConnectionDtoResponse**](ConnectionDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update1**
> ConnectionDtoResponse update1(body, connection_id)

Overwrite connection

Updates a connection according to the connection ID. Overwrites the connection’s previous values.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.ConnectionsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConnectionDtoResponse() # ConnectionDtoResponse | JSON body. Schema is identical to the response.
connection_id = 'connection_id_example' # str | The unique ID for the connection, assigned by Imperva. To find the connection ID, run GET /v3/connections

try:
    # Overwrite connection
    api_response = api_instance.update1(body, connection_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->update1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConnectionDtoResponse**](ConnectionDtoResponse.md)| JSON body. Schema is identical to the response. | 
 **connection_id** | **str**| The unique ID for the connection, assigned by Imperva. To find the connection ID, run GET /v3/connections | 

### Return type

[**ConnectionDtoResponse**](ConnectionDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

