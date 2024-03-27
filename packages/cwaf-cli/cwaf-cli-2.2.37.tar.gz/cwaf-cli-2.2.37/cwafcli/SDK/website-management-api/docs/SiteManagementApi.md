# swagger_client.SiteManagementApi

All URIs are relative to *https://api.imperva.com/sites-mgmt*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_site**](SiteManagementApi.md#get_site) | **GET** /v3/sites/{siteId} | Get site
[**get_sites**](SiteManagementApi.md#get_sites) | **GET** /v3/sites | Get sites

# **get_site**
> CollectionSite get_site(site_id, caid=caid)

Get site

Retrieve details of a website according to its Imperva ID

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
api_instance = swagger_client.SiteManagementApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | Numeric identifier of the site.
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Get site
    api_response = api_instance.get_site(site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteManagementApi->get_site: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| Numeric identifier of the site. | 
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**CollectionSite**](CollectionSite.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sites**
> PaginatedCollectionSite get_sites(site_ids=site_ids, names=names, site_types=site_types, page=page, size=size, caid=caid)

Get sites

Retrieve details of all websites associated with the current account. <br />To filter for a subset of the account’s websites, provide website IDs and website names. <br />If multiple filters are provided, an AND operation is applied and the API will return all websites matching the filters.

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
api_instance = swagger_client.SiteManagementApi(swagger_client.ApiClient(configuration))
site_ids = [56] # list[int] | A list of website ids. If this parameter is provided, only websites matching one of these IDs will be returned. (optional)
names = ['names_example'] # list[str] | A list of website names. If this parameter is provided, only websites matching one of these names will be returned. (optional)
site_types = ['site_types_example'] # list[str] | A list of website types. Indicates if the website is onboarded to Imperva Cloud WAF or configured for Imperva WAF Anywhere. If this parameter is provided, only websites with type matching one of these types will be returned. (optional)
page = 0 # int | The page to return starting from 0. (optional) (default to 0)
size = 10 # int | Page size used to determine the first object to be returned and the number of objects to be returned. (optional) (default to 10)
caid = 789 # int | The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. (optional)

try:
    # Get sites
    api_response = api_instance.get_sites(site_ids=site_ids, names=names, site_types=site_types, page=page, size=size, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteManagementApi->get_sites: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_ids** | [**list[int]**](int.md)| A list of website ids. If this parameter is provided, only websites matching one of these IDs will be returned. | [optional] 
 **names** | [**list[str]**](str.md)| A list of website names. If this parameter is provided, only websites matching one of these names will be returned. | [optional] 
 **site_types** | [**list[str]**](str.md)| A list of website types. Indicates if the website is onboarded to Imperva Cloud WAF or configured for Imperva WAF Anywhere. If this parameter is provided, only websites with type matching one of these types will be returned. | [optional] 
 **page** | **int**| The page to return starting from 0. | [optional] [default to 0]
 **size** | **int**| Page size used to determine the first object to be returned and the number of objects to be returned. | [optional] [default to 10]
 **caid** | **int**| The Imperva ID of the account or subaccount. By default, the account ID is the ID associated with the API credentials used for authentication. To run an API on a sub account, specify the sub account ID. | [optional] 

### Return type

[**PaginatedCollectionSite**](PaginatedCollectionSite.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

