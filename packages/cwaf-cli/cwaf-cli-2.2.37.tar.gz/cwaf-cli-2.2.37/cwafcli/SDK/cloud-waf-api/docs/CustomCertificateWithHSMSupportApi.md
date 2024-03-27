# swagger_client.CustomCertificateWithHSMSupportApi

All URIs are relative to *https://my.imperva.com/api/prov/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sites_ext_site_id_hsm_certificate_connectivity_test_get**](CustomCertificateWithHSMSupportApi.md#sites_ext_site_id_hsm_certificate_connectivity_test_get) | **GET** /sites/{extSiteId}/hsmCertificate/connectivityTest | Test connectivity between Imperva and HSM provider
[**sites_ext_site_id_hsm_certificate_delete**](CustomCertificateWithHSMSupportApi.md#sites_ext_site_id_hsm_certificate_delete) | **DELETE** /sites/{extSiteId}/hsmCertificate | Remove custom certificate and HSM credentials
[**sites_ext_site_id_hsm_certificate_put**](CustomCertificateWithHSMSupportApi.md#sites_ext_site_id_hsm_certificate_put) | **PUT** /sites/{extSiteId}/hsmCertificate | Upload custom certificate and HSM credentials

# **sites_ext_site_id_hsm_certificate_connectivity_test_get**
> sites_ext_site_id_hsm_certificate_connectivity_test_get(ext_site_id)

Test connectivity between Imperva and HSM provider

Test connectivity between Imperva and your HSM service provider. This endpoint also validates the integrity between the certificate and the private key, provided by the HSM service.

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
api_instance = swagger_client.CustomCertificateWithHSMSupportApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | The Imperva ID of your website.

try:
    # Test connectivity between Imperva and HSM provider
    api_instance.sites_ext_site_id_hsm_certificate_connectivity_test_get(ext_site_id)
except ApiException as e:
    print("Exception when calling CustomCertificateWithHSMSupportApi->sites_ext_site_id_hsm_certificate_connectivity_test_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| The Imperva ID of your website. | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_hsm_certificate_delete**
> sites_ext_site_id_hsm_certificate_delete(ext_site_id)

Remove custom certificate and HSM credentials

Remove custom certificate and HSM credentials.

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
api_instance = swagger_client.CustomCertificateWithHSMSupportApi(swagger_client.ApiClient(configuration))
ext_site_id = 56 # int | The Imperva ID of your website.

try:
    # Remove custom certificate and HSM credentials
    api_instance.sites_ext_site_id_hsm_certificate_delete(ext_site_id)
except ApiException as e:
    print("Exception when calling CustomCertificateWithHSMSupportApi->sites_ext_site_id_hsm_certificate_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| The Imperva ID of your website. | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_ext_site_id_hsm_certificate_put**
> sites_ext_site_id_hsm_certificate_put(body, ext_site_id)

Upload custom certificate and HSM credentials

Upload a custom certificate without the private key. Provide credentials for the HSM service that is managing your private key.

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
api_instance = swagger_client.CustomCertificateWithHSMSupportApi(swagger_client.ApiClient(configuration))
body = swagger_client.HsmBody() # HsmBody | The private key asset details in your HSM service.
ext_site_id = 56 # int | The Imperva ID of your website.

try:
    # Upload custom certificate and HSM credentials
    api_instance.sites_ext_site_id_hsm_certificate_put(body, ext_site_id)
except ApiException as e:
    print("Exception when calling CustomCertificateWithHSMSupportApi->sites_ext_site_id_hsm_certificate_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HsmBody**](HsmBody.md)| The private key asset details in your HSM service. | 
 **ext_site_id** | **int**| The Imperva ID of your website. | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

