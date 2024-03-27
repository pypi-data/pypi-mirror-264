# swagger_client.EncryptionkeyApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_domain_domain_id_encryptionkey_get**](EncryptionkeyApi.md#v1_domain_domain_id_encryptionkey_get) | **GET** /v1/domain/{domainId}/encryptionkey | Retrieve the token encryption keys for a Domain
[**v1_domain_domain_id_encryptionkey_post**](EncryptionkeyApi.md#v1_domain_domain_id_encryptionkey_post) | **POST** /v1/domain/{domainId}/encryptionkey | Create a new encryption key for a Domain
[**v1_encryptionkey_encryptionkey_id_delete**](EncryptionkeyApi.md#v1_encryptionkey_encryptionkey_id_delete) | **DELETE** /v1/encryptionkey/{encryptionkeyId} | Delete an encryption key.

# **v1_domain_domain_id_encryptionkey_get**
> InlineResponse20012 v1_domain_domain_id_encryptionkey_get(domain_id, caid=caid)

Retrieve the token encryption keys for a Domain

The response is sorted in ascending order of time of creation. It is recommended to try the last (newest) key first and then proceeding backwards in the array, as the latest key is most likely to be active. The account configuration needs to be published for the analysis host to accept new keys. 

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
api_instance = swagger_client.EncryptionkeyApi(swagger_client.ApiClient(configuration))
domain_id = swagger_client.DomainId() # DomainId | Identifies a Domain to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the token encryption keys for a Domain
    api_response = api_instance.v1_domain_domain_id_encryptionkey_get(domain_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EncryptionkeyApi->v1_domain_domain_id_encryptionkey_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_id** | [**DomainId**](.md)| Identifies a Domain to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse20012**](InlineResponse20012.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_domain_domain_id_encryptionkey_post**
> InlineResponse2017 v1_domain_domain_id_encryptionkey_post(body, domain_id, caid=caid)

Create a new encryption key for a Domain

A new encryption key will be created even if the same encryption key material is used by another Domain.

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
api_instance = swagger_client.EncryptionkeyApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateEncryptionKeyV1() # CreateEncryptionKeyV1 | 
domain_id = swagger_client.DomainId() # DomainId | Identifies a Domain to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Create a new encryption key for a Domain
    api_response = api_instance.v1_domain_domain_id_encryptionkey_post(body, domain_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EncryptionkeyApi->v1_domain_domain_id_encryptionkey_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateEncryptionKeyV1**](CreateEncryptionKeyV1.md)|  | 
 **domain_id** | [**DomainId**](.md)| Identifies a Domain to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2017**](InlineResponse2017.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_encryptionkey_encryptionkey_id_delete**
> InlineResponse2017 v1_encryptionkey_encryptionkey_id_delete(encryptionkey_id, caid=caid)

Delete an encryption key.

Delete an encryption key for a Domain. Other domains are unaffected. 

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
api_instance = swagger_client.EncryptionkeyApi(swagger_client.ApiClient(configuration))
encryptionkey_id = swagger_client.EncryptionKeyId() # EncryptionKeyId | Identifies the Encryption Key to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Delete an encryption key.
    api_response = api_instance.v1_encryptionkey_encryptionkey_id_delete(encryptionkey_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EncryptionkeyApi->v1_encryptionkey_encryptionkey_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **encryptionkey_id** | [**EncryptionKeyId**](.md)| Identifies the Encryption Key to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2017**](InlineResponse2017.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

