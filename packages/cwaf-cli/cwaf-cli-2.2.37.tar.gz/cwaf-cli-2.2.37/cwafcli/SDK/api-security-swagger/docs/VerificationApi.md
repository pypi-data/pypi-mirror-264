# swagger_client.VerificationApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_action**](VerificationApi.md#delete_action) | **DELETE** /v2/shift-left/actions/{actionId} | Delete an action
[**download_results**](VerificationApi.md#download_results) | **GET** /v2/shift-left/actions/{actionId}/actionType/{actionTypeId} | Download reports
[**get_action_types**](VerificationApi.md#get_action_types) | **GET** /v2/shift-left/actions/action-types | Retrieve all action types for an account
[**get_actions**](VerificationApi.md#get_actions) | **GET** /v2/shift-left/actions | Retrieve all actions for an account
[**upload_discovered_hosts_spec_files**](VerificationApi.md#upload_discovered_hosts_spec_files) | **POST** /v2/shift-left/files/discovery | Uploads discovered APIs
[**upload_file**](VerificationApi.md#upload_file) | **POST** /v2/shift-left/files/oas | Upload an OAS file

# **delete_action**
> delete_action(action_id)

Delete an action

Deletes a specified action from the account.

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
api_instance = swagger_client.VerificationApi(swagger_client.ApiClient(configuration))
action_id = 789 # int | The ActionId

try:
    # Delete an action
    api_instance.delete_action(action_id)
except ApiException as e:
    print("Exception when calling VerificationApi->delete_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **action_id** | **int**| The ActionId | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_results**
> download_results(action_id, action_type_id)

Download reports

Downloads the requested reports for a specified action

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
api_instance = swagger_client.VerificationApi(swagger_client.ApiClient(configuration))
action_id = 789 # int | Action Id
action_type_id = 789 # int | Action Type Id

try:
    # Download reports
    api_instance.download_results(action_id, action_type_id)
except ApiException as e:
    print("Exception when calling VerificationApi->download_results: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **action_id** | **int**| Action Id | 
 **action_type_id** | **int**| Action Type Id | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_action_types**
> GetActionTypesResponse get_action_types()

Retrieve all action types for an account

Retrieves details of all action types for the account

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
api_instance = swagger_client.VerificationApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve all action types for an account
    api_response = api_instance.get_action_types()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VerificationApi->get_action_types: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetActionTypesResponse**](GetActionTypesResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_actions**
> GetActionsResponse get_actions()

Retrieve all actions for an account

Retrieves details of all actions for the account

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
api_instance = swagger_client.VerificationApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve all actions for an account
    api_response = api_instance.get_actions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VerificationApi->get_actions: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetActionsResponse**](GetActionsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_discovered_hosts_spec_files**
> UploadFileSuccessResponse upload_discovered_hosts_spec_files(body=body)

Uploads discovered APIs

Uploads the OAS file generated by the Discovery engine which contains discovered APIs for a selected host

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
api_instance = swagger_client.VerificationApi(swagger_client.ApiClient(configuration))
body = 'body_example' # str | Selected host ids (optional)

try:
    # Uploads discovered APIs
    api_response = api_instance.upload_discovered_hosts_spec_files(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VerificationApi->upload_discovered_hosts_spec_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**str**](str.md)| Selected host ids | [optional] 

### Return type

[**UploadFileSuccessResponse**](UploadFileSuccessResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**
> UploadFileSuccessResponse upload_file(action_types=action_types, file=file)

Upload an OAS file

Uploads an OAS file manually.

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
api_instance = swagger_client.VerificationApi(swagger_client.ApiClient(configuration))
action_types = 'action_types_example' # str |  (optional)
file = 'file_example' # str |  (optional)

try:
    # Upload an OAS file
    api_response = api_instance.upload_file(action_types=action_types, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VerificationApi->upload_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **action_types** | **str**|  | [optional] 
 **file** | **str**|  | [optional] 

### Return type

[**UploadFileSuccessResponse**](UploadFileSuccessResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

