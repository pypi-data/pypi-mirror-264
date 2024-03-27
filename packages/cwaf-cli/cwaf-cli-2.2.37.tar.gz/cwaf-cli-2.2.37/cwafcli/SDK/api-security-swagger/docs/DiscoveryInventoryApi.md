# swagger_client.DiscoveryInventoryApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_discovered_api_files**](DiscoveryInventoryApi.md#get_discovered_api_files) | **GET** /v2/discovery/inventory/endpoints/files | Download all OAS files of the discovered APIs to a compressed ZIP file
[**get_discovered_endpoints**](DiscoveryInventoryApi.md#get_discovered_endpoints) | **GET** /v2/discovery/inventory/endpoints | Retrieve all discovered endpoints
[**get_endpoint_drill_down**](DiscoveryInventoryApi.md#get_endpoint_drill_down) | **GET** /v2/discovery/inventory/endpoints/{endpointId} | Retrieve detailed information for the endpoint
[**relearn_risk**](DiscoveryInventoryApi.md#relearn_risk) | **DELETE** /v2/discovery/inventory/endpoints/risks | Relearn risk data

# **get_discovered_api_files**
> get_discovered_api_files(host_ids=host_ids)

Download all OAS files of the discovered APIs to a compressed ZIP file

Download all OAS files of the discovered APIs, for all hosts or selected hosts in the query, to a compressed ZIP file. The ZIP file format is account-<account_id>-api-files.zip and the ZIP file name format is <host_name>-<base_path>-discovery.json. Underscore is used as the delimiter for the basePath.

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
api_instance = swagger_client.DiscoveryInventoryApi(swagger_client.ApiClient(configuration))
host_ids = 'host_ids_example' # str | Comma separated list of host ids (optional)

try:
    # Download all OAS files of the discovered APIs to a compressed ZIP file
    api_instance.get_discovered_api_files(host_ids=host_ids)
except ApiException as e:
    print("Exception when calling DiscoveryInventoryApi->get_discovered_api_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_ids** | **str**| Comma separated list of host ids | [optional] 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_discovered_endpoints**
> GetDiscoveredEndpointsResponse get_discovered_endpoints(host_ids=host_ids)

Retrieve all discovered endpoints

Retrieve all discovered endpoints for the account or for the specified hosts. If no host id is provided - retrieve all discovered endpoints for all hosts

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
api_instance = swagger_client.DiscoveryInventoryApi(swagger_client.ApiClient(configuration))
host_ids = 'host_ids_example' # str | Comma separated list of host ids (optional)

try:
    # Retrieve all discovered endpoints
    api_response = api_instance.get_discovered_endpoints(host_ids=host_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryInventoryApi->get_discovered_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_ids** | **str**| Comma separated list of host ids | [optional] 

### Return type

[**GetDiscoveredEndpointsResponse**](GetDiscoveredEndpointsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_endpoint_drill_down**
> GetEndpointDrillDownResponse get_endpoint_drill_down(endpoint_id)

Retrieve detailed information for the endpoint

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
api_instance = swagger_client.DiscoveryInventoryApi(swagger_client.ApiClient(configuration))
endpoint_id = 789 # int | endpoint ID

try:
    # Retrieve detailed information for the endpoint
    api_response = api_instance.get_endpoint_drill_down(endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryInventoryApi->get_endpoint_drill_down: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_id** | **int**| endpoint ID | 

### Return type

[**GetEndpointDrillDownResponse**](GetEndpointDrillDownResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **relearn_risk**
> ApiSuccessResponse relearn_risk(endpoint_ids=endpoint_ids)

Relearn risk data

Deletes the current risk data and adds new risk data by relearning

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
api_instance = swagger_client.DiscoveryInventoryApi(swagger_client.ApiClient(configuration))
endpoint_ids = 'endpoint_ids_example' # str | endpointIds (optional)

try:
    # Relearn risk data
    api_response = api_instance.relearn_risk(endpoint_ids=endpoint_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryInventoryApi->relearn_risk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_ids** | **str**| endpointIds | [optional] 

### Return type

[**ApiSuccessResponse**](ApiSuccessResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

