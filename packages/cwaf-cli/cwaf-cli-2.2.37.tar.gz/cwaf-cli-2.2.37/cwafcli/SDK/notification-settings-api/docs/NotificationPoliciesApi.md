# swagger_client.NotificationPoliciesApi

All URIs are relative to *https://api.imperva.com/notification-settings*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](NotificationPoliciesApi.md#create) | **POST** /v3/policies | Create a notification policy
[**delete**](NotificationPoliciesApi.md#delete) | **DELETE** /v3/policies/{policyId} | Delete a notification policy
[**get**](NotificationPoliciesApi.md#get) | **GET** /v3/policies/{policyId} | Retrieve a notification policy
[**get_notification_policy_lite_list**](NotificationPoliciesApi.md#get_notification_policy_lite_list) | **GET** /v3/policies/lite | Get account notification policies
[**update**](NotificationPoliciesApi.md#update) | **PUT** /v3/policies/{policyId} | Update a notification policy
[**update_non_crud_policy**](NotificationPoliciesApi.md#update_non_crud_policy) | **PUT** /v3/policy/update | Update notification policy status

# **create**
> ImpervaApiDtoNotificationPolicyFull create(body, caid=caid)

Create a notification policy

Create a notification policy for account and website activity, application security events, and network security updates.

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
api_instance = swagger_client.NotificationPoliciesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ImpervaApiDtoNotificationPolicyFull() # ImpervaApiDtoNotificationPolicyFull | 
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Create a notification policy
    api_response = api_instance.create(body, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationPoliciesApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ImpervaApiDtoNotificationPolicyFull**](ImpervaApiDtoNotificationPolicyFull.md)|  | 
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**ImpervaApiDtoNotificationPolicyFull**](ImpervaApiDtoNotificationPolicyFull.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete**
> ImpervaApiDtoNotificationPolicyFull delete(policy_id, caid=caid)

Delete a notification policy

Delete the notification policy as per the specified CAID and policy ID parameters.

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
api_instance = swagger_client.NotificationPoliciesApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Imperva ID of the policy. To retrieve the policy ID, run the GET /v3/policies/lite API.
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Delete a notification policy
    api_response = api_instance.delete(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationPoliciesApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Imperva ID of the policy. To retrieve the policy ID, run the GET /v3/policies/lite API. | 
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**ImpervaApiDtoNotificationPolicyFull**](ImpervaApiDtoNotificationPolicyFull.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get**
> ImpervaApiDtoNotificationPolicyFull get(policy_id, caid=caid)

Retrieve a notification policy

Retrieve details of a given policy according to policy ID. To retrieve the policy ID, run the GET /v3/policies/lite API.

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
api_instance = swagger_client.NotificationPoliciesApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Imperva ID of the policy. To retrieve the policy ID, run the GET /v3/policies/lite API.
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Retrieve a notification policy
    api_response = api_instance.get(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationPoliciesApi->get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Imperva ID of the policy. To retrieve the policy ID, run the GET /v3/policies/lite API. | 
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**ImpervaApiDtoNotificationPolicyFull**](ImpervaApiDtoNotificationPolicyFull.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_notification_policy_lite_list**
> ImpervaApiDtoListNotificationPolicyLite get_notification_policy_lite_list(caid=caid)

Get account notification policies

Get a summarized list of all notification policies in your account.

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
api_instance = swagger_client.NotificationPoliciesApi(swagger_client.ApiClient(configuration))
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Get account notification policies
    api_response = api_instance.get_notification_policy_lite_list(caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationPoliciesApi->get_notification_policy_lite_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**ImpervaApiDtoListNotificationPolicyLite**](ImpervaApiDtoListNotificationPolicyLite.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> ImpervaApiDtoNotificationPolicyFull update(body, policy_id, caid=caid)

Update a notification policy

Overwrite an existing policy (full update)

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
api_instance = swagger_client.NotificationPoliciesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ImpervaApiDtoNotificationPolicyFull() # ImpervaApiDtoNotificationPolicyFull | 
policy_id = 789 # int | The Imperva ID of the policy. To retrieve the policy ID, run the GET /v3/policies/lite API.
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Update a notification policy
    api_response = api_instance.update(body, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationPoliciesApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ImpervaApiDtoNotificationPolicyFull**](ImpervaApiDtoNotificationPolicyFull.md)|  | 
 **policy_id** | **int**| The Imperva ID of the policy. To retrieve the policy ID, run the GET /v3/policies/lite API. | 
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**ImpervaApiDtoNotificationPolicyFull**](ImpervaApiDtoNotificationPolicyFull.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_non_crud_policy**
> ImpervaApiDtoNotificationPolicyUpdates update_non_crud_policy(body, caid=caid)

Update notification policy status

Enable or disable a notification policy.

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
api_instance = swagger_client.NotificationPoliciesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ImpervaApiDtoNotificationPolicyUpdates() # ImpervaApiDtoNotificationPolicyUpdates | 
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Update notification policy status
    api_response = api_instance.update_non_crud_policy(body, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationPoliciesApi->update_non_crud_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ImpervaApiDtoNotificationPolicyUpdates**](ImpervaApiDtoNotificationPolicyUpdates.md)|  | 
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**ImpervaApiDtoNotificationPolicyUpdates**](ImpervaApiDtoNotificationPolicyUpdates.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

