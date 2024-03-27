# swagger_client.SubscriptionsApi

All URIs are relative to *https://api.imperva.com/subscription-management*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get**](SubscriptionsApi.md#get) | **GET** /v3/subscriptions/{subscription-id} | Retrieve a subscription
[**get_all**](SubscriptionsApi.md#get_all) | **GET** /v3/subscriptions | Retrieve all subscriptions

# **get**
> ImpervaApiBodySubscription get(caid, subscription_id, status_list=status_list)

Retrieve a subscription

Retrieve subscription details by a subscription ID.

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
api_instance = swagger_client.SubscriptionsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
subscription_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Subscription ID. Unique identifier of the subscription. Run the GET /v3/subscriptions API to locate the value of the ‘id’ parameter in the response.
status_list = ['[\"ACTIVE\",\"CANCELLED\",\"MIGRATION_INITIATED\",\"EXPIRED\"]'] # list[str] | Subscription status to return. (optional) (default to ["ACTIVE","CANCELLED","MIGRATION_INITIATED","EXPIRED"])

try:
    # Retrieve a subscription
    api_response = api_instance.get(caid, subscription_id, status_list=status_list)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionsApi->get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **subscription_id** | [**str**](.md)| Subscription ID. Unique identifier of the subscription. Run the GET /v3/subscriptions API to locate the value of the ‘id’ parameter in the response. | 
 **status_list** | [**list[str]**](str.md)| Subscription status to return. | [optional] [default to [&quot;ACTIVE&quot;,&quot;CANCELLED&quot;,&quot;MIGRATION_INITIATED&quot;,&quot;EXPIRED&quot;]]

### Return type

[**ImpervaApiBodySubscription**](ImpervaApiBodySubscription.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all**
> ImpervaApiBodyListSubscription get_all(caid, status_list=status_list)

Retrieve all subscriptions

Retrieve all subscription details of an account.

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
api_instance = swagger_client.SubscriptionsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
status_list = ['[\"ACTIVE\",\"CANCELLED\",\"MIGRATION_INITIATED\",\"EXPIRED\"]'] # list[str] | Subscription status to return. (optional) (default to ["ACTIVE","CANCELLED","MIGRATION_INITIATED","EXPIRED"])

try:
    # Retrieve all subscriptions
    api_response = api_instance.get_all(caid, status_list=status_list)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubscriptionsApi->get_all: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **status_list** | [**list[str]**](str.md)| Subscription status to return. | [optional] [default to [&quot;ACTIVE&quot;,&quot;CANCELLED&quot;,&quot;MIGRATION_INITIATED&quot;,&quot;EXPIRED&quot;]]

### Return type

[**ImpervaApiBodyListSubscription**](ImpervaApiBodyListSubscription.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

