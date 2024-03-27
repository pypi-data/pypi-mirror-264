# swagger_client.APIApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_api**](APIApi.md#add_api) | **POST** /api/{siteId} | Add an API
[**delete_api**](APIApi.md#delete_api) | **DELETE** /api/{siteId}/{apiId} | Delete an API
[**get_all_apis**](APIApi.md#get_all_apis) | **GET** /api | Retrieve all APIs for the account
[**get_all_site_apis**](APIApi.md#get_all_site_apis) | **GET** /api/{siteId} | Retrieve all APIs for a site
[**get_all_site_apis_with_endpoints**](APIApi.md#get_all_site_apis_with_endpoints) | **GET** /api/{siteId}/all | Retrieve all APIs and endpoints for a site
[**get_api**](APIApi.md#get_api) | **GET** /api/{siteId}/{apiId} | Retrieve an API
[**get_api_file**](APIApi.md#get_api_file) | **GET** /api/file/{siteId}/{apiId} | Download the API OAS file
[**update_api**](APIApi.md#update_api) | **POST** /api/{siteId}/{apiId} | Update an API

# **add_api**
> AddApiResponse add_api(api_specification, base_path, description, oas_file_name, specification_violation_action, validate_host, violation_actions, site_id)

Add an API

Adds an API specification to a site

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
api_specification = 'api_specification_example' # str | 
base_path = 'base_path_example' # str | 
description = 'description_example' # str | 
oas_file_name = 'oas_file_name_example' # str | 
specification_violation_action = 'specification_violation_action_example' # str | 
validate_host = true # bool | 
violation_actions = 'violation_actions_example' # str | 
site_id = 789 # int | The site ID

try:
    # Add an API
    api_response = api_instance.add_api(api_specification, base_path, description, oas_file_name, specification_violation_action, validate_host, violation_actions, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->add_api: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_specification** | **str**|  | 
 **base_path** | **str**|  | 
 **description** | **str**|  | 
 **oas_file_name** | **str**|  | 
 **specification_violation_action** | **str**|  | 
 **validate_host** | **bool**|  | 
 **violation_actions** | **str**|  | 
 **site_id** | **int**| The site ID | 

### Return type

[**AddApiResponse**](AddApiResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api**
> SimpleTextSuccessResponse delete_api(api_id, site_id)

Delete an API

Deletes an API from a site in the account

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID
site_id = 789 # int | The site ID

try:
    # Delete an API
    api_response = api_instance.delete_api(api_id, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->delete_api: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 
 **site_id** | **int**| The site ID | 

### Return type

[**SimpleTextSuccessResponse**](SimpleTextSuccessResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_apis**
> GetApisResponse get_all_apis()

Retrieve all APIs for the account

Retrieves details of all protected APIs for all sites in the account

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve all APIs for the account
    api_response = api_instance.get_all_apis()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->get_all_apis: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetApisResponse**](GetApisResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_site_apis**
> GetApisResponse get_all_site_apis(site_id)

Retrieve all APIs for a site

Retrieves details of all protected APIs for a specific site in the account

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The site ID

try:
    # Retrieve all APIs for a site
    api_response = api_instance.get_all_site_apis(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->get_all_site_apis: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The site ID | 

### Return type

[**GetApisResponse**](GetApisResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_site_apis_with_endpoints**
> GetApisWithEndpointsResponse get_all_site_apis_with_endpoints(site_id)

Retrieve all APIs and endpoints for a site

Retrieves details of all protected APIs and their endpoints for a specific site in the account

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The site ID

try:
    # Retrieve all APIs and endpoints for a site
    api_response = api_instance.get_all_site_apis_with_endpoints(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->get_all_site_apis_with_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The site ID | 

### Return type

[**GetApisWithEndpointsResponse**](GetApisWithEndpointsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api**
> GetApiResponse get_api(api_id, site_id)

Retrieve an API

Retrieves details of a specific API

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID
site_id = 789 # int | The site ID

try:
    # Retrieve an API
    api_response = api_instance.get_api(api_id, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->get_api: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 
 **site_id** | **int**| The site ID | 

### Return type

[**GetApiResponse**](GetApiResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_file**
> DownloadApiSpecificationDtoResponse get_api_file(api_id, site_id)

Download the API OAS file

Download the manually uploaded or automatically discovered OAS file for a specific API. If the API source is mixed, the result is the manually uploaded file.

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID
site_id = 789 # int | The site ID

try:
    # Download the API OAS file
    api_response = api_instance.get_api_file(api_id, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->get_api_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 
 **site_id** | **int**| The site ID | 

### Return type

[**DownloadApiSpecificationDtoResponse**](DownloadApiSpecificationDtoResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_api**
> AddApiResponse update_api(api_id, site_id, api_specification=api_specification, description=description, oas_file_name=oas_file_name, specification_violation_action=specification_violation_action, validate_host=validate_host, violation_actions=violation_actions)

Update an API

Updates any or all of the optional parameters.

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
api_instance = swagger_client.APIApi(swagger_client.ApiClient(configuration))
api_id = 789 # int | The API ID
site_id = 789 # int | The site ID
api_specification = 'api_specification_example' # str |  (optional)
description = 'description_example' # str |  (optional)
oas_file_name = 'oas_file_name_example' # str |  (optional)
specification_violation_action = 'specification_violation_action_example' # str |  (optional)
validate_host = true # bool |  (optional)
violation_actions = 'violation_actions_example' # str |  (optional)

try:
    # Update an API
    api_response = api_instance.update_api(api_id, site_id, api_specification=api_specification, description=description, oas_file_name=oas_file_name, specification_violation_action=specification_violation_action, validate_host=validate_host, violation_actions=violation_actions)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIApi->update_api: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **int**| The API ID | 
 **site_id** | **int**| The site ID | 
 **api_specification** | **str**|  | [optional] 
 **description** | **str**|  | [optional] 
 **oas_file_name** | **str**|  | [optional] 
 **specification_violation_action** | **str**|  | [optional] 
 **validate_host** | **bool**|  | [optional] 
 **violation_actions** | **str**|  | [optional] 

### Return type

[**AddApiResponse**](AddApiResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

