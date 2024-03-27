# swagger_client.DiscoveryAccountSettingsApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_auth_location**](DiscoveryAccountSettingsApi.md#add_auth_location) | **POST** /v2/discovery/account/settings/auth-parameter-location | Add Authentication Location
[**delete_discovery_account_settings**](DiscoveryAccountSettingsApi.md#delete_discovery_account_settings) | **DELETE** /v2/discovery/account/settings | Deletes the Discovery account settings
[**get_discovery_account_settings**](DiscoveryAccountSettingsApi.md#get_discovery_account_settings) | **GET** /v2/discovery/account/settings | Retrieve the Discovery account settings
[**update_discovery_account_settings**](DiscoveryAccountSettingsApi.md#update_discovery_account_settings) | **POST** /v2/discovery/account/settings | Update only the changed Discovery account settings

# **add_auth_location**
> AuthParameterLocationResponse add_auth_location(body=body)

Add Authentication Location

Adds the Authentication Location for all websites currently configured or to a specific website

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
api_instance = swagger_client.DiscoveryAccountSettingsApi(swagger_client.ApiClient(configuration))
body = [swagger_client.AuthParameterLocationDto()] # list[AuthParameterLocationDto] | Authentication location details (optional)

try:
    # Add Authentication Location
    api_response = api_instance.add_auth_location(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryAccountSettingsApi->add_auth_location: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[AuthParameterLocationDto]**](AuthParameterLocationDto.md)| Authentication location details | [optional] 

### Return type

[**AuthParameterLocationResponse**](AuthParameterLocationResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_discovery_account_settings**
> delete_discovery_account_settings(body=body)

Deletes the Discovery account settings

Deletes the specific settings of the Discovery account which includes the site settings.

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
api_instance = swagger_client.DiscoveryAccountSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DiscoveryAccountSettings() # DiscoveryAccountSettings | Discovery Account Settings (optional)

try:
    # Deletes the Discovery account settings
    api_instance.delete_discovery_account_settings(body=body)
except ApiException as e:
    print("Exception when calling DiscoveryAccountSettingsApi->delete_discovery_account_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DiscoveryAccountSettings**](DiscoveryAccountSettings.md)| Discovery Account Settings | [optional] 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_discovery_account_settings**
> GetDiscoveryAccountSettingsResponse get_discovery_account_settings()

Retrieve the Discovery account settings

Retrieves the configuration details for the Discovery account settings associated with the account.

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
api_instance = swagger_client.DiscoveryAccountSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve the Discovery account settings
    api_response = api_instance.get_discovery_account_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryAccountSettingsApi->get_discovery_account_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetDiscoveryAccountSettingsResponse**](GetDiscoveryAccountSettingsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_discovery_account_settings**
> GetDiscoveryAccountSettingsResponse update_discovery_account_settings(body=body)

Update only the changed Discovery account settings

Updates the configuration details for the changed Discovery account settings associated with the account.

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
api_instance = swagger_client.DiscoveryAccountSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DiscoveryAccountSettings() # DiscoveryAccountSettings | Discovery Account Settings (optional)

try:
    # Update only the changed Discovery account settings
    api_response = api_instance.update_discovery_account_settings(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryAccountSettingsApi->update_discovery_account_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DiscoveryAccountSettings**](DiscoveryAccountSettings.md)| Discovery Account Settings | [optional] 

### Return type

[**GetDiscoveryAccountSettingsResponse**](GetDiscoveryAccountSettingsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

