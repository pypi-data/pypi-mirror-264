# swagger_client.AttackAnalyticsApi

All URIs are relative to *https://api.imperva.com/analytics*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_incident_stats_by_account**](AttackAnalyticsApi.md#get_incident_stats_by_account) | **GET** /v1/incidents/{incidentId}/stats | Retrieve incident details
[**get_incidents_by_account**](AttackAnalyticsApi.md#get_incidents_by_account) | **GET** /v1/incidents | Retrieve a list of incidents
[**get_insights_per_account**](AttackAnalyticsApi.md#get_insights_per_account) | **GET** /v1/insights | Retrieve insights
[**get_sample_events_by_incident**](AttackAnalyticsApi.md#get_sample_events_by_incident) | **GET** /v1/incidents/{incidentId}/sample-events | Retrieve event sample

# **get_incident_stats_by_account**
> IncidentStats get_incident_stats_by_account(caid, incident_id)

Retrieve incident details

Retrieves full details of a specified incident.

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
api_instance = swagger_client.AttackAnalyticsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
incident_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | The incident identifier.

try:
    # Retrieve incident details
    api_response = api_instance.get_incident_stats_by_account(caid, incident_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAnalyticsApi->get_incident_stats_by_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **incident_id** | [**str**](.md)| The incident identifier. | 

### Return type

[**IncidentStats**](IncidentStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_incidents_by_account**
> list[Incident] get_incidents_by_account(caid, from_timestamp=from_timestamp, to_timestamp=to_timestamp)

Retrieve a list of incidents

Retrieves Attack Analytics details for an account during a specified time period.

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
api_instance = swagger_client.AttackAnalyticsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Account ID. Unique identifier of the account to operate on.
from_timestamp = 789 # int | Earliest time boundary, specified as number of milliseconds since midnight 1970 (UNIX time * 1000). (optional)
to_timestamp = 789 # int | Latest time boundary, specified as number of milliseconds since midnight 1970 (UNIX time * 1000). (optional)

try:
    # Retrieve a list of incidents
    api_response = api_instance.get_incidents_by_account(caid, from_timestamp=from_timestamp, to_timestamp=to_timestamp)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAnalyticsApi->get_incidents_by_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Account ID. Unique identifier of the account to operate on. | 
 **from_timestamp** | **int**| Earliest time boundary, specified as number of milliseconds since midnight 1970 (UNIX time * 1000). | [optional] 
 **to_timestamp** | **int**| Latest time boundary, specified as number of milliseconds since midnight 1970 (UNIX time * 1000). | [optional] 

### Return type

[**list[Incident]**](Incident.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_insights_per_account**
> list[InsightsDataApi] get_insights_per_account(caid)

Retrieve insights

Retrieves the list of insights for your account (recommended actions to take based on attacks that have targeted your sites and applications).

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
api_instance = swagger_client.AttackAnalyticsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Unique account id

try:
    # Retrieve insights
    api_response = api_instance.get_insights_per_account(caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAnalyticsApi->get_insights_per_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Unique account id | 

### Return type

[**list[InsightsDataApi]**](InsightsDataApi.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sample_events_by_incident**
> Event get_sample_events_by_incident(caid, incident_id)

Retrieve event sample

Retrieves a sampling of events in a specified incident.

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
api_instance = swagger_client.AttackAnalyticsApi(swagger_client.ApiClient(configuration))
caid = 789 # int | Unique identifier of the account to operate on
incident_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | The incident identifier

try:
    # Retrieve event sample
    api_response = api_instance.get_sample_events_by_incident(caid, incident_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttackAnalyticsApi->get_sample_events_by_incident: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **caid** | **int**| Unique identifier of the account to operate on | 
 **incident_id** | [**str**](.md)| The incident identifier | 

### Return type

[**Event**](Event.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

