# swagger_client.SSLSettingsApi

All URIs are relative to *https://api.imperva.com/certificates-ui*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_domain_to_ssl_validation_delegation_settings**](SSLSettingsApi.md#add_domain_to_ssl_validation_delegation_settings) | **POST** /v3/account/ssl-settings/delegation/domain/{domain} | Add domain to the SSL validation delegation settings
[**delete_ssl_validation_delegation_settings**](SSLSettingsApi.md#delete_ssl_validation_delegation_settings) | **DELETE** /v3/account/ssl-settings | Reset SSL settings to default
[**get_ssl_validation_delegation_settings**](SSLSettingsApi.md#get_ssl_validation_delegation_settings) | **GET** /v3/account/ssl-settings | Get account SSL settings
[**patch_ssl_validation_delegation_settings**](SSLSettingsApi.md#patch_ssl_validation_delegation_settings) | **PATCH** /v3/account/ssl-settings | Modify SSL settings (partial update)
[**removed_domain_to_ssl_validation_delegation_settings**](SSLSettingsApi.md#removed_domain_to_ssl_validation_delegation_settings) | **DELETE** /v3/account/ssl-settings/delegation/domain/{domainId} | Remove domain from the SSL validation delegation settings
[**update_ssl_validation_delegation_settings**](SSLSettingsApi.md#update_ssl_validation_delegation_settings) | **POST** /v3/account/ssl-settings | Overwrite SSL settings (full update)
[**verify_domain_to_ssl_validation_delegation_settings**](SSLSettingsApi.md#verify_domain_to_ssl_validation_delegation_settings) | **POST** /v3/account/ssl-settings/delegation/domain/{domainId}/status | Check the configuration status of a domain that appears in the domain delegation list

# **add_domain_to_ssl_validation_delegation_settings**
> AccountSSLSettingsResponseDto add_domain_to_ssl_validation_delegation_settings(domain)

Add domain to the SSL validation delegation settings

Add domain to the SSL validation delegation settings of your account. Delegating a domain enables Imperva to perform domain ownership validation on your behalf during website onboarding and certificate renewal. 

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))
domain = 'domain_example' # str | 

try:
    # Add domain to the SSL validation delegation settings
    api_response = api_instance.add_domain_to_ssl_validation_delegation_settings(domain)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->add_domain_to_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain** | **str**|  | 

### Return type

[**AccountSSLSettingsResponseDto**](AccountSSLSettingsResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ssl_validation_delegation_settings**
> AccountSSLSettingsResponseDto delete_ssl_validation_delegation_settings()

Reset SSL settings to default

Resets SSL settings for your account to the default values.

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Reset SSL settings to default
    api_response = api_instance.delete_ssl_validation_delegation_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->delete_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AccountSSLSettingsResponseDto**](AccountSSLSettingsResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ssl_validation_delegation_settings**
> AccountSSLSettingsResponseDto get_ssl_validation_delegation_settings()

Get account SSL settings

Get SSL settings for your account.

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Get account SSL settings
    api_response = api_instance.get_ssl_validation_delegation_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->get_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AccountSSLSettingsResponseDto**](AccountSSLSettingsResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_ssl_validation_delegation_settings**
> AccountSSLSettingsResponseDto patch_ssl_validation_delegation_settings(body)

Modify SSL settings (partial update)

Updates the SSL settings that you send in the request. Other settings remain as is.

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.AccountSettingsDto() # AccountSettingsDto | 

try:
    # Modify SSL settings (partial update)
    api_response = api_instance.patch_ssl_validation_delegation_settings(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->patch_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AccountSettingsDto**](AccountSettingsDto.md)|  | 

### Return type

[**AccountSSLSettingsResponseDto**](AccountSSLSettingsResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **removed_domain_to_ssl_validation_delegation_settings**
> AccountSSLSettingsResponseDto removed_domain_to_ssl_validation_delegation_settings(domain_id)

Remove domain from the SSL validation delegation settings

Remove domain from the SSL validation delegation settings of your account. Certificate renewal may require you to revalidate domain ownership.

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))
domain_id = 789 # int | domainId can be getting from this api (GET /v3/account/ssl-settings)

try:
    # Remove domain from the SSL validation delegation settings
    api_response = api_instance.removed_domain_to_ssl_validation_delegation_settings(domain_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->removed_domain_to_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_id** | **int**| domainId can be getting from this api (GET /v3/account/ssl-settings) | 

### Return type

[**AccountSSLSettingsResponseDto**](AccountSSLSettingsResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_ssl_validation_delegation_settings**
> AccountSSLSettingsResponseDto update_ssl_validation_delegation_settings(body)

Overwrite SSL settings (full update)

Update SSL settings for your account.

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.AccountSettingsDto() # AccountSettingsDto | 

try:
    # Overwrite SSL settings (full update)
    api_response = api_instance.update_ssl_validation_delegation_settings(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->update_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AccountSettingsDto**](AccountSettingsDto.md)|  | 

### Return type

[**AccountSSLSettingsResponseDto**](AccountSSLSettingsResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verify_domain_to_ssl_validation_delegation_settings**
> AllowDelegationDomainWithInheritanceResponseDto verify_domain_to_ssl_validation_delegation_settings(domain_id)

Check the configuration status of a domain that appears in the domain delegation list

Check if the CNAME record has been added to the domain's DNS zone.

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
api_instance = swagger_client.SSLSettingsApi(swagger_client.ApiClient(configuration))
domain_id = 789 # int | domainId can be getting from this api (GET /v3/account/ssl-settings)

try:
    # Check the configuration status of a domain that appears in the domain delegation list
    api_response = api_instance.verify_domain_to_ssl_validation_delegation_settings(domain_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLSettingsApi->verify_domain_to_ssl_validation_delegation_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_id** | **int**| domainId can be getting from this api (GET /v3/account/ssl-settings) | 

### Return type

[**AllowDelegationDomainWithInheritanceResponseDto**](AllowDelegationDomainWithInheritanceResponseDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

