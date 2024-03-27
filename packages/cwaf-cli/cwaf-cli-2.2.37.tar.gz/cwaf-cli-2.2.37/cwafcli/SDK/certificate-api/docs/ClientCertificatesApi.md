# swagger_client.ClientCertificatesApi

All URIs are relative to *https://api.imperva.com/certificate-manager*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_client_ca_cert**](ClientCertificatesApi.md#add_client_ca_cert) | **POST** /v2/accounts/{accountId}/client-certificates | Add client CA certificate to account
[**assign_site_to_certificate**](ClientCertificatesApi.md#assign_site_to_certificate) | **POST** /v2/sites/{siteId}/client-certificates/{certId} | Assign client CA certificate of the account to site
[**deassign_cert_from_site**](ClientCertificatesApi.md#deassign_cert_from_site) | **DELETE** /v2/sites/{siteId}/client-certificates/{certId} | Remove client CA certificate from site
[**delete_client_ca_cert**](ClientCertificatesApi.md#delete_client_ca_cert) | **DELETE** /v2/accounts/{accountId}/client-certificates/{certId} | Delete client CA certificate from account
[**full_update_site_configuration**](ClientCertificatesApi.md#full_update_site_configuration) | **PUT** /v2/sites/{siteId}/configuration/client-certificates | Overwrite the client CA certificate configuration (full update)
[**get_all_certs_for_site**](ClientCertificatesApi.md#get_all_certs_for_site) | **GET** /v2/sites/{siteId}/client-certificates | List all client CA certificates assigned to site
[**get_site_configuration**](ClientCertificatesApi.md#get_site_configuration) | **GET** /v2/sites/{siteId}/configuration/client-certificates | Get client CA certificate configuration for site
[**list_client_ca_certs_by_account**](ClientCertificatesApi.md#list_client_ca_certs_by_account) | **GET** /v2/accounts/{accountId}/client-certificates | List client CA certificates in account
[**list_sites_by_cert**](ClientCertificatesApi.md#list_sites_by_cert) | **GET** /v2/accounts/{accountId}/client-certificates/{certId} | Get client CA certificate information including assigned sites
[**partial_update_site_configuration**](ClientCertificatesApi.md#partial_update_site_configuration) | **POST** /v2/sites/{siteId}/configuration/client-certificates | Modify the client CA certificate configuration (partial update)

# **add_client_ca_cert**
> ClientCACertificateDetails add_client_ca_cert(account_id, ca_file=ca_file, name=name)

Add client CA certificate to account

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | The Imperva ID for the account.
ca_file = 'B' # str |  (optional)
name = 'name_example' # str |  (optional)

try:
    # Add client CA certificate to account
    api_response = api_instance.add_client_ca_cert(account_id, ca_file=ca_file, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->add_client_ca_cert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| The Imperva ID for the account. | 
 **ca_file** | **str**|  | [optional] 
 **name** | **str**|  | [optional] 

### Return type

[**ClientCACertificateDetails**](ClientCACertificateDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assign_site_to_certificate**
> assign_site_to_certificate(site_id, cert_id)

Assign client CA certificate of the account to site

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.
cert_id = 789 # int | The Imperva ID assigned to an uploaded certificate. <br>Run GET method to locate the certificate ID.

try:
    # Assign client CA certificate of the account to site
    api_instance.assign_site_to_certificate(site_id, cert_id)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->assign_site_to_certificate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 
 **cert_id** | **int**| The Imperva ID assigned to an uploaded certificate. &lt;br&gt;Run GET method to locate the certificate ID. | 

### Return type

void (empty response body)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deassign_cert_from_site**
> deassign_cert_from_site(site_id, cert_id)

Remove client CA certificate from site

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.
cert_id = 789 # int | The Imperva ID assigned to an uploaded certificate. <br>Run GET method to locate the certificate ID.

try:
    # Remove client CA certificate from site
    api_instance.deassign_cert_from_site(site_id, cert_id)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->deassign_cert_from_site: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 
 **cert_id** | **int**| The Imperva ID assigned to an uploaded certificate. &lt;br&gt;Run GET method to locate the certificate ID. | 

### Return type

void (empty response body)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_client_ca_cert**
> delete_client_ca_cert(account_id, cert_id)

Delete client CA certificate from account

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | The Imperva ID for the account.
cert_id = 789 # int | The Imperva ID assigned to an uploaded certificate. <br>Run GET method to locate the certificate ID.

try:
    # Delete client CA certificate from account
    api_instance.delete_client_ca_cert(account_id, cert_id)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->delete_client_ca_cert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| The Imperva ID for the account. | 
 **cert_id** | **int**| The Imperva ID assigned to an uploaded certificate. &lt;br&gt;Run GET method to locate the certificate ID. | 

### Return type

void (empty response body)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **full_update_site_configuration**
> ClientCACertificateSiteConfiguration full_update_site_configuration(body, site_id)

Overwrite the client CA certificate configuration (full update)

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ClientCACertificateSiteConfiguration() # ClientCACertificateSiteConfiguration | configuration to update
site_id = 789 # int | The Imperva ID for the website.

try:
    # Overwrite the client CA certificate configuration (full update)
    api_response = api_instance.full_update_site_configuration(body, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->full_update_site_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ClientCACertificateSiteConfiguration**](ClientCACertificateSiteConfiguration.md)| configuration to update | 
 **site_id** | **int**| The Imperva ID for the website. | 

### Return type

[**ClientCACertificateSiteConfiguration**](ClientCACertificateSiteConfiguration.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_certs_for_site**
> ClientCACertificateDetails get_all_certs_for_site(site_id)

List all client CA certificates assigned to site

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.

try:
    # List all client CA certificates assigned to site
    api_response = api_instance.get_all_certs_for_site(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->get_all_certs_for_site: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 

### Return type

[**ClientCACertificateDetails**](ClientCACertificateDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_site_configuration**
> ClientCACertificateSiteConfiguration get_site_configuration(site_id)

Get client CA certificate configuration for site

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID for the website.

try:
    # Get client CA certificate configuration for site
    api_response = api_instance.get_site_configuration(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->get_site_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID for the website. | 

### Return type

[**ClientCACertificateSiteConfiguration**](ClientCACertificateSiteConfiguration.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_client_ca_certs_by_account**
> list[ClientCACertificateDetails] list_client_ca_certs_by_account(account_id)

List client CA certificates in account

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | The Imperva ID for the account.

try:
    # List client CA certificates in account
    api_response = api_instance.list_client_ca_certs_by_account(account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->list_client_ca_certs_by_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| The Imperva ID for the account. | 

### Return type

[**list[ClientCACertificateDetails]**](ClientCACertificateDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sites_by_cert**
> ClientCACertificateDetails list_sites_by_cert(account_id, cert_id)

Get client CA certificate information including assigned sites

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | The Imperva ID for the account.
cert_id = 789 # int | The Imperva ID assigned to an uploaded certificate. <br>Run GET method to locate the certificate ID.

try:
    # Get client CA certificate information including assigned sites
    api_response = api_instance.list_sites_by_cert(account_id, cert_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->list_sites_by_cert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| The Imperva ID for the account. | 
 **cert_id** | **int**| The Imperva ID assigned to an uploaded certificate. &lt;br&gt;Run GET method to locate the certificate ID. | 

### Return type

[**ClientCACertificateDetails**](ClientCACertificateDetails.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **partial_update_site_configuration**
> ClientCACertificateSiteConfiguration partial_update_site_configuration(body, site_id)

Modify the client CA certificate configuration (partial update)

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
api_instance = swagger_client.ClientCertificatesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ClientCACertificateSiteConfiguration() # ClientCACertificateSiteConfiguration | configuration sections to update
site_id = 789 # int | The Imperva ID for the website.

try:
    # Modify the client CA certificate configuration (partial update)
    api_response = api_instance.partial_update_site_configuration(body, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientCertificatesApi->partial_update_site_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ClientCACertificateSiteConfiguration**](ClientCACertificateSiteConfiguration.md)| configuration sections to update | 
 **site_id** | **int**| The Imperva ID for the website. | 

### Return type

[**ClientCACertificateSiteConfiguration**](ClientCACertificateSiteConfiguration.md)

### Authorization

[x-API-Id](../README.md#x-API-Id), [x-API-Key](../README.md#x-API-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

