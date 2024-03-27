# swagger_client.PolicyManagementAssetApplicationApi

All URIs are relative to *https://api.imperva.com/policies*

Method | HTTP request | Description
------------- | ------------- | -------------
[**apply_asset_to_policy**](PolicyManagementAssetApplicationApi.md#apply_asset_to_policy) | **POST** /v2/assets/{assetType}/{assetId}/policies/{policyId} | Apply a single policy to a single asset
[**get_all_asset_of_policy**](PolicyManagementAssetApplicationApi.md#get_all_asset_of_policy) | **GET** /v2/assets/policies/{policyId} | Retrieve assets to which policy is applied
[**get_all_policies_of_asset**](PolicyManagementAssetApplicationApi.md#get_all_policies_of_asset) | **GET** /v2/assets/{assetType}/{assetId}/policies | Retrieve all policies applied to an asset
[**un_apply_policy_on_asset**](PolicyManagementAssetApplicationApi.md#un_apply_policy_on_asset) | **DELETE** /v2/assets/{assetType}/{assetId}/policies/{policyId} | Remove policy from asset
[**update_asset_with_single_policy**](PolicyManagementAssetApplicationApi.md#update_asset_with_single_policy) | **PUT** /v2/assets/{assetType}/{assetId}/policies/{policyId} | Overwrite policies assigned to a single asset

# **apply_asset_to_policy**
> GetAssetsResponse apply_asset_to_policy(asset_id, asset_type, policy_id, caid=caid)

Apply a single policy to a single asset

Applies a policy to an asset. Policies already assigned to the asset are not modified. A website must have exactly one WAF Rules policy applied to it

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
api_instance = swagger_client.PolicyManagementAssetApplicationApi(swagger_client.ApiClient(configuration))
asset_id = 789 # int | Asset ID to add to policy
asset_type = 'asset_type_example' # str | The type of asset on which the policy is applied
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the Asset should belong to the account (A) associated with the API credentials used for authentication. To assign an asset of a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Apply a single policy to a single asset
    api_response = api_instance.apply_asset_to_policy(asset_id, asset_type, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAssetApplicationApi->apply_asset_to_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**| Asset ID to add to policy | 
 **asset_type** | **str**| The type of asset on which the policy is applied | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the Asset should belong to the account (A) associated with the API credentials used for authentication. To assign an asset of a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**GetAssetsResponse**](GetAssetsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_asset_of_policy**
> GetAssetsResponse get_all_asset_of_policy(policy_id, caid=caid)

Retrieve assets to which policy is applied

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
api_instance = swagger_client.PolicyManagementAssetApplicationApi(swagger_client.ApiClient(configuration))
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy should belong to the account (A) associated with the API credentials used for authentication. To get the assets for a policy of a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Retrieve assets to which policy is applied
    api_response = api_instance.get_all_asset_of_policy(policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAssetApplicationApi->get_all_asset_of_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy should belong to the account (A) associated with the API credentials used for authentication. To get the assets for a policy of a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**GetAssetsResponse**](GetAssetsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_policies_of_asset**
> GetLeanPoliciesResponse get_all_policies_of_asset(asset_id, asset_type, extended=extended)

Retrieve all policies applied to an asset

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
api_instance = swagger_client.PolicyManagementAssetApplicationApi(swagger_client.ApiClient(configuration))
asset_id = 789 # int | The Asset ID
asset_type = 'asset_type_example' # str | The type of asset on which the policy is applied
extended = true # bool | Optional to get full policy data. Default is false. When set to false, the response returns basic policy details such as name, ID, and policy type, according to GetLeanPoliciesResponse. This is the default value. If set to true, the response returns full policy details, including current configuration and settings, according to GetPoliciesResponse. (optional)

try:
    # Retrieve all policies applied to an asset
    api_response = api_instance.get_all_policies_of_asset(asset_id, asset_type, extended=extended)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAssetApplicationApi->get_all_policies_of_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**| The Asset ID | 
 **asset_type** | **str**| The type of asset on which the policy is applied | 
 **extended** | **bool**| Optional to get full policy data. Default is false. When set to false, the response returns basic policy details such as name, ID, and policy type, according to GetLeanPoliciesResponse. This is the default value. If set to true, the response returns full policy details, including current configuration and settings, according to GetPoliciesResponse. | [optional] 

### Return type

[**GetLeanPoliciesResponse**](GetLeanPoliciesResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **un_apply_policy_on_asset**
> PolicyAssetMappingResult un_apply_policy_on_asset(asset_id, asset_type, policy_id, caid=caid)

Remove policy from asset

If you remove a WAF Rules policy from a website, the account’s default policy is automatically re-applied to the website.

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
api_instance = swagger_client.PolicyManagementAssetApplicationApi(swagger_client.ApiClient(configuration))
asset_id = 789 # int | Asset ID to remove
asset_type = 'asset_type_example' # str | Asset type to remove
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy should belong to the account (A) associated with the API credentials used for authentication. To unapply a policy for a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Remove policy from asset
    api_response = api_instance.un_apply_policy_on_asset(asset_id, asset_type, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAssetApplicationApi->un_apply_policy_on_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**| Asset ID to remove | 
 **asset_type** | **str**| Asset type to remove | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy should belong to the account (A) associated with the API credentials used for authentication. To unapply a policy for a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**PolicyAssetMappingResult**](PolicyAssetMappingResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_asset_with_single_policy**
> PolicyDtoResult update_asset_with_single_policy(asset_id, asset_type, policy_id, caid=caid)

Overwrite policies assigned to a single asset

Applies a single policy to a single asset and removes previously assigned policies. If you apply a WAF Rules policy to a website, it replaces the policy that is currently applied. Since this API is removing all other policies but the one provided, it can be only applied to WAF Rules policies

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
api_instance = swagger_client.PolicyManagementAssetApplicationApi(swagger_client.ApiClient(configuration))
asset_id = 789 # int | Asset Id
asset_type = 'asset_type_example' # str | The type of asset on which the policy is applied
policy_id = 789 # int | The Policy ID
caid = 789 # int | By default, the policy should belong to the account (A) associated with the API credentials used for authentication. To update a policy for a different account (an account under the account (A)), specify the account ID. (optional)

try:
    # Overwrite policies assigned to a single asset
    api_response = api_instance.update_asset_with_single_policy(asset_id, asset_type, policy_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PolicyManagementAssetApplicationApi->update_asset_with_single_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **int**| Asset Id | 
 **asset_type** | **str**| The type of asset on which the policy is applied | 
 **policy_id** | **int**| The Policy ID | 
 **caid** | **int**| By default, the policy should belong to the account (A) associated with the API credentials used for authentication. To update a policy for a different account (an account under the account (A)), specify the account ID. | [optional] 

### Return type

[**PolicyDtoResult**](PolicyDtoResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

