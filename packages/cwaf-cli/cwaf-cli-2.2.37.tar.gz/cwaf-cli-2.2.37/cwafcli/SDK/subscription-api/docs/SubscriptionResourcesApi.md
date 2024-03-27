# swagger_client.SubscriptionResourcesApi

All URIs are relative to *https://api.imperva.com/subscription-management*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_subscription_resources**](SubscriptionResourcesApi.md#get_subscription_resources) | **GET** /v3/subscriptions/{subscription-id}/resources | Retrieve a subscription&#x27;s resources

# **get_subscription_resources**
> ImpervaApiBodyListSubscriptionResourceDto get_subscription_resources(caid, subscription_id)

Retrieve a subscription's resources

Retrieve a subscription's resources by a subscription ID.

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
api_instance = swagger_client.SubscriptionResourcesApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
subscription_id = 'subscription_id_example' # str | Subscription ID. Unique identifier of the subscription. Run the GET /v3/subscriptions API to locate the value of the ‘id’ parameter in the response.

try:
    # Retrieve a subscription's resources
    api_response = api_instance.get_subscription_resources(caid, subscription_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionResourcesApi->get_subscription_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **subscription_id** | **str**| Subscription ID. Unique identifier of the subscription. Run the GET /v3/subscriptions API to locate the value of the ‘id’ parameter in the response. | 

### Return type

[**ImpervaApiBodyListSubscriptionResourceDto**](ImpervaApiBodyListSubscriptionResourceDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

