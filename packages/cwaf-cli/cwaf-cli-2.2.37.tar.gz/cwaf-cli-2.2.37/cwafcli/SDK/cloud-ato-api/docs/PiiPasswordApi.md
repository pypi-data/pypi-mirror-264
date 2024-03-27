# swagger_client.PiiPasswordApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_pii_password**](PiiPasswordApi.md#delete_pii_password) | **DELETE** /v2/sites/{siteId}/pii-password | Reset the PII password
[**set_pii_password**](PiiPasswordApi.md#set_pii_password) | **POST** /v2/sites/{siteId}/pii-password | Update the PII password

# **delete_pii_password**
> delete_pii_password(site_id, caid=caid)

Reset the PII password

Reset the PII password for the current account. This will delete the currently configured PII password and you will have to configure a new one before being able to see plaintext usernames. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.PiiPasswordApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Reset the PII password
    api_instance.delete_pii_password(site_id, caid=caid)
except ApiException as e:
    print("Exception when calling PiiPasswordApi->delete_pii_password: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_pii_password**
> set_pii_password(body, site_id, caid=caid)

Update the PII password

Update the PII password for the current account. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.PiiPasswordApi(swagger_client.ApiClient(configuration))
body = swagger_client.PiiConfigPassword() # PiiConfigPassword | Pii Password to update
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Update the PII password
    api_instance.set_pii_password(body, site_id, caid=caid)
except ApiException as e:
    print("Exception when calling PiiPasswordApi->set_pii_password: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PiiConfigPassword**](PiiConfigPassword.md)| Pii Password to update | 
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

