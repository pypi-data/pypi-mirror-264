# swagger_client.PolicyManagementApi

All URIs are relative to *https://api.imperva.com/policies*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_if_policy_is_applied_on_asset**](PolicyManagementApi.md#check_if_policy_is_applied_on_asset) | **GET** /v2/policies/{policyId}/assets/{assetType}/{assetId} | Check whether the policy is applied on the asset
[**create_new_policy**](PolicyManagementApi.md#create_new_policy) | **POST** /v2/policies | Add a new policy or copy an existing policy
[**delete_policy**](PolicyManagementApi.md#delete_policy) | **DELETE** /v2/policies/{policyId} | Delete an existing policy
[**get_all_policies_by_account**](PolicyManagementApi.md#get_all_policies_by_account) | **GET** /v2/policies | Retrieve all policies in account
[**get_policy_by_id**](PolicyManagementApi.md#get_policy_by_id) | **GET** /v2/policies/{policyId} | Retrieve policy details
[**modify_policy**](PolicyManagementApi.md#modify_policy) | **POST** /v2/policies/{policyId} | Modify an existing policy (partial update)
[**update_policy**](PolicyManagementApi.md#update_policy) | **PUT** /v2/policies/{policyId} | Overwrite an existing policy (full update)
[**update_policy_to_single_asset**](PolicyManagementApi.md#update_policy_to_single_asset) | **PATCH** /v2/policies/{policyId}/{assetType}/{assetId} | Overwrite applied assets in a policy

# **check_if_policy_is_applied_on_asset**
> GetPolicyAssetResponse check_if_policy_is_applied_on_asset(asset_id, asset_type, policy_id, caid=caid)

Check whether the policy is applied on the asset

True if the policy is applied on the asset

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
asset_id = 789 # int | Asset ID
asset_type = 'asset_type_example' # str | The type of asset on which the policy is applied
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the check is performed for an asset that belongs to the account (A) associated with the API credentials used for authentication. To check for an asset that belongs to a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Check whether the policy is applied on the asset
    api_response = api_instance.check_if_policy_is_applied_on_asset(asset_id, asset_type, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->check_if_policy_is_applied_on_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**| Asset ID | 
 **asset_type** | **str**| The type of asset on which the policy is applied | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the check is performed for an asset that belongs to the account (A) associated with the API credentials used for authentication. To check for an asset that belongs to a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**GetPolicyAssetResponse**](GetPolicyAssetResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_policy**
> GetPolicyResponse create_new_policy(body, caid=caid, source_policy_id=source_policy_id)

Add a new policy or copy an existing policy

When copying an existing policy the body is ignored but nevertheless needs to be sent. A good approach is to send an empty JSON as the request body, e.g {}

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.PolicyDto() # PolicyDto | Policy to save. The supported format JSON
caid = 789 # int | By default, the policy is created for the account (A) associated with the API credentials used for authentication. To create the policy for a different account (an account under the account (A)), specify the account ID. (optional)
source_policy_id = 789 # int | Optional to clone full policy data (optional)

try:
    # Add a new policy or copy an existing policy
    api_response = api_instance.create_new_policy(body, caid=caid, source_policy_id=source_policy_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->create_new_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PolicyDto**](PolicyDto.md)| Policy to save. The supported format JSON | 
 **caid** | **int**| By default, the policy is created for the account (A) associated with the API credentials used for authentication. To create the policy for a different account (an account under the account (A)), specify the account ID. | [optional] 
 **source_policy_id** | **int**| Optional to clone full policy data | [optional] 

### Return type

[**GetPolicyResponse**](GetPolicyResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_policy**
> PolicyResult delete_policy(policy_id, caid=caid)

Delete an existing policy

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy is deleted for the account (A) associated with the API credentials used for authentication. To delete the policy for a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Delete an existing policy
    api_response = api_instance.delete_policy(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->delete_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy is deleted for the account (A) associated with the API credentials used for authentication. To delete the policy for a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**PolicyResult**](PolicyResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_policies_by_account**
> GetLeanPoliciesResponse get_all_policies_by_account(caid=caid, extended=extended)

Retrieve all policies in account

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
caid = 789 # int | By default, the policies are retrieved for the account (A) associated with the API credentials used for authentication. To retrieve the policies for a different account (an account under the account (A)), specify the account ID. (optional)
extended = true # bool | Optional to get full policy data. Default is false. When set to false, the response returns basic policy details such as name, ID, and policy type, according to GetLeanPoliciesResponse. This is the default value. If set to true, the response returns full policy details, including current configuration and settings, according to GetPoliciesResponse. (optional)

try:
    # Retrieve all policies in account
    api_response = api_instance.get_all_policies_by_account(caid=caid, extended=extended)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->get_all_policies_by_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| By default, the policies are retrieved for the account (A) associated with the API credentials used for authentication. To retrieve the policies for a different account (an account under the account (A)), specify the account ID. | [optional] 
 **extended** | **bool**| Optional to get full policy data. Default is false. When set to false, the response returns basic policy details such as name, ID, and policy type, according to GetLeanPoliciesResponse. This is the default value. If set to true, the response returns full policy details, including current configuration and settings, according to GetPoliciesResponse. | [optional] 

### Return type

[**GetLeanPoliciesResponse**](GetLeanPoliciesResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_policy_by_id**
> GetLeanPolicyResponse get_policy_by_id(policy_id, caid=caid, extended=extended)

Retrieve policy details

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy is retrieved for the account (A) associated with the API credentials used for authentication. To retrieve the policy for a different account (an account under the account (A)), specify the account ID. (optional)
extended = true # bool | Optional to get full policy data. Default is false. When set to false, the response returns basic policy details such as name, ID, and policy type, according to GetLeanPoliciesResponse. This is the default value. If set to true, the response returns full policy details, including current configuration and settings, according to GetPoliciesResponse. (optional)

try:
    # Retrieve policy details
    api_response = api_instance.get_policy_by_id(policy_id, caid=caid, extended=extended)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->get_policy_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy is retrieved for the account (A) associated with the API credentials used for authentication. To retrieve the policy for a different account (an account under the account (A)), specify the account ID. | [optional] 
 **extended** | **bool**| Optional to get full policy data. Default is false. When set to false, the response returns basic policy details such as name, ID, and policy type, according to GetLeanPoliciesResponse. This is the default value. If set to true, the response returns full policy details, including current configuration and settings, according to GetPoliciesResponse. | [optional] 

### Return type

[**GetLeanPolicyResponse**](GetLeanPolicyResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_policy**
> GetPolicyResponse modify_policy(body, policy_id, caid=caid)

Modify an existing policy (partial update)

When sending the content in the \"data\" attribute, it will be appended and not overwritten. When updating an existing policy settings or exceptions, the relevant id (policy settings or exception id) must be provided.

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdatePolicyDto() # UpdatePolicyDto | Policy to save. The supported format JSON
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy is updated for the account (A) associated with the API credentials used for authentication. To update the policy for a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Modify an existing policy (partial update)
    api_response = api_instance.modify_policy(body, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->modify_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdatePolicyDto**](UpdatePolicyDto.md)| Policy to save. The supported format JSON | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy is updated for the account (A) associated with the API credentials used for authentication. To update the policy for a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**GetPolicyResponse**](GetPolicyResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_policy**
> GetPolicyResponse update_policy(body, policy_id, caid=caid)

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.PolicyDto() # PolicyDto | Policy to save. The supported format JSON
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy is saved for the account (A) associated with the API credentials used for authentication. To save the policy for a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Overwrite an existing policy (full update)
    api_response = api_instance.update_policy(body, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->update_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PolicyDto**](PolicyDto.md)| Policy to save. The supported format JSON | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy is saved for the account (A) associated with the API credentials used for authentication. To save the policy for a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**GetPolicyResponse**](GetPolicyResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_policy_to_single_asset**
> AssetResult update_policy_to_single_asset(asset_id, asset_type, policy_id, caid=caid)

Overwrite applied assets in a policy

Applies a single policy to a single asset and removes the previously applied assets from the policy.

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
api_instance = swagger_client.PolicyManagementApi(swagger_client.ApiClient(configuration))
asset_id = 789 # int | Asset ID
asset_type = 'asset_type_example' # str | The type of asset on which the policy is applied
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy is applied for an asset that belongs to the account (A) associated with the API credentials used for authentication. To apply the policy for an asset that belongs to a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Overwrite applied assets in a policy
    api_response = api_instance.update_policy_to_single_asset(asset_id, asset_type, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementApi->update_policy_to_single_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**| Asset ID | 
 **asset_type** | **str**| The type of asset on which the policy is applied | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy is applied for an asset that belongs to the account (A) associated with the API credentials used for authentication. To apply the policy for an asset that belongs to a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**AssetResult**](AssetResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

