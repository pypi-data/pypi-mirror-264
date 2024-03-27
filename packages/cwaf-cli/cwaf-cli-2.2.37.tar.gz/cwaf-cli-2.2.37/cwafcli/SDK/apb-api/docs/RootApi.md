# swagger_client.RootApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_get**](RootApi.md#v1_get) | **GET** /v1/ | Retrieve the authenticated Account&#x27;s ID

# **v1_get**
> InlineResponse200 v1_get(caid=caid)

Retrieve the authenticated Account's ID

Call this endpoint to retreive an Account ID. The Account is identified by the API credentials. This endpoint is only meant to give the Account ID. Once you have that there is no need to use this endpoint. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.RootApi(swagger_client.ApiClient(configuration))
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the authenticated Account's ID
    api_response = api_instance.v1_get(caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RootApi->v1_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

