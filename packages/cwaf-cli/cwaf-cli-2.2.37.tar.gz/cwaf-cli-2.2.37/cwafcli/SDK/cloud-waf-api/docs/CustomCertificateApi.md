# swagger_client.CustomCertificateApi

All URIs are relative to *https://my.imperva.com/api/prov/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sites_ext_site_id_custom_certificate_delete**](CustomCertificateApi.md#sites_ext_site_id_custom_certificate_delete) | **DELETE** /sites/{extSiteId}/customCertificate | Remove custom certificate
[**sites_ext_site_id_custom_certificate_put**](CustomCertificateApi.md#sites_ext_site_id_custom_certificate_put) | **PUT** /sites/{extSiteId}/customCertificate | Upload custom certificate

# **sites_ext_site_id_custom_certificate_delete**
> sites_ext_site_id_custom_certificate_delete(ext_site_id, auth_type)

Remove custom certificate

Remove the custom certificate uploaded to Imperva for a specified website.

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
api_instance = swagger_client.CustomCertificateApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | The Imperva ID of your website.
auth_type = 'auth_type_example' # str | 

try:
    # Remove custom certificate
    api_instance.sites_ext_site_id_custom_certificate_delete(ext_site_id, auth_type)
except ApiException as e:
    print("Exception when calling CustomCertificateApi->sites_ext_site_id_custom_certificate_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| The Imperva ID of your website. | 
 **auth_type** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_custom_certificate_put**
> sites_ext_site_id_custom_certificate_put(body, ext_site_id)

Upload custom certificate

Upload your own SSL certificate to Imperva for a specified website. Supported file formats: PFX, PEM, CER. This certificate is presented to SNI-supporting clients only.

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
api_instance = swagger_client.CustomCertificateApi(swagger_client.ApiClient(configuration))
body = swagger_client.CustomCertificateBody() # CustomCertificateBody | 
ext_site_id = 56 # int | The Imperva ID of your website.

try:
    # Upload custom certificate
    api_instance.sites_ext_site_id_custom_certificate_put(body, ext_site_id)
except ApiException as e:
    print("Exception when calling CustomCertificateApi->sites_ext_site_id_custom_certificate_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomCertificateBody**](CustomCertificateBody.md)|  | 
 **ext_site_id** | **int**| The Imperva ID of your website. | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

