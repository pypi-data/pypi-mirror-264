# swagger_client.DomainsApi

All URIs are relative to *https://api.imperva.com/site-domain-manager*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_site_domain**](DomainsApi.md#add_site_domain) | **POST** /v2/sites/{siteId}/domains | Add domain to a given website
[**delete_site_domain**](DomainsApi.md#delete_site_domain) | **DELETE** /v2/sites/{siteId}/domains/{domainId} | Delete a domain from a website
[**get_site_domain**](DomainsApi.md#get_site_domain) | **GET** /v2/sites/{siteId}/domains/{domainId} |  Retrieve details of a given domain
[**list_site_domains**](DomainsApi.md#list_site_domains) | **GET** /v2/sites/{siteId}/domains | List domains for a given website

# **add_site_domain**
> SiteDomainDetails add_site_domain(body, site_id)

Add domain to a given website

Adds a domain to an onboarded website.

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
api_instance = swagger_client.DomainsApi(swagger_client.ApiClient(configuration))
body = swagger_client.AddSiteDomainDetails() # AddSiteDomainDetails | 
site_id = 789 # int | The Imperva ID of the onboarded website.

try:
    # Add domain to a given website
    api_response = api_instance.add_site_domain(body, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DomainsApi->add_site_domain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddSiteDomainDetails**](AddSiteDomainDetails.md)|  | 
 **site_id** | **int**| The Imperva ID of the onboarded website. | 

### Return type

[**SiteDomainDetails**](SiteDomainDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_site_domain**
> delete_site_domain(site_id, domain_id)

Delete a domain from a website

Deletes a domain from an onboarded website.

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
api_instance = swagger_client.DomainsApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the onboarded website.
domain_id = 789 # int | The Imperva ID of the domain. You can retrieve the domain ID using the GET /domains call.

try:
    # Delete a domain from a website
    api_instance.delete_site_domain(site_id, domain_id)
except ApiException as e:
    print("Exception when calling DomainsApi->delete_site_domain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the onboarded website. | 
 **domain_id** | **int**| The Imperva ID of the domain. You can retrieve the domain ID using the GET /domains call. | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_site_domain**
> SiteDomainDetails get_site_domain(site_id, domain_id)

 Retrieve details of a given domain

Retrieve details of a domain associated with an onboarded website.

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
api_instance = swagger_client.DomainsApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the onboarded website.
domain_id = 789 # int | The Imperva ID of the domain. You can retrieve the domain ID using the GET /domains call.

try:
    #  Retrieve details of a given domain
    api_response = api_instance.get_site_domain(site_id, domain_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DomainsApi->get_site_domain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the onboarded website. | 
 **domain_id** | **int**| The Imperva ID of the domain. You can retrieve the domain ID using the GET /domains call. | 

### Return type

[**SiteDomainDetails**](SiteDomainDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_site_domains**
> GetSiteDomainsDetails list_site_domains(site_id, page_number=page_number, page_size=page_size)

List domains for a given website

Lists all domains associated with an onboarded website.

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
api_instance = swagger_client.DomainsApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the onboarded website.
page_number = 56 # int | The page to return starting from 0.<br/><br/>In order to view the full results, run the API call with page_num set to 0,<br/>then again with page_num set to 1, and so forth.<br/><br/>Default: 0 (optional)
page_size = 56 # int | The number of objects to return in the response.<br/><br/>Default: 50<br/><br/>Maximum: 100 (optional)

try:
    # List domains for a given website
    api_response = api_instance.list_site_domains(site_id, page_number=page_number, page_size=page_size)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DomainsApi->list_site_domains: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the onboarded website. | 
 **page_number** | **int**| The page to return starting from 0.&lt;br/&gt;&lt;br/&gt;In order to view the full results, run the API call with page_num set to 0,&lt;br/&gt;then again with page_num set to 1, and so forth.&lt;br/&gt;&lt;br/&gt;Default: 0 | [optional] 
 **page_size** | **int**| The number of objects to return in the response.&lt;br/&gt;&lt;br/&gt;Default: 50&lt;br/&gt;&lt;br/&gt;Maximum: 100 | [optional] 

### Return type

[**GetSiteDomainsDetails**](GetSiteDomainsDetails.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

