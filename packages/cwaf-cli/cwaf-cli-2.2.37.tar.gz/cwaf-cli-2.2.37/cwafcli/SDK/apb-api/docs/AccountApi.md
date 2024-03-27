# swagger_client.AccountApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_account_account_id_default_encryption_key_get**](AccountApi.md#v1_account_account_id_default_encryption_key_get) | **GET** /v1/account/{accountId}/default_encryption_key | Retrieve the default encryption key for an Account
[**v1_account_account_id_get**](AccountApi.md#v1_account_account_id_get) | **GET** /v1/account/{accountId} | Retrieve an Account

# **v1_account_account_id_default_encryption_key_get**
> InlineResponse2002 v1_account_account_id_default_encryption_key_get(account_id, caid=caid)

Retrieve the default encryption key for an Account

Retrieve the default encryption key for an Account

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
api_instance = swagger_client.AccountApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the default encryption key for an Account
    api_response = api_instance.v1_account_account_id_default_encryption_key_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountApi->v1_account_account_id_default_encryption_key_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_account_account_id_get**
> InlineResponse2001 v1_account_account_id_get(account_id, caid=caid)

Retrieve an Account

Retrieve an Account

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
api_instance = swagger_client.AccountApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve an Account
    api_response = api_instance.v1_account_account_id_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountApi->v1_account_account_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

