# swagger_client.SnapshotApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_account_account_id_snapshot_get**](SnapshotApi.md#v1_account_account_id_snapshot_get) | **GET** /v1/account/{accountId}/snapshot | Retrieve the list of snapshots belonging to an Account
[**v1_account_account_id_snapshot_post**](SnapshotApi.md#v1_account_account_id_snapshot_post) | **POST** /v1/account/{accountId}/snapshot | Create a snapshot to allow a configuration rollback
[**v1_snapshot_snapshot_id_delete**](SnapshotApi.md#v1_snapshot_snapshot_id_delete) | **DELETE** /v1/snapshot/{snapshotId} | Delete a snapshot
[**v1_snapshot_snapshot_id_get**](SnapshotApi.md#v1_snapshot_snapshot_id_get) | **GET** /v1/snapshot/{snapshotId} | Retrieve a snapshot
[**v1_snapshot_snapshot_id_restore_post**](SnapshotApi.md#v1_snapshot_snapshot_id_restore_post) | **POST** /v1/snapshot/{snapshotId}/restore | Restore the account configuration to the state in the provided snapshot.

# **v1_account_account_id_snapshot_get**
> InlineResponse20010 v1_account_account_id_snapshot_get(account_id, caid=caid)

Retrieve the list of snapshots belonging to an Account

Retrieves the list of snapshots belonging to an Account. 

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
api_instance = swagger_client.SnapshotApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the list of snapshots belonging to an Account
    api_response = api_instance.v1_account_account_id_snapshot_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnapshotApi->v1_account_account_id_snapshot_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse20010**](InlineResponse20010.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_account_account_id_snapshot_post**
> InlineResponse2016 v1_account_account_id_snapshot_post(body, account_id, caid=caid)

Create a snapshot to allow a configuration rollback

The snapshot is based on the current configuration. It is recommended to publish the configuration before creating a snapshot to make sure that it only contains live configuration. 

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
api_instance = swagger_client.SnapshotApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateSnapshotV1() # CreateSnapshotV1 | 
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Create a snapshot to allow a configuration rollback
    api_response = api_instance.v1_account_account_id_snapshot_post(body, account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnapshotApi->v1_account_account_id_snapshot_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateSnapshotV1**](CreateSnapshotV1.md)|  | 
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2016**](InlineResponse2016.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_snapshot_snapshot_id_delete**
> InlineResponse2016 v1_snapshot_snapshot_id_delete(snapshot_id, caid=caid)

Delete a snapshot

Deletes a snapshot.

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
api_instance = swagger_client.SnapshotApi(swagger_client.ApiClient(configuration))
snapshot_id = swagger_client.SnapshotId() # SnapshotId | Identifies a Snapshot to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Delete a snapshot
    api_response = api_instance.v1_snapshot_snapshot_id_delete(snapshot_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnapshotApi->v1_snapshot_snapshot_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | [**SnapshotId**](.md)| Identifies a Snapshot to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2016**](InlineResponse2016.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_snapshot_snapshot_id_get**
> InlineResponse2016 v1_snapshot_snapshot_id_get(snapshot_id, caid=caid)

Retrieve a snapshot

Retrieves a snapshot.

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
api_instance = swagger_client.SnapshotApi(swagger_client.ApiClient(configuration))
snapshot_id = swagger_client.SnapshotId() # SnapshotId | Identifies a Snapshot to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve a snapshot
    api_response = api_instance.v1_snapshot_snapshot_id_get(snapshot_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnapshotApi->v1_snapshot_snapshot_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | [**SnapshotId**](.md)| Identifies a Snapshot to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2016**](InlineResponse2016.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_snapshot_snapshot_id_restore_post**
> InlineResponse2016 v1_snapshot_snapshot_id_restore_post(snapshot_id, caid=caid)

Restore the account configuration to the state in the provided snapshot.

Restores the account configuration to the state in the provided snapshot. The restored configuration needs to be published to take effect. A snapshot can not be restored if encryption keys for a currently existing domain have changed since the snapshot was created. It can also not be restored if a domain is connected to a CloudWAF website that has been offboarded or moved to a different account. 

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
api_instance = swagger_client.SnapshotApi(swagger_client.ApiClient(configuration))
snapshot_id = swagger_client.SnapshotId() # SnapshotId | Identifies a Snapshot to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Restore the account configuration to the state in the provided snapshot.
    api_response = api_instance.v1_snapshot_snapshot_id_restore_post(snapshot_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnapshotApi->v1_snapshot_snapshot_id_restore_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | [**SnapshotId**](.md)| Identifies a Snapshot to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2016**](InlineResponse2016.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

