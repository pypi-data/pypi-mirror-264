# swagger_client.DiscoveryHostsApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_hosts**](DiscoveryHostsApi.md#get_hosts) | **GET** /v2/discovery/hosts | Retrieves the account&#x27;s discovered hosts

# **get_hosts**
> GetHostsResponse get_hosts()

Retrieves the account's discovered hosts

Retrieves a list of all hosts discovered within a particular account.

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
api_instance = swagger_client.DiscoveryHostsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieves the account's discovered hosts
    api_response = api_instance.get_hosts()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryHostsApi->get_hosts: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetHostsResponse**](GetHostsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

