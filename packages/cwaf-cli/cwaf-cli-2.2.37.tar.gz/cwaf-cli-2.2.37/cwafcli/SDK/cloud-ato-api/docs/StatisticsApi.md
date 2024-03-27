# swagger_client.StatisticsApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_stats**](StatisticsApi.md#get_all_stats) | **POST** /v2/sites/{siteId}/stats | Get all stats - top stats and unique users stats.

# **get_all_stats**
> AllStats get_all_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get all stats - top stats and unique users stats.

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.StatisticsApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get all stats - top stats and unique users stats.
    api_response = api_instance.get_all_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatisticsApi->get_all_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**AllStats**](AllStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

