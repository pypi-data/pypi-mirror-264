# swagger_client.MitigationApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_mitigation_config**](MitigationApi.md#get_mitigation_config) | **GET** /v2/sites/{siteId}/mitigation | Get the mitigation configuration for a specific site.
[**set_mitigation_config_for_endpoints**](MitigationApi.md#set_mitigation_config_for_endpoints) | **POST** /v2/sites/{siteId}/mitigation | Change the mitigation configuration for a specific site and endpoint. The actions (low, medium, high) should all be in UPPER CASE.

# **get_mitigation_config**
> list[MitigationRequest] get_mitigation_config(site_id, caid=caid, endpoint_ids=endpoint_ids)

Get the mitigation configuration for a specific site.

Pass a comma-separated string of endpoint ids in order to get the mitigation configuration just for those ones. If not passed, this API will retrieve the mitigation configuration for all endpoints

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
api_instance = swagger_client.MitigationApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_ids = 'endpoint_ids_example' # str | Comma-separated list of endpoint ids (optional)

try:
    # Get the mitigation configuration for a specific site.
    api_response = api_instance.get_mitigation_config(site_id, caid=caid, endpoint_ids=endpoint_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MitigationApi->get_mitigation_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_ids** | **str**| Comma-separated list of endpoint ids | [optional] 

### Return type

[**list[MitigationRequest]**](MitigationRequest.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_mitigation_config_for_endpoints**
> set_mitigation_config_for_endpoints(body, site_id, caid=caid)

Change the mitigation configuration for a specific site and endpoint. The actions (low, medium, high) should all be in UPPER CASE.

Possible values for actions are: NONE, CAPTCHA, BLOCK, TARPIT.

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
api_instance = swagger_client.MitigationApi(swagger_client.ApiClient(configuration))
body = [swagger_client.MitigationRequest()] # list[MitigationRequest] | Specify endpoint ID and mitigation actions list
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Change the mitigation configuration for a specific site and endpoint. The actions (low, medium, high) should all be in UPPER CASE.
    api_instance.set_mitigation_config_for_endpoints(body, site_id, caid=caid)
except ApiException as e:
    print("Exception when calling MitigationApi->set_mitigation_config_for_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[MitigationRequest]**](MitigationRequest.md)| Specify endpoint ID and mitigation actions list | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

