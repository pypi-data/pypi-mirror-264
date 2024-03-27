# swagger_client.SSLCertificatesApi

All URIs are relative to *https://api.imperva.com/certificates-ui*

Method | HTTP request | Description
------------- | ------------- | -------------
[**change_san_validation_method**](SSLCertificatesApi.md#change_san_validation_method) | **PUT** /v3/certificates/{certificateId}/sans/{sanId}/validationMethod | Change SAN validation method
[**get_certificates1**](SSLCertificatesApi.md#get_certificates1) | **GET** /v3/certificates | Get certificate details
[**san_instructions_for_account**](SSLCertificatesApi.md#san_instructions_for_account) | **GET** /v3/instructions | Get domain validation instructions

# **change_san_validation_method**
> ChangeValidationMethodExternalResponse change_san_validation_method(body, certificate_id, san_id)

Change SAN validation method

Changes the SAN validation method and value used for certificate revalidation.

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
api_instance = swagger_client.SSLCertificatesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ChangeValidationMethodRequest() # ChangeValidationMethodRequest | 
certificate_id = 789 # int | The Imperva ID assigned to the certificate. Use the GET /v3/certificates API call to retrieve the IDs of certificates in your account.
san_id = 789 # int | The Imperva ID assigned to the SAN. Use the GET /v3/certificates API call to retrieve the SAN IDs of certificates in your account.

try:
    # Change SAN validation method
    api_response = api_instance.change_san_validation_method(body, certificate_id, san_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLCertificatesApi->change_san_validation_method: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ChangeValidationMethodRequest**](ChangeValidationMethodRequest.md)|  | 
 **certificate_id** | **int**| The Imperva ID assigned to the certificate. Use the GET /v3/certificates API call to retrieve the IDs of certificates in your account. | 
 **san_id** | **int**| The Imperva ID assigned to the SAN. Use the GET /v3/certificates API call to retrieve the SAN IDs of certificates in your account. | 

### Return type

[**ChangeValidationMethodExternalResponse**](ChangeValidationMethodExternalResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_certificates1**
> Certificate get_certificates1(ext_site_id=ext_site_id, cert_type=cert_type)

Get certificate details

Get details for certificates in your account.

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
api_instance = swagger_client.SSLCertificatesApi(swagger_client.ApiClient(configuration))
ext_site_id = 789 # int | The Imperva ID of the onboarded website. Retrieves certificate details for a specific website. If not specified, this API retrieves details of all certificates in the account. (optional)
cert_type = 'cert_type_example' # str | The type of certificate to provide details for (optional)

try:
    # Get certificate details
    api_response = api_instance.get_certificates1(ext_site_id=ext_site_id, cert_type=cert_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLCertificatesApi->get_certificates1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| The Imperva ID of the onboarded website. Retrieves certificate details for a specific website. If not specified, this API retrieves details of all certificates in the account. | [optional] 
 **cert_type** | **str**| The type of certificate to provide details for | [optional] 

### Return type

[**Certificate**](Certificate.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **san_instructions_for_account**
> SanInstructionsDto san_instructions_for_account(ext_site_id=ext_site_id, validation_method=validation_method, certificate_type=certificate_type)

Get domain validation instructions

Get validation instructions for all pending SANs in the account

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
api_instance = swagger_client.SSLCertificatesApi(swagger_client.ApiClient(configuration))
ext_site_id = 789 # int | The Imperva ID of the onboarded website. (optional)
validation_method = 'validation_method_example' # str | The methods that can be used to validate ownership of the domain. (optional)
certificate_type = 'certificate_type_example' # str | The type that can be used to get san instructions. (optional)

try:
    # Get domain validation instructions
    api_response = api_instance.san_instructions_for_account(ext_site_id=ext_site_id, validation_method=validation_method, certificate_type=certificate_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SSLCertificatesApi->san_instructions_for_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ext_site_id** | **int**| The Imperva ID of the onboarded website. | [optional] 
 **validation_method** | **str**| The methods that can be used to validate ownership of the domain. | [optional] 
 **certificate_type** | **str**| The type that can be used to get san instructions. | [optional] 

### Return type

[**SanInstructionsDto**](SanInstructionsDto.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

