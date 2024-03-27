# swagger_client.AuditTrailV1RetiredApi

All URIs are relative to *https://api.imperva.com/audit-trail*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_audit_events**](AuditTrailV1RetiredApi.md#get_audit_events) | **GET** /v1/events | Get account audit events

# **get_audit_events**
> list[AuditRecord] get_audit_events(start, assume=assume, caid=caid, end=end, limit=limit, offset=offset, type=type)

Get account audit events

This api is deprecated. This is a list of audit events of the specified account

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
api_instance = swagger_client.AuditTrailV1RetiredApi(swagger_client.ApiClient(configuration))
start = 789 # int | Earliest time boundary (in milliseconds)
assume = true # bool | Is the action performed by Imperva Support logged in as an account user (optional)
caid = 789 # int | Numeric identifier of the account to operate on. If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
end = 789 # int | Latest time boundary (in milliseconds) (optional)
limit = 56 # int | The number of objects to return in the response. Defaults to 50. Maximum is 100 (optional)
offset = 56 # int | Offset is the position of a particular record in the dataset. You can retrieve a subset of records starting with the offset value. The offset and limit parameters work together. Valid values for the offset parameter are multiples of the limit. For example, if you define limit as 50, you can define offset as either 0, 50, 100, 150, or any multiple of 50. (optional)
type = 'type_example' # str | The action that was performed in the account, such as ACCOUNT_LOGIN (optional)

try:
    # Get account audit events
    api_response = api_instance.get_audit_events(start, assume=assume, caid=caid, end=end, limit=limit, offset=offset, type=type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditTrailV1RetiredApi->get_audit_events: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start** | **int**| Earliest time boundary (in milliseconds) | 
 **assume** | **bool**| Is the action performed by Imperva Support logged in as an account user | [optional] 
 **caid** | **int**| Numeric identifier of the account to operate on. If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **end** | **int**| Latest time boundary (in milliseconds) | [optional] 
 **limit** | **int**| The number of objects to return in the response. Defaults to 50. Maximum is 100 | [optional] 
 **offset** | **int**| Offset is the position of a particular record in the dataset. You can retrieve a subset of records starting with the offset value. The offset and limit parameters work together. Valid values for the offset parameter are multiples of the limit. For example, if you define limit as 50, you can define offset as either 0, 50, 100, 150, or any multiple of 50. | [optional] 
 **type** | **str**| The action that was performed in the account, such as ACCOUNT_LOGIN | [optional] 

### Return type

[**list[AuditRecord]**](AuditRecord.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

