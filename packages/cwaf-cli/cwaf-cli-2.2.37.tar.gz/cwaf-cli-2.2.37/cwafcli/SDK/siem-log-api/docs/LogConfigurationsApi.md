# swagger_client.LogConfigurationsApi

All URIs are relative to *https://api.imperva.com/siem-config-service*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](LogConfigurationsApi.md#create) | **POST** /v3/log-configurations/ | Create log configuration
[**delete**](LogConfigurationsApi.md#delete) | **DELETE** /v3/log-configurations/{configurationId} | Delete log configuration
[**get**](LogConfigurationsApi.md#get) | **GET** /v3/log-configurations/{configurationId} | Retrieve log configuration
[**get_all**](LogConfigurationsApi.md#get_all) | **GET** /v3/log-configurations/ | Retrieve all log configurations
[**update**](LogConfigurationsApi.md#update) | **PUT** /v3/log-configurations/{configurationId} | Overwrite log configuration

# **create**
> LogConfigurationDtoResponse create(body)

Create log configuration

Define the logs that you want to receive from Imperva, and the connection to use to receive them. The available services and log types are based on the account’s subscribed services.

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
api_instance = swagger_client.LogConfigurationsApi(swagger_client.ApiClient(configuration))
body = swagger_client.LogConfigurationDtoResponse() # LogConfigurationDtoResponse | JSON body. Schema is identical to the response.

try:
    # Create log configuration
    api_response = api_instance.create(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LogConfigurationsApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LogConfigurationDtoResponse**](LogConfigurationDtoResponse.md)| JSON body. Schema is identical to the response. | 

### Return type

[**LogConfigurationDtoResponse**](LogConfigurationDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete**
> delete(configuration_id)

Delete log configuration

Deletes a log configuration according to the configuration ID.

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
api_instance = swagger_client.LogConfigurationsApi(swagger_client.ApiClient(configuration))
configuration_id = 'configuration_id_example' # str | The unique ID for the log configuration, assigned by Imperva. To find the configuration ID, run GET /v3/log-configurations

try:
    # Delete log configuration
    api_instance.delete(configuration_id)
except ApiException as e:
    print("Exception when calling LogConfigurationsApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **configuration_id** | **str**| The unique ID for the log configuration, assigned by Imperva. To find the configuration ID, run GET /v3/log-configurations | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get**
> LogConfigurationDtoResponse get(configuration_id)

Retrieve log configuration

Retrieves details of a specific log configuration according to the configuration ID.

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
api_instance = swagger_client.LogConfigurationsApi(swagger_client.ApiClient(configuration))
configuration_id = 'configuration_id_example' # str | The unique ID for the log configuration, assigned by Imperva. To find the configuration ID, run GET /v3/log-configurations

try:
    # Retrieve log configuration
    api_response = api_instance.get(configuration_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LogConfigurationsApi->get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **configuration_id** | **str**| The unique ID for the log configuration, assigned by Imperva. To find the configuration ID, run GET /v3/log-configurations | 

### Return type

[**LogConfigurationDtoResponse**](LogConfigurationDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all**
> LogConfigurationDtoResponse get_all()

Retrieve all log configurations

Retrieves details of all configurations in the account.

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
api_instance = swagger_client.LogConfigurationsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve all log configurations
    api_response = api_instance.get_all()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LogConfigurationsApi->get_all: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**LogConfigurationDtoResponse**](LogConfigurationDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> LogConfigurationDtoResponse update(body, configuration_id)

Overwrite log configuration

Updates a log configuration according to the configuration ID. Overwrites the configuration’s previous values.

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
api_instance = swagger_client.LogConfigurationsApi(swagger_client.ApiClient(configuration))
body = swagger_client.LogConfigurationDtoResponse() # LogConfigurationDtoResponse | JSON body. Schema is identical to the response.
configuration_id = 'configuration_id_example' # str | The unique ID for the log configuration, assigned by Imperva. To find the configuration ID, run GET /v3/log-configurations

try:
    # Overwrite log configuration
    api_response = api_instance.update(body, configuration_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LogConfigurationsApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LogConfigurationDtoResponse**](LogConfigurationDtoResponse.md)| JSON body. Schema is identical to the response. | 
 **configuration_id** | **str**| The unique ID for the log configuration, assigned by Imperva. To find the configuration ID, run GET /v3/log-configurations | 

### Return type

[**LogConfigurationDtoResponse**](LogConfigurationDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

