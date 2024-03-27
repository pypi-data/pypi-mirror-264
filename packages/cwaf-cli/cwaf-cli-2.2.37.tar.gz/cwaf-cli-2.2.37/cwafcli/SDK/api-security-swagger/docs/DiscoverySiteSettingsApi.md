# swagger_client.DiscoverySiteSettingsApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_site_discovery_settings**](DiscoverySiteSettingsApi.md#get_site_discovery_settings) | **GET** /v2/discovery/sites/{siteId}/settings | Retrieve discovery settings for a site
[**get_sites_discovery_settings**](DiscoverySiteSettingsApi.md#get_sites_discovery_settings) | **GET** /v2/discovery/sites/settings | Retrieve the discovery settings for all sites in the account
[**update_one_site_discovery_settings**](DiscoverySiteSettingsApi.md#update_one_site_discovery_settings) | **POST** /v2/discovery/sites/{siteId}/settings | Update the site&#x27;s discovery settings
[**update_sites_discovery_settings**](DiscoverySiteSettingsApi.md#update_sites_discovery_settings) | **POST** /v2/discovery/sites/settings | Update the site&#x27;s discovery settings

# **get_site_discovery_settings**
> GetSiteDiscoverySettingsResponse get_site_discovery_settings(site_id)

Retrieve discovery settings for a site

Retrieve discovery settings for a site

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
api_instance = swagger_client.DiscoverySiteSettingsApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The site ID

try:
    # Retrieve discovery settings for a site
    api_response = api_instance.get_site_discovery_settings(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoverySiteSettingsApi->get_site_discovery_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The site ID | 

### Return type

[**GetSiteDiscoverySettingsResponse**](GetSiteDiscoverySettingsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sites_discovery_settings**
> GetSiteDiscoverySettingsListResponse get_sites_discovery_settings()

Retrieve the discovery settings for all sites in the account

Retrieve the discovery settings for all sites in the account

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
api_instance = swagger_client.DiscoverySiteSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve the discovery settings for all sites in the account
    api_response = api_instance.get_sites_discovery_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoverySiteSettingsApi->get_sites_discovery_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetSiteDiscoverySettingsListResponse**](GetSiteDiscoverySettingsListResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_site_discovery_settings**
> GetSiteDiscoverySettingsResponse update_one_site_discovery_settings(site_id, body=body)

Update the site's discovery settings

Update the site's discovery settings with one of the optional parameters for each site

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
api_instance = swagger_client.DiscoverySiteSettingsApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The site ID
body = swagger_client.SiteDiscoverySettings() # SiteDiscoverySettings | Discovery settings (optional)

try:
    # Update the site's discovery settings
    api_response = api_instance.update_one_site_discovery_settings(site_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoverySiteSettingsApi->update_one_site_discovery_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The site ID | 
 **body** | [**SiteDiscoverySettings**](SiteDiscoverySettings.md)| Discovery settings | [optional] 

### Return type

[**GetSiteDiscoverySettingsResponse**](GetSiteDiscoverySettingsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_sites_discovery_settings**
> GetSiteDiscoverySettingsListResponse update_sites_discovery_settings(body=body)

Update the site's discovery settings

Update the site's discovery settings with one of the optional parameters for each site

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
api_instance = swagger_client.DiscoverySiteSettingsApi(swagger_client.ApiClient(configuration))
body = [swagger_client.SiteDiscoverySettings()] # list[SiteDiscoverySettings] | Discovery settings (optional)

try:
    # Update the site's discovery settings
    api_response = api_instance.update_sites_discovery_settings(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoverySiteSettingsApi->update_sites_discovery_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[SiteDiscoverySettings]**](SiteDiscoverySettings.md)| Discovery settings | [optional] 

### Return type

[**GetSiteDiscoverySettingsListResponse**](GetSiteDiscoverySettingsListResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

