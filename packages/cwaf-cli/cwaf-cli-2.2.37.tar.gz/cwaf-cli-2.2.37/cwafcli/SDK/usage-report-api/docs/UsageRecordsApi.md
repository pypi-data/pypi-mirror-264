# swagger_client.UsageRecordsApi

All URIs are relative to *https://api.imperva.com/usage-management*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_detailed_usage**](UsageRecordsApi.md#get_detailed_usage) | **GET** /v3/subscription-usage-records/{subscription-usage-record-id}/detailed-usage | Retrieve a usage record&#x27;s detailed information.
[**get_usage_summary**](UsageRecordsApi.md#get_usage_summary) | **GET** /v3/subscription-usage-records | Retrieve a summary of usage records.

# **get_detailed_usage**
> ImpervaApiBodyListDetailedSubscriptionUsage get_detailed_usage(caid, subscription_usage_record_id, resource)

Retrieve a usage record's detailed information.

Retrieve a usage record's detailed information.

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
api_instance = swagger_client.UsageRecordsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
subscription_usage_record_id = 'subscription_usage_record_id_example' # str | Unique identifier of the subscription usage record. Run the GET /v3/subscription-usage-record API to locate the value of the ‘id’ parameter in the response.
resource = 'resource_example' # str | Resource ID.

try:
    # Retrieve a usage record's detailed information.
    api_response = api_instance.get_detailed_usage(caid, subscription_usage_record_id, resource)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsageRecordsApi->get_detailed_usage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **subscription_usage_record_id** | **str**| Unique identifier of the subscription usage record. Run the GET /v3/subscription-usage-record API to locate the value of the ‘id’ parameter in the response. | 
 **resource** | **str**| Resource ID. | 

### Return type

[**ImpervaApiBodyListDetailedSubscriptionUsage**](ImpervaApiBodyListDetailedSubscriptionUsage.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usage_summary**
> ImpervaApiBodyListSubscriptionUsageRecord get_usage_summary(caid, _from=_from, to=to, resource=resource)

Retrieve a summary of usage records.

Retrieve a summary of usage records.

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
api_instance = swagger_client.UsageRecordsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
_from = '2013-10-20' # date | Earliest time boundary, specified as an ISO Date Format yyyy-MM-dd. (optional)
to = '2013-10-20' # date | Latest time boundary, specified as an ISO Date Format yyyy-MM-dd. (optional)
resource = 'resource_example' # str | Resource ID. Possible values : advanced_bot_protection_connector, api_security_anywhere ,bot_management ,infra_protect_always_on_bandwidth, on_demand_throughput, throughput (optional)

try:
    # Retrieve a summary of usage records.
    api_response = api_instance.get_usage_summary(caid, _from=_from, to=to, resource=resource)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsageRecordsApi->get_usage_summary: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **_from** | **date**| Earliest time boundary, specified as an ISO Date Format yyyy-MM-dd. | [optional] 
 **to** | **date**| Latest time boundary, specified as an ISO Date Format yyyy-MM-dd. | [optional] 
 **resource** | **str**| Resource ID. Possible values : advanced_bot_protection_connector, api_security_anywhere ,bot_management ,infra_protect_always_on_bandwidth, on_demand_throughput, throughput | [optional] 

### Return type

[**ImpervaApiBodyListSubscriptionUsageRecord**](ImpervaApiBodyListSubscriptionUsageRecord.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

