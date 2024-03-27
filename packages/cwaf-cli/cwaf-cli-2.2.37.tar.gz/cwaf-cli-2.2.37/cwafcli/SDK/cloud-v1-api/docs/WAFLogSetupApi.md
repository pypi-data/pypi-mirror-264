# swagger_client.WAFLogSetupApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate**](WAFLogSetupApi.md#activate) | **POST** /api/prov/v1/waf-log-setup/activate | Activate WAF Logs
[**change_status**](WAFLogSetupApi.md#change_status) | **POST** /api/prov/v1/waf-log-setup/change/status | Change logs collector configuration status

# **activate**
> ApiResultWAFLogSetupActivate activate(account_id)

Activate WAF Logs

Use this operation to activate WAF Logs

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
api_instance = swagger_client.WAFLogSetupApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | Numeric identifier of the account to operate on.

try:
    # Activate WAF Logs
    api_response = api_instance.activate(account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WAFLogSetupApi->activate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| Numeric identifier of the account to operate on. | 

### Return type

[**ApiResultWAFLogSetupActivate**](ApiResultWAFLogSetupActivate.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **change_status**
> ApiResult change_status(account_id, config_id, logs_config_new_status)

Change logs collector configuration status

Change the status of the Logs Collector configuration.

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
api_instance = swagger_client.WAFLogSetupApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | Numeric identifier of the account to operate on.
config_id = 789 # int | The Logs Collector configuration identifier.
logs_config_new_status = 'logs_config_new_status_example' # str | The new configuration status of the Logs Collector. Possible values: ACTIVE, SUSPENDED

try:
    # Change logs collector configuration status
    api_response = api_instance.change_status(account_id, config_id, logs_config_new_status)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WAFLogSetupApi->change_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| Numeric identifier of the account to operate on. | 
 **config_id** | **int**| The Logs Collector configuration identifier. | 
 **logs_config_new_status** | **str**| The new configuration status of the Logs Collector. Possible values: ACTIVE, SUSPENDED | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

