# swagger_client.SiteConfigurationApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_site_configuration_for_account**](SiteConfigurationApi.md#get_site_configuration_for_account) | **GET** /config/site | Retrieves all site configurations
[**get_site_configuration_for_site**](SiteConfigurationApi.md#get_site_configuration_for_site) | **GET** /config/site/{siteId} | Retrieves a site configuration
[**update_site_configuration**](SiteConfigurationApi.md#update_site_configuration) | **POST** /config/site/{siteId} | Updates site configuration

# **get_site_configuration_for_account**
> GetSiteConfigurationsResponse get_site_configuration_for_account(filter_active_only=filter_active_only)

Retrieves all site configurations

Retrieves configuration settings for all sites in the account.

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
api_instance = swagger_client.SiteConfigurationApi(swagger_client.ApiClient(configuration))
filter_active_only = true # bool |  (optional)

try:
    # Retrieves all site configurations
    api_response = api_instance.get_site_configuration_for_account(filter_active_only=filter_active_only)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteConfigurationApi->get_site_configuration_for_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter_active_only** | **bool**|  | [optional] 

### Return type

[**GetSiteConfigurationsResponse**](GetSiteConfigurationsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_site_configuration_for_site**
> GetSiteConfigurationResponse get_site_configuration_for_site(site_id)

Retrieves a site configuration

Retrieves the configuration settings for a specific site

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
api_instance = swagger_client.SiteConfigurationApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The site ID

try:
    # Retrieves a site configuration
    api_response = api_instance.get_site_configuration_for_site(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteConfigurationApi->get_site_configuration_for_site: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The site ID | 

### Return type

[**GetSiteConfigurationResponse**](GetSiteConfigurationResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_site_configuration**
> UpdateSiteConfigurationResponse update_site_configuration(site_id, body=body)

Updates site configuration

Updates the site configuration with settings such as attack policy and more as the optional parameters

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
api_instance = swagger_client.SiteConfigurationApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The site ID
body = swagger_client.SiteConfigurationResponse() # SiteConfigurationResponse | Settings for attack policy and more (optional)

try:
    # Updates site configuration
    api_response = api_instance.update_site_configuration(site_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteConfigurationApi->update_site_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The site ID | 
 **body** | [**SiteConfigurationResponse**](SiteConfigurationResponse.md)| Settings for attack policy and more | [optional] 

### Return type

[**UpdateSiteConfigurationResponse**](UpdateSiteConfigurationResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

