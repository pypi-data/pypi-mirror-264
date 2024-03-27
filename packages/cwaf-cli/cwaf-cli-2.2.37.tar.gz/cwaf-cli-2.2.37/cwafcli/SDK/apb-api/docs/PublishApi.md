# swagger_client.PublishApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_account_account_id_publish_latest_successful_get**](PublishApi.md#v1_account_account_id_publish_latest_successful_get) | **GET** /v1/account/{accountId}/publish/latest_successful | Gets the latest successful Publish for the Account
[**v1_preflight_preflight_id_publish_post**](PublishApi.md#v1_preflight_preflight_id_publish_post) | **POST** /v1/preflight/{preflightId}/publish | Publishes a preflight
[**v1_publish_publish_id_get**](PublishApi.md#v1_publish_publish_id_get) | **GET** /v1/publish/{publishId} | Retrieve publish information

# **v1_account_account_id_publish_latest_successful_get**
> InlineResponse2009 v1_account_account_id_publish_latest_successful_get(account_id, caid=caid)

Gets the latest successful Publish for the Account

Gets the latest successful Publish for the Account. If the account has never been successfully published this endpoint responds with Not Found. 

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
api_instance = swagger_client.PublishApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Gets the latest successful Publish for the Account
    api_response = api_instance.v1_account_account_id_publish_latest_successful_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublishApi->v1_account_account_id_publish_latest_successful_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2009**](InlineResponse2009.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_preflight_preflight_id_publish_post**
> InlineResponse2018 v1_preflight_preflight_id_publish_post(preflight_id, caid=caid)

Publishes a preflight

Publishes the account configuration snapshot contained in the preflight to the analysis host. 

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
api_instance = swagger_client.PublishApi(swagger_client.ApiClient(configuration))
preflight_id = swagger_client.PreflightId() # PreflightId | Identifies a Preflight to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Publishes a preflight
    api_response = api_instance.v1_preflight_preflight_id_publish_post(preflight_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublishApi->v1_preflight_preflight_id_publish_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **preflight_id** | [**PreflightId**](.md)| Identifies a Preflight to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2018**](InlineResponse2018.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_publish_publish_id_get**
> InlineResponse2018 v1_publish_publish_id_get(publish_id, caid=caid)

Retrieve publish information

Provides information about a published preflight. 

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
api_instance = swagger_client.PublishApi(swagger_client.ApiClient(configuration))
publish_id = swagger_client.PublishId() # PublishId | Identifies a Publish to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve publish information
    api_response = api_instance.v1_publish_publish_id_get(publish_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublishApi->v1_publish_publish_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **publish_id** | [**PublishId**](.md)| Identifies a Publish to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2018**](InlineResponse2018.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

