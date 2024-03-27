# swagger_client.PolicyApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_account_account_id_policy_get**](PolicyApi.md#v1_account_account_id_policy_get) | **GET** /v1/account/{accountId}/policy | Retrieve the list of Policies belonging to the Account
[**v1_account_account_id_policy_post**](PolicyApi.md#v1_account_account_id_policy_post) | **POST** /v1/account/{accountId}/policy | Create a new Policy
[**v1_policy_policy_id_delete**](PolicyApi.md#v1_policy_policy_id_delete) | **DELETE** /v1/policy/{policyId} | Delete a Policy
[**v1_policy_policy_id_environmental_parameters_get**](PolicyApi.md#v1_policy_policy_id_environmental_parameters_get) | **GET** /v1/policy/{policyId}/environmental_parameters | Retrieve all environmental parameters used in a Policy
[**v1_policy_policy_id_get**](PolicyApi.md#v1_policy_policy_id_get) | **GET** /v1/policy/{policyId} | Retrieve a Policy
[**v1_policy_policy_id_put**](PolicyApi.md#v1_policy_policy_id_put) | **PUT** /v1/policy/{policyId} | Update a Policy

# **v1_account_account_id_policy_get**
> InlineResponse2006 v1_account_account_id_policy_get(account_id, caid=caid)

Retrieve the list of Policies belonging to the Account

Retrieves the list of Policies belonging to the Account.

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
api_instance = swagger_client.PolicyApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the list of Policies belonging to the Account
    api_response = api_instance.v1_account_account_id_policy_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyApi->v1_account_account_id_policy_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2006**](InlineResponse2006.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_account_account_id_policy_post**
> InlineResponse2013 v1_account_account_id_policy_post(body, account_id, caid=caid)

Create a new Policy

Creates a new Policy.

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
api_instance = swagger_client.PolicyApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreatePolicyV1() # CreatePolicyV1 | 
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Create a new Policy
    api_response = api_instance.v1_account_account_id_policy_post(body, account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyApi->v1_account_account_id_policy_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreatePolicyV1**](CreatePolicyV1.md)|  | 
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2013**](InlineResponse2013.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_policy_policy_id_delete**
> InlineResponse2013 v1_policy_policy_id_delete(policy_id, caid=caid)

Delete a Policy

Deletes a policy

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
api_instance = swagger_client.PolicyApi(swagger_client.ApiClient(configuration))
policy_id = swagger_client.PolicyId() # PolicyId | Identifies a Policy to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Delete a Policy
    api_response = api_instance.v1_policy_policy_id_delete(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyApi->v1_policy_policy_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | [**PolicyId**](.md)| Identifies a Policy to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2013**](InlineResponse2013.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_policy_policy_id_environmental_parameters_get**
> InlineResponse20011 v1_policy_policy_id_environmental_parameters_get(policy_id, caid=caid)

Retrieve all environmental parameters used in a Policy

Retrieve all environmental parameters used in a Policy

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
api_instance = swagger_client.PolicyApi(swagger_client.ApiClient(configuration))
policy_id = swagger_client.PolicyId() # PolicyId | Identifies a Policy to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve all environmental parameters used in a Policy
    api_response = api_instance.v1_policy_policy_id_environmental_parameters_get(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyApi->v1_policy_policy_id_environmental_parameters_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | [**PolicyId**](.md)| Identifies a Policy to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse20011**](InlineResponse20011.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_policy_policy_id_get**
> InlineResponse2013 v1_policy_policy_id_get(policy_id, caid=caid)

Retrieve a Policy

Retrieve a Policy

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
api_instance = swagger_client.PolicyApi(swagger_client.ApiClient(configuration))
policy_id = swagger_client.PolicyId() # PolicyId | Identifies a Policy to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve a Policy
    api_response = api_instance.v1_policy_policy_id_get(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyApi->v1_policy_policy_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | [**PolicyId**](.md)| Identifies a Policy to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2013**](InlineResponse2013.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_policy_policy_id_put**
> InlineResponse2013 v1_policy_policy_id_put(body, policy_id, caid=caid)

Update a Policy

Replaces a Policy resource with the given representation.

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
api_instance = swagger_client.PolicyApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdatePolicyV1() # UpdatePolicyV1 | 
policy_id = swagger_client.PolicyId() # PolicyId | Identifies a Policy to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Update a Policy
    api_response = api_instance.v1_policy_policy_id_put(body, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyApi->v1_policy_policy_id_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdatePolicyV1**](UpdatePolicyV1.md)|  | 
 **policy_id** | [**PolicyId**](.md)| Identifies a Policy to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2013**](InlineResponse2013.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

