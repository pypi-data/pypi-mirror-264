# swagger_client.ConnectivityTestsApi

All URIs are relative to *https://api.imperva.com/troubleshooting-center*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_connectivity_check_api_result**](ConnectivityTestsApi.md#get_connectivity_check_api_result) | **POST** /v3/connectivityTests/{assetType}/{assetId} | Retrieve connectivity tests for a given website.

# **get_connectivity_check_api_result**
> ApiResult get_connectivity_check_api_result(body, asset_type, asset_id)

Retrieve connectivity tests for a given website.

Retrieves details of connectivity tests of a given website.

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
api_instance = swagger_client.ConnectivityTestsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConnectivityTestSearch() # ConnectivityTestSearch | Filters
asset_type = 'asset_type_example' # str | 
asset_id = 789 # int | Numeric identifier of the site to retrieve.

try:
    # Retrieve connectivity tests for a given website.
    api_response = api_instance.get_connectivity_check_api_result(body, asset_type, asset_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectivityTestsApi->get_connectivity_check_api_result: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConnectivityTestSearch**](ConnectivityTestSearch.md)| Filters | 
 **asset_type** | **str**|  | 
 **asset_id** | **int**| Numeric identifier of the site to retrieve. | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

