# swagger_client.SiteApi

All URIs are relative to *https://api.imperva.com/botmanagement*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v1_account_account_id_site_get**](SiteApi.md#v1_account_account_id_site_get) | **GET** /v1/account/{accountId}/site | Retrieve the list of Sites belonging to an Account
[**v1_account_account_id_site_post**](SiteApi.md#v1_account_account_id_site_post) | **POST** /v1/account/{accountId}/site | Create a new Site
[**v1_account_account_id_site_priority_get**](SiteApi.md#v1_account_account_id_site_priority_get) | **GET** /v1/account/{accountId}/site_priority | Retrieve the Account&#x27;s Site priority order
[**v1_account_account_id_site_priority_put**](SiteApi.md#v1_account_account_id_site_priority_put) | **PUT** /v1/account/{accountId}/site_priority | Set site priority in this Account
[**v1_site_site_id_delete**](SiteApi.md#v1_site_site_id_delete) | **DELETE** /v1/site/{siteId} | Delete a Site
[**v1_site_site_id_environmental_parameters_get**](SiteApi.md#v1_site_site_id_environmental_parameters_get) | **GET** /v1/site/{siteId}/environmental_parameters | Retrieve all environmental parameters used in a Site
[**v1_site_site_id_get**](SiteApi.md#v1_site_site_id_get) | **GET** /v1/site/{siteId} | Retrieve a Site
[**v1_site_site_id_put**](SiteApi.md#v1_site_site_id_put) | **PUT** /v1/site/{siteId} | Update a Site

# **v1_account_account_id_site_get**
> InlineResponse2004 v1_account_account_id_site_get(account_id, caid=caid)

Retrieve the list of Sites belonging to an Account

The Sites are returned in order from most to least significant. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the list of Sites belonging to an Account
    api_response = api_instance.v1_account_account_id_site_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_account_account_id_site_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_account_account_id_site_post**
> InlineResponse2011 v1_account_account_id_site_post(body, account_id, caid=caid)

Create a new Site

In addition to the provided Selectors, a default Selector that matches any path will automatically be created with the lowest priority. A default Policy will be automatically created and assigned to the default Selector. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateSiteV1() # CreateSiteV1 | 
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Create a new Site
    api_response = api_instance.v1_account_account_id_site_post(body, account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_account_account_id_site_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateSiteV1**](CreateSiteV1.md)|  | 
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2011**](InlineResponse2011.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_account_account_id_site_priority_get**
> InlineResponse20016 v1_account_account_id_site_priority_get(account_id, caid=caid)

Retrieve the Account's Site priority order

The response contains an array of `SiteId`s ordered by their priority. Listing all sites in the account returns results in the same order. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve the Account's Site priority order
    api_response = api_instance.v1_account_account_id_site_priority_get(account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_account_account_id_site_priority_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse20016**](InlineResponse20016.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_account_account_id_site_priority_put**
> InlineResponse20016 v1_account_account_id_site_priority_put(body, account_id, caid=caid)

Set site priority in this Account

Sets the order of the sites within this Account. All site IDs in the account must be provided exactly once. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
body = swagger_client.SitePriorityV1() # SitePriorityV1 | The new site priority list.
account_id = swagger_client.AccountId() # AccountId | Identifies an Account to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Set site priority in this Account
    api_response = api_instance.v1_account_account_id_site_priority_put(body, account_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_account_account_id_site_priority_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SitePriorityV1**](SitePriorityV1.md)| The new site priority list. | 
 **account_id** | [**AccountId**](.md)| Identifies an Account to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse20016**](InlineResponse20016.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_site_site_id_delete**
> InlineResponse2011 v1_site_site_id_delete(site_id, caid=caid)

Delete a Site

You must delete all Domains beloning to the Site before it can be deleted.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
site_id = swagger_client.SiteId() # SiteId | Identifies a Site to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Delete a Site
    api_response = api_instance.v1_site_site_id_delete(site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_site_site_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | [**SiteId**](.md)| Identifies a Site to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2011**](InlineResponse2011.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_site_site_id_environmental_parameters_get**
> InlineResponse20013 v1_site_site_id_environmental_parameters_get(site_id, caid=caid)

Retrieve all environmental parameters used in a Site

Retrieve all environmental parameters used in a Site

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
site_id = swagger_client.SiteId() # SiteId | Identifies a Site to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve all environmental parameters used in a Site
    api_response = api_instance.v1_site_site_id_environmental_parameters_get(site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_site_site_id_environmental_parameters_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | [**SiteId**](.md)| Identifies a Site to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse20013**](InlineResponse20013.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_site_site_id_get**
> InlineResponse2011 v1_site_site_id_get(site_id, caid=caid)

Retrieve a Site

Retrieve a Site.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
site_id = swagger_client.SiteId() # SiteId | Identifies a Site to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Retrieve a Site
    api_response = api_instance.v1_site_site_id_get(site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_site_site_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | [**SiteId**](.md)| Identifies a Site to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2011**](InlineResponse2011.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **v1_site_site_id_put**
> InlineResponse2011 v1_site_site_id_put(body, site_id, caid=caid)

Update a Site

Replaces a Site resource with the given representation.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-api-id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-api-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-api-key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.SiteApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateSiteV1() # UpdateSiteV1 | 
site_id = swagger_client.SiteId() # SiteId | Identifies a Site to operate on.
caid = 56 # int | Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account's ID.  (optional)

try:
    # Update a Site
    api_response = api_instance.v1_site_site_id_put(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SiteApi->v1_site_site_id_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateSiteV1**](UpdateSiteV1.md)|  | 
 **site_id** | [**SiteId**](.md)| Identifies a Site to operate on. | 
 **caid** | **int**| Current Account ID. API keys are valid for an account and all of its sub accounts. When working with sub-accounts, this needs to be set to the corresponding Imperva account ID. Not specifying the parameter will default it to the main account&#x27;s ID.  | [optional] 

### Return type

[**InlineResponse2011**](InlineResponse2011.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

