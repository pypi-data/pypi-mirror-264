# swagger_client.EndpointApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_user_facing_endpoints**](EndpointApi.md#get_all_user_facing_endpoints) | **GET** /endpoint/{apiId} | Retrieve all endpoints
[**get_user_facing_endpoint**](EndpointApi.md#get_user_facing_endpoint) | **GET** /endpoint/{apiId}/{endpointId} | Retrieve an endpoint
[**update_endpoint**](EndpointApi.md#update_endpoint) | **POST** /endpoint/{apiId}/{endpointId} | Update an endpoint

# **get_all_user_facing_endpoints**
> GetEndpointsResponse get_all_user_facing_endpoints(api_id)

Retrieve all endpoints

Retrieve details on all endpoints for an API

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
api_instance = swagger_client.EndpointApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID

try:
    # Retrieve all endpoints
    api_response = api_instance.get_all_user_facing_endpoints(api_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->get_all_user_facing_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 

### Return type

[**GetEndpointsResponse**](GetEndpointsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_facing_endpoint**
> GetEndpointResponse get_user_facing_endpoint(api_id, endpoint_id)

Retrieve an endpoint

Retrieve details for an endpoint

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
api_instance = swagger_client.EndpointApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID
endpoint_id = 789 # int | The endpoint ID

try:
    # Retrieve an endpoint
    api_response = api_instance.get_user_facing_endpoint(api_id, endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->get_user_facing_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 
 **endpoint_id** | **int**| The endpoint ID | 

### Return type

[**GetEndpointResponse**](GetEndpointResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_endpoint**
> UpdateEndpointResponse update_endpoint(api_id, endpoint_id, specification_violation_action=specification_violation_action, violation_actions=violation_actions)

Update an endpoint

Update an endpoint API Specification Violation Action

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
api_instance = swagger_client.EndpointApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID
endpoint_id = 789 # int | The endpoint ID
specification_violation_action = 'specification_violation_action_example' # str |  (optional)
violation_actions = 'violation_actions_example' # str |  (optional)

try:
    # Update an endpoint
    api_response = api_instance.update_endpoint(api_id, endpoint_id, specification_violation_action=specification_violation_action, violation_actions=violation_actions)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EndpointApi->update_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 
 **endpoint_id** | **int**| The endpoint ID | 
 **specification_violation_action** | **str**|  | [optional] 
 **violation_actions** | **str**|  | [optional] 

### Return type

[**UpdateEndpointResponse**](UpdateEndpointResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

