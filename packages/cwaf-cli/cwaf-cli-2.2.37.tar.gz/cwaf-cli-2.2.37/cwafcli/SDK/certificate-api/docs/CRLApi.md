# swagger_client.CRLApi

All URIs are relative to *https://api.imperva.com/certificate-manager*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_crl**](CRLApi.md#add_crl) | **POST** /sites/{siteId}/CRL | Add CRL to site
[**full_update_crl**](CRLApi.md#full_update_crl) | **PUT** /sites/{siteId}/CRL/{crlId} | Update existing CRL on site
[**list_crls**](CRLApi.md#list_crls) | **GET** /sites/{siteId}/CRL | List site CRLs
[**remove_crl**](CRLApi.md#remove_crl) | **DELETE** /sites/{siteId}/CRL/{crlId} | Remove CRL from site

# **add_crl**
> CRLDetails add_crl(site_id, crl_file=crl_file, name=name)

Add CRL to site

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: x-API-Id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: x-API-Key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CRLApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.
crl_file = 'crl_file_example' # str |  (optional)
name = 'name_example' # str |  (optional)

try:
    # Add CRL to site
    api_response = api_instance.add_crl(site_id, crl_file=crl_file, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CRLApi->add_crl: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 
 **crl_file** | **str**|  | [optional] 
 **name** | **str**|  | [optional] 

### Return type

[**CRLDetails**](CRLDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **full_update_crl**
> CRLDetails full_update_crl(site_id, crl_id, crl_file=crl_file, name=name)

Update existing CRL on site

Replaces the CRL currently uploaded to the website

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: x-API-Id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: x-API-Key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CRLApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.
crl_id = 789 # int | The Imperva ID for the CRL.
crl_file = 'crl_file_example' # str |  (optional)
name = 'name_example' # str |  (optional)

try:
    # Update existing CRL on site
    api_response = api_instance.full_update_crl(site_id, crl_id, crl_file=crl_file, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CRLApi->full_update_crl: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 
 **crl_id** | **int**| The Imperva ID for the CRL. | 
 **crl_file** | **str**|  | [optional] 
 **name** | **str**|  | [optional] 

### Return type

[**CRLDetails**](CRLDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_crls**
> CRLDetails list_crls(site_id)

List site CRLs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: x-API-Id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: x-API-Key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CRLApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.

try:
    # List site CRLs
    api_response = api_instance.list_crls(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CRLApi->list_crls: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 

### Return type

[**CRLDetails**](CRLDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_crl**
> remove_crl(site_id, crl_id)

Remove CRL from site

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: x-API-Id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: x-API-Key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CRLApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.
crl_id = 789 # int | The Imperva ID for the CRL.

try:
    # Remove CRL from site
    api_instance.remove_crl(site_id, crl_id)
except ApiException as e:
    print("Exception when calling CRLApi->remove_crl: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 
 **crl_id** | **int**| The Imperva ID for the CRL. | 

### Return type

void (empty response body)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

