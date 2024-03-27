# swagger_client.ConfigurationApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**copy_endpoint_configuration_from_site_to_another_site**](ConfigurationApi.md#copy_endpoint_configuration_from_site_to_another_site) | **POST** /v2/sites/{siteId}/onboard/copy-to/{target-site-id} | Copy a single login endpoint, or all of them, from the \&quot;source\&quot; website to the \&quot;target\&quot; website under the same account ID
[**delete_endpoint**](ConfigurationApi.md#delete_endpoint) | **DELETE** /v2/sites/{siteId}/endpoint/{endpointId} | Delete an endpoint for this website
[**get_endpoints**](ConfigurationApi.md#get_endpoints) | **GET** /v2/sites/{siteId}/endpoints | Retrieve all the onboarded login endpoints for this website
[**get_onboarded_sites_with_mitigation_status**](ConfigurationApi.md#get_onboarded_sites_with_mitigation_status) | **GET** /v2/sites | Retrieve all onboarded sites with their mitigation status.

# **copy_endpoint_configuration_from_site_to_another_site**
> copy_endpoint_configuration_from_site_to_another_site(site_id, target_site_id, caid=caid, endpoint_id=endpoint_id)

Copy a single login endpoint, or all of them, from the \"source\" website to the \"target\" website under the same account ID

Both sites must be under the same account ID (no sub-accounts support yet). In addition, mitigation settings are not copied.

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the \"source\" website (the website we copy from)
target_site_id = 789 # int | The Imperva ID of the \"target\" website (the website we want to copy the endpoint config to)
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str | Optional: pass an endpoint ID to copy, if none passed all endpoints will be copied (optional)

try:
    # Copy a single login endpoint, or all of them, from the \"source\" website to the \"target\" website under the same account ID
    api_instance.copy_endpoint_configuration_from_site_to_another_site(site_id, target_site_id, caid=caid, endpoint_id=endpoint_id)
except ApiException as e:
    print("Exception when calling ConfigurationApi->copy_endpoint_configuration_from_site_to_another_site: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the \&quot;source\&quot; website (the website we copy from) | 
 **target_site_id** | **int**| The Imperva ID of the \&quot;target\&quot; website (the website we want to copy the endpoint config to) | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**| Optional: pass an endpoint ID to copy, if none passed all endpoints will be copied | [optional] 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_endpoint**
> delete_endpoint(endpoint_id, site_id, caid=caid)

Delete an endpoint for this website

Delete the specified endpoint from the specified website.If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
endpoint_id = 'endpoint_id_example' # str | The endpoint ID to delete
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Delete an endpoint for this website
    api_instance.delete_endpoint(endpoint_id, site_id, caid=caid)
except ApiException as e:
    print("Exception when calling ConfigurationApi->delete_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_id** | **str**| The endpoint ID to delete | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_endpoints**
> list[Endpoints] get_endpoints(site_id, caid=caid)

Retrieve all the onboarded login endpoints for this website

Retrieve a list of all onboarded login endpoints for your website. Each endpoint will include its id, url, username and password parameters. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve all the onboarded login endpoints for this website
    api_response = api_instance.get_endpoints(site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**list[Endpoints]**](Endpoints.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_onboarded_sites_with_mitigation_status**
> list[SiteStatus] get_onboarded_sites_with_mitigation_status(caid=caid)

Retrieve all onboarded sites with their mitigation status.

Retrieve a list of all onboarded sites for the account ID. Each site will include the Imperva website ID, site name, and mitigation status. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve all onboarded sites with their mitigation status.
    api_response = api_instance.get_onboarded_sites_with_mitigation_status(caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->get_onboarded_sites_with_mitigation_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**list[SiteStatus]**](SiteStatus.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

