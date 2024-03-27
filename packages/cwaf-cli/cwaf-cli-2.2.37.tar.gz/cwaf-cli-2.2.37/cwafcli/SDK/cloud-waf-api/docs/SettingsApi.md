# swagger_client.SettingsApi

All URIs are relative to *https://my.imperva.com/api/prov/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sites_ext_site_id_settings_general_additional_txt_records_delete**](SettingsApi.md#sites_ext_site_id_settings_general_additional_txt_records_delete) | **DELETE** /sites/{extSiteId}/settings/general/additionalTxtRecords | Delete a specific TXT record that is defined for the site in Cloud WAF
[**sites_ext_site_id_settings_general_additional_txt_records_delete_all_delete**](SettingsApi.md#sites_ext_site_id_settings_general_additional_txt_records_delete_all_delete) | **DELETE** /sites/{extSiteId}/settings/general/additionalTxtRecords/delete-all | Delete all TXT records that are defined for the site in Cloud WAF
[**sites_ext_site_id_settings_general_additional_txt_records_get**](SettingsApi.md#sites_ext_site_id_settings_general_additional_txt_records_get) | **GET** /sites/{extSiteId}/settings/general/additionalTxtRecords | Return all TXT records defined for the site in Cloud WAF
[**sites_ext_site_id_settings_general_additional_txt_records_post**](SettingsApi.md#sites_ext_site_id_settings_general_additional_txt_records_post) | **POST** /sites/{extSiteId}/settings/general/additionalTxtRecords | Create or modify one or more of the TXT records defined for the site in Cloud WAF  (partial update)
[**sites_ext_site_id_settings_general_additional_txt_records_put**](SettingsApi.md#sites_ext_site_id_settings_general_additional_txt_records_put) | **PUT** /sites/{extSiteId}/settings/general/additionalTxtRecords | Overwrite a specific TXT record that is defined for the site in Cloud WAF  (full update)
[**sites_site_id_settings_masking_get**](SettingsApi.md#sites_site_id_settings_masking_get) | **GET** /sites/{siteId}/settings/masking | Returns a masking setting for the given site.
[**sites_site_id_settings_masking_post**](SettingsApi.md#sites_site_id_settings_masking_post) | **POST** /sites/{siteId}/settings/masking | Update masking settings for site

# **sites_ext_site_id_settings_general_additional_txt_records_delete**
> sites_ext_site_id_settings_general_additional_txt_records_delete(ext_site_id, record_number=record_number)

Delete a specific TXT record that is defined for the site in Cloud WAF

Delete a specific TXT record that is defined for the site in Cloud WAF

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | Site id
record_number = 'record_number_example' # str | Number of txt record to delete (optional)

try:
    # Delete a specific TXT record that is defined for the site in Cloud WAF
    api_instance.sites_ext_site_id_settings_general_additional_txt_records_delete(ext_site_id, record_number=record_number)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_ext_site_id_settings_general_additional_txt_records_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| Site id | 
 **record_number** | **str**| Number of txt record to delete | [optional] 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_settings_general_additional_txt_records_delete_all_delete**
> sites_ext_site_id_settings_general_additional_txt_records_delete_all_delete(ext_site_id)

Delete all TXT records that are defined for the site in Cloud WAF

Delete all TXT records that are defined for the site in Cloud WAF

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | Site id

try:
    # Delete all TXT records that are defined for the site in Cloud WAF
    api_instance.sites_ext_site_id_settings_general_additional_txt_records_delete_all_delete(ext_site_id)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_ext_site_id_settings_general_additional_txt_records_delete_all_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| Site id | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_settings_general_additional_txt_records_get**
> sites_ext_site_id_settings_general_additional_txt_records_get(ext_site_id)

Return all TXT records defined for the site in Cloud WAF

Return all TXT records defined for the site in Cloud WAF

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | Site id

try:
    # Return all TXT records defined for the site in Cloud WAF
    api_instance.sites_ext_site_id_settings_general_additional_txt_records_get(ext_site_id)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_ext_site_id_settings_general_additional_txt_records_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| Site id | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_settings_general_additional_txt_records_post**
> sites_ext_site_id_settings_general_additional_txt_records_post(ext_site_id, txt_record_value_one=txt_record_value_one, txt_record_value_two=txt_record_value_two, txt_record_value_three=txt_record_value_three, txt_record_value_four=txt_record_value_four, txt_record_value_five=txt_record_value_five)

Create or modify one or more of the TXT records defined for the site in Cloud WAF  (partial update)

Create or modify one or more of the TXT records defined for the site in Cloud WAF  (partial update)

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | Site id
txt_record_value_one = 'txt_record_value_one_example' # str | New value for txt record number one (optional)
txt_record_value_two = 'txt_record_value_two_example' # str | New value for txt record number two (optional)
txt_record_value_three = 'txt_record_value_three_example' # str | New value for txt record number three (optional)
txt_record_value_four = 'txt_record_value_four_example' # str | New value for txt record number four (optional)
txt_record_value_five = 'txt_record_value_five_example' # str | New value for txt record number five (optional)

try:
    # Create or modify one or more of the TXT records defined for the site in Cloud WAF  (partial update)
    api_instance.sites_ext_site_id_settings_general_additional_txt_records_post(ext_site_id, txt_record_value_one=txt_record_value_one, txt_record_value_two=txt_record_value_two, txt_record_value_three=txt_record_value_three, txt_record_value_four=txt_record_value_four, txt_record_value_five=txt_record_value_five)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_ext_site_id_settings_general_additional_txt_records_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| Site id | 
 **txt_record_value_one** | **str**| New value for txt record number one | [optional] 
 **txt_record_value_two** | **str**| New value for txt record number two | [optional] 
 **txt_record_value_three** | **str**| New value for txt record number three | [optional] 
 **txt_record_value_four** | **str**| New value for txt record number four | [optional] 
 **txt_record_value_five** | **str**| New value for txt record number five | [optional] 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_settings_general_additional_txt_records_put**
> sites_ext_site_id_settings_general_additional_txt_records_put(ext_site_id, record_number=record_number, txt_record_value=txt_record_value)

Overwrite a specific TXT record that is defined for the site in Cloud WAF  (full update)

Overwrite a specific TXT record that is defined for the site in Cloud WAF  (full update)

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | Site id
record_number = 'record_number_example' # str | Number of txt record to edit (optional)
txt_record_value = 'txt_record_value_example' # str | New value for txt record (optional)

try:
    # Overwrite a specific TXT record that is defined for the site in Cloud WAF  (full update)
    api_instance.sites_ext_site_id_settings_general_additional_txt_records_put(ext_site_id, record_number=record_number, txt_record_value=txt_record_value)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_ext_site_id_settings_general_additional_txt_records_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| Site id | 
 **record_number** | **str**| Number of txt record to edit | [optional] 
 **txt_record_value** | **str**| New value for txt record | [optional] 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_site_id_settings_masking_get**
> sites_site_id_settings_masking_get(site_id)

Returns a masking setting for the given site.

Read masking settings.

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
site_id = 56 # int | Site id

try:
    # Returns a masking setting for the given site.
    api_instance.sites_site_id_settings_masking_get(site_id)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_site_id_settings_masking_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| Site id | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_site_id_settings_masking_post**
> sites_site_id_settings_masking_post(body, site_id)

Update masking settings for site

Update masking settings.

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
api_instance = swagger_client.SettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.MaskingSettings() # MaskingSettings | The masking setting to configure
site_id = 56 # int | Site id

try:
    # Update masking settings for site
    api_instance.sites_site_id_settings_masking_post(body, site_id)
except ApiException as e:
    print("Exception when calling SettingsApi->sites_site_id_settings_masking_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MaskingSettings**](MaskingSettings.md)| The masking setting to configure | 
 **site_id** | **int**| Site id | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

