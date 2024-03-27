# swagger_client.PolicyManagementAccountApplicationApi

All URIs are relative to *https://api.imperva.com/policies*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_available_account_to_policy**](PolicyManagementAccountApplicationApi.md#add_available_account_to_policy) | **POST** /v2/accounts/{subAccountId}/policies/{policyId} | Enables an account to access a policy
[**get_account_policy_association**](PolicyManagementAccountApplicationApi.md#get_account_policy_association) | **GET** /v3/accounts/associated-policies | Retrieve the list of default and available policies of the account
[**get_all_available_accounts_of_policy**](PolicyManagementAccountApplicationApi.md#get_all_available_accounts_of_policy) | **GET** /v2/accounts/policies/{policyId} | Retrieves the list of accounts that can access a policy
[**patch_account_policy_association**](PolicyManagementAccountApplicationApi.md#patch_account_policy_association) | **PATCH** /v3/accounts/associated-policies | Update the list of default and available policies of the account
[**put_account_policy_association**](PolicyManagementAccountApplicationApi.md#put_account_policy_association) | **PUT** /v3/accounts/associated-policies | Set the list of default and available policies of the account (full overwrite)
[**remove_available_account_from_policy**](PolicyManagementAccountApplicationApi.md#remove_available_account_from_policy) | **DELETE** /v2/accounts/{subAccountId}/policies/{policyId} | Removes access to a policy by an account
[**set_available_account_to_policy**](PolicyManagementAccountApplicationApi.md#set_available_account_to_policy) | **PUT** /v2/accounts/policies/{policyId} | Defines the list of accounts that can access a policy

# **add_available_account_to_policy**
> PolicyAccountsResult add_available_account_to_policy(policy_id, sub_account_id)

Enables an account to access a policy

Adds an account to the list of accounts that can view and manage a given policy.  If the policy is currently defined as available to all sub accounts, running this API overwrites the setting. The policy will be available to the parent account and the specified sub account only.

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Policy ID
sub_account_id = 789 # int | Sub Account Id to add to the policy

try:
    # Enables an account to access a policy
    api_response = api_instance.add_available_account_to_policy(policy_id, sub_account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->add_available_account_to_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Policy ID | 
 **sub_account_id** | **int**| Sub Account Id to add to the policy | 

### Return type

[**PolicyAccountsResult**](PolicyAccountsResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account_policy_association**
> AccountPolicyAssociationV3RequestResponse get_account_policy_association(caid=caid)

Retrieve the list of default and available policies of the account

Retrieves the account’s default polices, and all the policies that are available to the account.

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
caid = 789 # int | By default, the policies association is retrieved for the account (A) associated with the API credentials used for authentication. To retrieve the policies associated with a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Retrieve the list of default and available policies of the account
    api_response = api_instance.get_account_policy_association(caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->get_account_policy_association: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| By default, the policies association is retrieved for the account (A) associated with the API credentials used for authentication. To retrieve the policies associated with a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**AccountPolicyAssociationV3RequestResponse**](AccountPolicyAssociationV3RequestResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_available_accounts_of_policy**
> PolicyAccountsResult get_all_available_accounts_of_policy(policy_id)

Retrieves the list of accounts that can access a policy

Retrieves the IDs of accounts that can view and manage a policy

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Policy ID

try:
    # Retrieves the list of accounts that can access a policy
    api_response = api_instance.get_all_available_accounts_of_policy(policy_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->get_all_available_accounts_of_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Policy ID | 

### Return type

[**PolicyAccountsResult**](PolicyAccountsResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_account_policy_association**
> AccountPolicyAssociationV3RequestResponse patch_account_policy_association(body, caid=caid)

Update the list of default and available policies of the account

Updates the account’s default polices and updates the list of policies that are available to the account.

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
body = swagger_client.AccountPolicyAssociationV3RequestResponse() # AccountPolicyAssociationV3RequestResponse | Account policy association. Only JSON format is supported.
caid = 789 # int | By default, the policies association is set for the account (A) associated with the API credentials used for authentication. To retrieve the policies associated with a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Update the list of default and available policies of the account
    api_response = api_instance.patch_account_policy_association(body, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->patch_account_policy_association: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AccountPolicyAssociationV3RequestResponse**](AccountPolicyAssociationV3RequestResponse.md)| Account policy association. Only JSON format is supported. | 
 **caid** | **int**| By default, the policies association is set for the account (A) associated with the API credentials used for authentication. To retrieve the policies associated with a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**AccountPolicyAssociationV3RequestResponse**](AccountPolicyAssociationV3RequestResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_account_policy_association**
> AccountPolicyAssociationV3RequestResponse put_account_policy_association(body, caid=caid)

Set the list of default and available policies of the account (full overwrite)

Sets the account’s default polices, and sets the list of policies that are available to the account (full overwrite).

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
body = swagger_client.AccountPolicyAssociationV3RequestResponse() # AccountPolicyAssociationV3RequestResponse | Account policy association. Only JSON format is supported.
caid = 789 # int | By default, the policies association is set for the account (A) associated with the API credentials used for authentication. To retrieve the policies associated with a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Set the list of default and available policies of the account (full overwrite)
    api_response = api_instance.put_account_policy_association(body, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->put_account_policy_association: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AccountPolicyAssociationV3RequestResponse**](AccountPolicyAssociationV3RequestResponse.md)| Account policy association. Only JSON format is supported. | 
 **caid** | **int**| By default, the policies association is set for the account (A) associated with the API credentials used for authentication. To retrieve the policies associated with a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**AccountPolicyAssociationV3RequestResponse**](AccountPolicyAssociationV3RequestResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_available_account_from_policy**
> PolicyAccountsResult remove_available_account_from_policy(policy_id, sub_account_id)

Removes access to a policy by an account

Removes an account from the list of accounts that can view and manage a policy

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Policy ID
sub_account_id = 789 # int | Sub Account Id to remove from the policy

try:
    # Removes access to a policy by an account
    api_response = api_instance.remove_available_account_from_policy(policy_id, sub_account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->remove_available_account_from_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Policy ID | 
 **sub_account_id** | **int**| Sub Account Id to remove from the policy | 

### Return type

[**PolicyAccountsResult**](PolicyAccountsResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_available_account_to_policy**
> PolicyAccountsResult set_available_account_to_policy(body, policy_id)

Defines the list of accounts that can access a policy

Configures the list of accounts that can view and manage a policy

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
api_instance = swagger_client.PolicyManagementAccountApplicationApi(swagger_client.ApiClient(configuration))
body = [56] # list[int] | The list of account IDs that can access the policy, e.g. [123,234]
policy_id = 789 # int | The Policy ID

try:
    # Defines the list of accounts that can access a policy
    api_response = api_instance.set_available_account_to_policy(body, policy_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAccountApplicationApi->set_available_account_to_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[int]**](int.md)| The list of account IDs that can access the policy, e.g. [123,234] | 
 **policy_id** | **int**| The Policy ID | 

### Return type

[**PolicyAccountsResult**](PolicyAccountsResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

