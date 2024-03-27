# swagger_client.RulesApi

All URIs are relative to *https://my.imperva.com/api/prov/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sites_site_id_rules_post**](RulesApi.md#sites_site_id_rules_post) | **POST** /sites/{siteId}/rules | Create rule
[**sites_site_id_rules_rule_id_delete**](RulesApi.md#sites_site_id_rules_rule_id_delete) | **DELETE** /sites/{siteId}/rules/{ruleId} | Delete rule - must contain valid rule id
[**sites_site_id_rules_rule_id_get**](RulesApi.md#sites_site_id_rules_rule_id_get) | **GET** /sites/{siteId}/rules/{ruleId} | Read rule - must contain valid rule id
[**sites_site_id_rules_rule_id_post**](RulesApi.md#sites_site_id_rules_rule_id_post) | **POST** /sites/{siteId}/rules/{ruleId} | Update rule - must contain valid rule id
[**sites_site_id_rules_rule_id_put**](RulesApi.md#sites_site_id_rules_rule_id_put) | **PUT** /sites/{siteId}/rules/{ruleId} | Overwrite rule - must contain valid rule id

# **sites_site_id_rules_post**
> Rule sites_site_id_rules_post(body, site_id)

Create rule

Create a custom rule. For full feature documentation, see [Rules](https://docs.imperva.com/bundle/cloud-application-security/page/rules/rules.htm).

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
api_instance = swagger_client.RulesApi(swagger_client.ApiClient(configuration))
body = swagger_client.Rule() # Rule | The rule to create
site_id = 56 # int | Site id

try:
    # Create rule
    api_response = api_instance.sites_site_id_rules_post(body, site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RulesApi->sites_site_id_rules_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Rule**](Rule.md)| The rule to create | 
 **site_id** | **int**| Site id | 

### Return type

[**Rule**](Rule.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_site_id_rules_rule_id_delete**
> ApiResult sites_site_id_rules_rule_id_delete(site_id, rule_id)

Delete rule - must contain valid rule id

Delete rule

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
api_instance = swagger_client.RulesApi(swagger_client.ApiClient(configuration))
site_id = 56 # int | Numeric identifier of the site to operate on
rule_id = 56 # int | Numeric identifier of the rule to operate on

try:
    # Delete rule - must contain valid rule id
    api_response = api_instance.sites_site_id_rules_rule_id_delete(site_id, rule_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RulesApi->sites_site_id_rules_rule_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| Numeric identifier of the site to operate on | 
 **rule_id** | **int**| Numeric identifier of the rule to operate on | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_site_id_rules_rule_id_get**
> Rule sites_site_id_rules_rule_id_get(site_id, rule_id)

Read rule - must contain valid rule id

Read rule

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
api_instance = swagger_client.RulesApi(swagger_client.ApiClient(configuration))
site_id = 56 # int | Numeric identifier of the site to operate on
rule_id = 56 # int | Numeric identifier of the rule to operate on

try:
    # Read rule - must contain valid rule id
    api_response = api_instance.sites_site_id_rules_rule_id_get(site_id, rule_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RulesApi->sites_site_id_rules_rule_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| Numeric identifier of the site to operate on | 
 **rule_id** | **int**| Numeric identifier of the rule to operate on | 

### Return type

[**Rule**](Rule.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_site_id_rules_rule_id_post**
> Rule sites_site_id_rules_rule_id_post(body, site_id, rule_id)

Update rule - must contain valid rule id

Update rule

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
api_instance = swagger_client.RulesApi(swagger_client.ApiClient(configuration))
body = swagger_client.Rule() # Rule | The rule to update
site_id = 56 # int | Numeric identifier of the site to operate on
rule_id = 56 # int | Numeric identifier of the rule to operate on

try:
    # Update rule - must contain valid rule id
    api_response = api_instance.sites_site_id_rules_rule_id_post(body, site_id, rule_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RulesApi->sites_site_id_rules_rule_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Rule**](Rule.md)| The rule to update | 
 **site_id** | **int**| Numeric identifier of the site to operate on | 
 **rule_id** | **int**| Numeric identifier of the rule to operate on | 

### Return type

[**Rule**](Rule.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sites_site_id_rules_rule_id_put**
> Rule sites_site_id_rules_rule_id_put(body, site_id, rule_id)

Overwrite rule - must contain valid rule id

Overwrite rule

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
api_instance = swagger_client.RulesApi(swagger_client.ApiClient(configuration))
body = swagger_client.Rule() # Rule | The rule to overwrite
site_id = 56 # int | Numeric identifier of the site to operate on
rule_id = 56 # int | Numeric identifier of the rule to operate on

try:
    # Overwrite rule - must contain valid rule id
    api_response = api_instance.sites_site_id_rules_rule_id_put(body, site_id, rule_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RulesApi->sites_site_id_rules_rule_id_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Rule**](Rule.md)| The rule to overwrite | 
 **site_id** | **int**| Numeric identifier of the site to operate on | 
 **rule_id** | **int**| Numeric identifier of the rule to operate on | 

### Return type

[**Rule**](Rule.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

