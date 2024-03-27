# swagger_client.TimelineApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_logins_timeline**](TimelineApi.md#get_logins_timeline) | **POST** /v2/sites/{siteId}/timeline | Get the login timeline for a site.

# **get_logins_timeline**
> LoginsTimeline get_logins_timeline(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get the login timeline for a site.

Pass an endpoint id in order to get the timeline just for that one. If you don't pass an endpoint id, all configured ids will be sent as one \"TOTAL\" (summed together). A login timeline represents ongoing login requests made to your site over a time period. Each data point represents the number of logins attempted for that time bucket (each 5 minutes).

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
api_instance = swagger_client.TimelineApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get the login timeline for a site.
    api_response = api_instance.get_logins_timeline(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimelineApi->get_logins_timeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**LoginsTimeline**](LoginsTimeline.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

