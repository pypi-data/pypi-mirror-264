# swagger_client.V1Api

All URIs are relative to *https://api.imperva.com/ip-reputation*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_ip_reputation**](V1Api.md#get_ip_reputation) | **GET** /v1/reputation | Retrieve reputation intelligence data for a specified IP.

# **get_ip_reputation**
> IPDataApi get_ip_reputation(ip)

Retrieve reputation intelligence data for a specified IP.

Use this operation to get Reputation Intelligence details on a specified IP address.

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
api_instance = swagger_client.V1Api(swagger_client.ApiClient(configuration))
ip = 'ip_example' # str | Unique IP address. Only IPv4 addresses are supported.

try:
    # Retrieve reputation intelligence data for a specified IP.
    api_response = api_instance.get_ip_reputation(ip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_ip_reputation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip** | **str**| Unique IP address. Only IPv4 addresses are supported. | 

### Return type

[**IPDataApi**](IPDataApi.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

