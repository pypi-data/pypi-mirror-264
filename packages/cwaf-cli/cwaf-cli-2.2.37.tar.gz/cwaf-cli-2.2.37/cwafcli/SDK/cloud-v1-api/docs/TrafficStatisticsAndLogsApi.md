# swagger_client.TrafficStatisticsAndLogsApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**change_logs_collectors_config_status**](TrafficStatisticsAndLogsApi.md#change_logs_collectors_config_status) | **POST** /api/logscollector/change/status | Change logs collector configuration status
[**get_infra_events**](TrafficStatisticsAndLogsApi.md#get_infra_events) | **POST** /api/v1/infra/events | Get infrastructure protection events
[**get_infra_protect_histogram**](TrafficStatisticsAndLogsApi.md#get_infra_protect_histogram) | **POST** /api/v1/infra/histogram | Get infrastructure protection histogram
[**get_infra_protect_top_data**](TrafficStatisticsAndLogsApi.md#get_infra_protect_top_data) | **POST** /api/v1/infra/top-graph | Get infrastructure protection top items (graph view)
[**get_infra_protect_top_table**](TrafficStatisticsAndLogsApi.md#get_infra_protect_top_table) | **POST** /api/v1/infra/top-table | Get infrastructure protection top items (table view)
[**get_infra_stats**](TrafficStatisticsAndLogsApi.md#get_infra_stats) | **POST** /api/v1/infra/stats | Get infrastructure protection statistics
[**get_stats**](TrafficStatisticsAndLogsApi.md#get_stats) | **POST** /api/stats/v1 | Get statistics
[**get_visits**](TrafficStatisticsAndLogsApi.md#get_visits) | **POST** /api/visits/v1 | Get visits
[**upload_lc_public_key**](TrafficStatisticsAndLogsApi.md#upload_lc_public_key) | **POST** /api/logscollector/upload/publickey | Upload public key

# **change_logs_collectors_config_status**
> ApiResult change_logs_collectors_config_status(config_id, logs_config_new_status)

Change logs collector configuration status

Change the status of the Logs Collector configuration.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
config_id = 'config_id_example' # str | The Logs Collector configuration identifier.
logs_config_new_status = 'logs_config_new_status_example' # str | The new configuration status of the Logs Collector. Possible values: ACTIVE, SUSPENDED

try:
    # Change logs collector configuration status
    api_response = api_instance.change_logs_collectors_config_status(config_id, logs_config_new_status)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->change_logs_collectors_config_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **config_id** | **str**| The Logs Collector configuration identifier. | 
 **logs_config_new_status** | **str**| The new configuration status of the Logs Collector. Possible values: ACTIVE, SUSPENDED | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_infra_events**
> InlineResponse2005 get_infra_events(account_id=account_id, event_type=event_type, ip_prefix=ip_prefix, page_size=page_size, page_num=page_num, start=start, end=end)

Get infrastructure protection events

Use this operation to get Infrastructure Protection event information for an account

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
event_type = 'event_type_example' # str | A comma separated list of specific event types. Any of: GRE_TUNNEL_UP, GRE_TUNNEL_DOWN, ORIGIN_CONNECTION_GRE_UP, ORIGIN_CONNECTION_GRE_DOWN, ORIGIN_CONNECTION_ECX_UP, ORIGIN_CONNECTION_ECX_DOWN, ORIGIN_CONNECTION_CROSS_CONNECT_UP, ORIGIN_CONNECTION_CROSS_CONNECT_DOWN, DDOS_START_IP_RANGE, DDOS_STOP_IP_RANGE, DDOS_QUIET_TIME_IP_RANGE, EXPORTER_NO_DATA, EXPORTER_BAD_DATA, EXPORTER_GOOD_DATA, MONITORING_CRITICAL_ATTACK, PROTECTED_IP_STATUS_UP, PROTECTED_IP_STATUS_DOWN, PER_IP_DDOS_START_IP_RANGE. (optional)
ip_prefix = 'ip_prefix_example' # str | Specific Protected IP or IP range. For example, 1.1.1.0/24. (optional)
page_size = 'page_size_example' # str | The number of objects to return in the response.<br/>Default: 50<br/>Maximum: 100 (optional)
page_num = 'page_num_example' # str | The page to return starting from 0. Default: 0 (optional)
start = 'start_example' # str | The start date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)
end = 'end_example' # str | The end date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)

try:
    # Get infrastructure protection events
    api_response = api_instance.get_infra_events(account_id=account_id, event_type=event_type, ip_prefix=ip_prefix, page_size=page_size, page_num=page_num, start=start, end=end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_infra_events: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **event_type** | **str**| A comma separated list of specific event types. Any of: GRE_TUNNEL_UP, GRE_TUNNEL_DOWN, ORIGIN_CONNECTION_GRE_UP, ORIGIN_CONNECTION_GRE_DOWN, ORIGIN_CONNECTION_ECX_UP, ORIGIN_CONNECTION_ECX_DOWN, ORIGIN_CONNECTION_CROSS_CONNECT_UP, ORIGIN_CONNECTION_CROSS_CONNECT_DOWN, DDOS_START_IP_RANGE, DDOS_STOP_IP_RANGE, DDOS_QUIET_TIME_IP_RANGE, EXPORTER_NO_DATA, EXPORTER_BAD_DATA, EXPORTER_GOOD_DATA, MONITORING_CRITICAL_ATTACK, PROTECTED_IP_STATUS_UP, PROTECTED_IP_STATUS_DOWN, PER_IP_DDOS_START_IP_RANGE. | [optional] 
 **ip_prefix** | **str**| Specific Protected IP or IP range. For example, 1.1.1.0/24. | [optional] 
 **page_size** | **str**| The number of objects to return in the response.&lt;br/&gt;Default: 50&lt;br/&gt;Maximum: 100 | [optional] 
 **page_num** | **str**| The page to return starting from 0. Default: 0 | [optional] 
 **start** | **str**| The start date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 
 **end** | **str**| The end date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_infra_protect_histogram**
> InlineResponse2006 get_infra_protect_histogram(ip_range, range_type, start, end, mitigation_type, account_id=account_id, data_storage_region=data_storage_region)

Get infrastructure protection histogram

Use this operation to view the highest packet size values for a protected IP range during a selected time period.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
ip_range = 'ip_range_example' # str | The customer's IP range.
range_type = 'range_type_example' # str | One of the following: BGP, PROTECTED_IP, NETFLOW
start = 789 # int | The start date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
end = 789 # int | The end date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
mitigation_type = 'mitigation_type_example' # str | One of the following: BLOCK, PASS
account_id = 789 # int | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
data_storage_region = 'data_storage_region_example' # str | The data region to use. If not specified, account's default data region will be used. (optional)

try:
    # Get infrastructure protection histogram
    api_response = api_instance.get_infra_protect_histogram(ip_range, range_type, start, end, mitigation_type, account_id=account_id, data_storage_region=data_storage_region)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_infra_protect_histogram: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_range** | **str**| The customer&#x27;s IP range. | 
 **range_type** | **str**| One of the following: BGP, PROTECTED_IP, NETFLOW | 
 **start** | **int**| The start date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **end** | **int**| The end date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **mitigation_type** | **str**| One of the following: BLOCK, PASS | 
 **account_id** | **int**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **data_storage_region** | **str**| The data region to use. If not specified, account&#x27;s default data region will be used. | [optional] 

### Return type

[**InlineResponse2006**](InlineResponse2006.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_infra_protect_top_data**
> InlineResponse2007 get_infra_protect_top_data(ip_range, range_type, start, end, data_type, metric_type, mitigation_type, account_id=account_id, data_storage_region=data_storage_region, objects=objects)

Get infrastructure protection top items (graph view)

Use this operation to view the highest peak values and highest average values for a protected IP range during a selected time period.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
ip_range = 'ip_range_example' # str | The customer's IP range.
range_type = 'range_type_example' # str | One of the following: BGP, PROTECTED_IP, NETFLOW
start = 789 # int | The start date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
end = 789 # int | The end date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
data_type = 'data_type_example' # str | One of the following: SRC_IP, DST_IP, SRC_PORT_PROTOCOL, DST_PORT_PROTOCOL
metric_type = 'metric_type_example' # str | One of the following: BW, PPS
mitigation_type = 'mitigation_type_example' # str | One of the following: BLOCK, PASS
account_id = 789 # int | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
data_storage_region = 'data_storage_region_example' # str | The data region to use. If not specified, account's default data region will be used. (optional)
objects = 'objects_example' # str | A comma separated list of items to fetch data for. e.g., 10.10.10.10, 2.2.2.2. If not specified, top items are automatically fetched. (optional)

try:
    # Get infrastructure protection top items (graph view)
    api_response = api_instance.get_infra_protect_top_data(ip_range, range_type, start, end, data_type, metric_type, mitigation_type, account_id=account_id, data_storage_region=data_storage_region, objects=objects)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_infra_protect_top_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_range** | **str**| The customer&#x27;s IP range. | 
 **range_type** | **str**| One of the following: BGP, PROTECTED_IP, NETFLOW | 
 **start** | **int**| The start date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **end** | **int**| The end date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **data_type** | **str**| One of the following: SRC_IP, DST_IP, SRC_PORT_PROTOCOL, DST_PORT_PROTOCOL | 
 **metric_type** | **str**| One of the following: BW, PPS | 
 **mitigation_type** | **str**| One of the following: BLOCK, PASS | 
 **account_id** | **int**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **data_storage_region** | **str**| The data region to use. If not specified, account&#x27;s default data region will be used. | [optional] 
 **objects** | **str**| A comma separated list of items to fetch data for. e.g., 10.10.10.10, 2.2.2.2. If not specified, top items are automatically fetched. | [optional] 

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_infra_protect_top_table**
> InlineResponse2008 get_infra_protect_top_table(ip_range, range_type, start, end, data_type, metric_type, mitigation_type, aggregation_type, account_id=account_id, data_storage_region=data_storage_region)

Get infrastructure protection top items (table view)

Use this operation to view the highest peak values and highest average values for a protected IP range during a selected time period.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
ip_range = 'ip_range_example' # str | The customer's IP range.
range_type = 'range_type_example' # str | One of the following: BGP, PROTECTED_IP, NETFLOW
start = 789 # int | The start date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
end = 789 # int | The end date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
data_type = 'data_type_example' # str | One of the following: SRC_IP, DST_IP, SRC_PORT_PROTOCOL, DST_PORT_PROTOCOL
metric_type = 'metric_type_example' # str | One of the following: SRC_IP, DST_IP, SRC_PORT_PROTOCOL, DST_PORT_PROTOCOL
mitigation_type = 'mitigation_type_example' # str | One of the following: BLOCK, PASS
aggregation_type = 'aggregation_type_example' # str | One of the following: PEAK, AVERAGE
account_id = 789 # int | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
data_storage_region = 'data_storage_region_example' # str | The data region to use. If not specified, account's default data region will be used. (optional)

try:
    # Get infrastructure protection top items (table view)
    api_response = api_instance.get_infra_protect_top_table(ip_range, range_type, start, end, data_type, metric_type, mitigation_type, aggregation_type, account_id=account_id, data_storage_region=data_storage_region)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_infra_protect_top_table: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_range** | **str**| The customer&#x27;s IP range. | 
 **range_type** | **str**| One of the following: BGP, PROTECTED_IP, NETFLOW | 
 **start** | **int**| The start date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **end** | **int**| The end date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **data_type** | **str**| One of the following: SRC_IP, DST_IP, SRC_PORT_PROTOCOL, DST_PORT_PROTOCOL | 
 **metric_type** | **str**| One of the following: SRC_IP, DST_IP, SRC_PORT_PROTOCOL, DST_PORT_PROTOCOL | 
 **mitigation_type** | **str**| One of the following: BLOCK, PASS | 
 **aggregation_type** | **str**| One of the following: PEAK, AVERAGE | 
 **account_id** | **int**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **data_storage_region** | **str**| The data region to use. If not specified, account&#x27;s default data region will be used. | [optional] 

### Return type

[**InlineResponse2008**](InlineResponse2008.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_infra_stats**
> InlineResponse2009 get_infra_stats(account_id=account_id, ip_prefix=ip_prefix, traffic=traffic, traffic_type=traffic_type, pop=pop, start=start, end=end, direction_types=direction_types, range_type=range_type)

Get infrastructure protection statistics

Use this operation to get Infrastructure Protection event information for an account.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
ip_prefix = 'ip_prefix_example' # str | Specific Protected IP or IP range. For example, 1.1.1.0/24. (optional)
traffic = 'traffic_example' # str | Specific traffic. One of: Total, Passed, Blocked. (optional)
traffic_type = 'traffic_type_example' # str | A comma separated list of specific traffic types. Any of: UDP, TCP, DNS, DNS_RESPONSE, ICMP, SYN, FRAG, LARGE_SYN, NTP, NETFLOW, SSDP, GENERAL. Cannot be used together with the pop parameter. (optional)
pop = 'pop_example' # str | A comma separated list of specific PoP names. For example: iad, tko. Cannot be used together with the traffic_type parameter. For the list of PoP codes and locations, see <a href=\"https://docs.imperva.com/csh?context=pops\">Imperva Data Centers (PoPs)</a>. (optional)
start = 789 # int | The start date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)
end = 789 # int | The end date in milliseconds, since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)
direction_types = 'direction_types_example' # str | The type of direction(INGRESS/EGRESS) to filter the data (optional)
range_type = 'range_type_example' # str | Can be one of the following: BGP, PROTECTED_IP, NETFLOW (optional)

try:
    # Get infrastructure protection statistics
    api_response = api_instance.get_infra_stats(account_id=account_id, ip_prefix=ip_prefix, traffic=traffic, traffic_type=traffic_type, pop=pop, start=start, end=end, direction_types=direction_types, range_type=range_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_infra_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **ip_prefix** | **str**| Specific Protected IP or IP range. For example, 1.1.1.0/24. | [optional] 
 **traffic** | **str**| Specific traffic. One of: Total, Passed, Blocked. | [optional] 
 **traffic_type** | **str**| A comma separated list of specific traffic types. Any of: UDP, TCP, DNS, DNS_RESPONSE, ICMP, SYN, FRAG, LARGE_SYN, NTP, NETFLOW, SSDP, GENERAL. Cannot be used together with the pop parameter. | [optional] 
 **pop** | **str**| A comma separated list of specific PoP names. For example: iad, tko. Cannot be used together with the traffic_type parameter. For the list of PoP codes and locations, see &lt;a href&#x3D;\&quot;https://docs.imperva.com/csh?context&#x3D;pops\&quot;&gt;Imperva Data Centers (PoPs)&lt;/a&gt;. | [optional] 
 **start** | **int**| The start date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 
 **end** | **int**| The end date in milliseconds, since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 
 **direction_types** | **str**| The type of direction(INGRESS/EGRESS) to filter the data | [optional] 
 **range_type** | **str**| Can be one of the following: BGP, PROTECTED_IP, NETFLOW | [optional] 

### Return type

[**InlineResponse2009**](InlineResponse2009.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_stats**
> InlineResponse20010 get_stats(time_range, stats, account_id=account_id, start=start, end=end, site_id=site_id, granularity=granularity)

Get statistics

Get site statistics for one or more sites. This operation may return multiple statistics, as specified in the stats parameter.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
time_range = 'time_range_example' # str | Time range to fetch data for.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul>
stats = 'stats_example' # str | Statistics to fetch, as specified in the table below. Multiple statistics can be specified in a comma separated list.<br/>Values for the stats parameters:<br/><ul><li><b>visits_timeseries</b> Number of sessions by type (Humans/Bots) over time.</li><li><b>hits_timeseries</b> Number of requests by type (Humans/Bots/Blocked) over time and per second.</li><li><b>bandwidth_timeseries</b> Amount of bytes (bandwidth) and bits per second (throughput) transferred via the Imperva network from clients to proxy servers and vice-versa over time.</li><li><b>requests_geo_dist_summary</b> Total number of requests routed via the Imperva network by data center location.</li><li><b>visits_dist_summary</b> Total number of sessions per client application and country.</li><li><b>caching</b> Total number of requests and bytes that were cached by the Imperva network.</li><li><b>caching_timeseries</b> Number of requests and bytes that were cached by the Imperva network, with one day resolution, with info regarding the caching mode (standard or advanced).</li><li><b>threats</b> Total number of threats by type with additional information regarding the security rules configuration.</li><li><b>incap_rules</b> List of security rules with total number of reported incidents for each rule.</li><li><b>incap_rules_timeseries</b> List of security rules with a series of reported incidents for each rule with the specified granularity.</li><li><b>delivery_rules</b> List of delivery rules with total number of hits for each rule.</li><li><b>delivery_rules_timeseries</b> List of delivery rules with a series of hits for each rule with the specified granularity.</li></ul>
account_id = 'account_id_example' # str | Numeric identifier of the account to fetch data for.<br/>Note: You must specify either account_id or site_id. (optional)
start = 'start_example' # str | Start date in milliseconds since January 1, 1970 (midnight UTC/GMT). Used together with the time_range parameter to specify a custom time range. (optional)
end = 'end_example' # str | End date in milliseconds since January 1, 1970 (midnight UTC/GMT). Used together with the time_range parameter to specify a custom time range. (optional)
site_id = 'site_id_example' # str | Numeric identifier of the site to fetch data for. Multiple sites can be specified in a comma separated list. For example: 123,124,125.<br/>Note: You must specify either account_id or site_id. (optional)
granularity = 'granularity_example' # str | Time interval in milliseconds between data points for time series statistics. (See the timeseries values in the table below.)<br/>The default granularity depends on the specified time range, as follows:<br/><ul><li>Time range of less than 24 hours: Default granularity is 7200000 (2 hours).</li><li>Time range of between 24 hours and 30 days: Default granularity is 86400000 (1 day).</li><li>Time range of more than 30 days: Default granularity is 259200000 (3 days).</li></ul>The response includes one result for each interval. For example, if you specify a time range value of last_7_days, the default granularity is 1 day, and the response will return 7 results.<br/>The response timestamps are in milliseconds since January 1, 1970 (midnight UTC/GMT)<br/>Minimum granularity is 5 minutes (300000).<br/>Note: Time series statistics are presented oldest to newest.<br/> (optional)

try:
    # Get statistics
    api_response = api_instance.get_stats(time_range, stats, account_id=account_id, start=start, end=end, site_id=site_id, granularity=granularity)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **time_range** | **str**| Time range to fetch data for.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | 
 **stats** | **str**| Statistics to fetch, as specified in the table below. Multiple statistics can be specified in a comma separated list.&lt;br/&gt;Values for the stats parameters:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;visits_timeseries&lt;/b&gt; Number of sessions by type (Humans/Bots) over time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;hits_timeseries&lt;/b&gt; Number of requests by type (Humans/Bots/Blocked) over time and per second.&lt;/li&gt;&lt;li&gt;&lt;b&gt;bandwidth_timeseries&lt;/b&gt; Amount of bytes (bandwidth) and bits per second (throughput) transferred via the Imperva network from clients to proxy servers and vice-versa over time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;requests_geo_dist_summary&lt;/b&gt; Total number of requests routed via the Imperva network by data center location.&lt;/li&gt;&lt;li&gt;&lt;b&gt;visits_dist_summary&lt;/b&gt; Total number of sessions per client application and country.&lt;/li&gt;&lt;li&gt;&lt;b&gt;caching&lt;/b&gt; Total number of requests and bytes that were cached by the Imperva network.&lt;/li&gt;&lt;li&gt;&lt;b&gt;caching_timeseries&lt;/b&gt; Number of requests and bytes that were cached by the Imperva network, with one day resolution, with info regarding the caching mode (standard or advanced).&lt;/li&gt;&lt;li&gt;&lt;b&gt;threats&lt;/b&gt; Total number of threats by type with additional information regarding the security rules configuration.&lt;/li&gt;&lt;li&gt;&lt;b&gt;incap_rules&lt;/b&gt; List of security rules with total number of reported incidents for each rule.&lt;/li&gt;&lt;li&gt;&lt;b&gt;incap_rules_timeseries&lt;/b&gt; List of security rules with a series of reported incidents for each rule with the specified granularity.&lt;/li&gt;&lt;li&gt;&lt;b&gt;delivery_rules&lt;/b&gt; List of delivery rules with total number of hits for each rule.&lt;/li&gt;&lt;li&gt;&lt;b&gt;delivery_rules_timeseries&lt;/b&gt; List of delivery rules with a series of hits for each rule with the specified granularity.&lt;/li&gt;&lt;/ul&gt; | 
 **account_id** | **str**| Numeric identifier of the account to fetch data for.&lt;br/&gt;Note: You must specify either account_id or site_id. | [optional] 
 **start** | **str**| Start date in milliseconds since January 1, 1970 (midnight UTC/GMT). Used together with the time_range parameter to specify a custom time range. | [optional] 
 **end** | **str**| End date in milliseconds since January 1, 1970 (midnight UTC/GMT). Used together with the time_range parameter to specify a custom time range. | [optional] 
 **site_id** | **str**| Numeric identifier of the site to fetch data for. Multiple sites can be specified in a comma separated list. For example: 123,124,125.&lt;br/&gt;Note: You must specify either account_id or site_id. | [optional] 
 **granularity** | **str**| Time interval in milliseconds between data points for time series statistics. (See the timeseries values in the table below.)&lt;br/&gt;The default granularity depends on the specified time range, as follows:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;Time range of less than 24 hours: Default granularity is 7200000 (2 hours).&lt;/li&gt;&lt;li&gt;Time range of between 24 hours and 30 days: Default granularity is 86400000 (1 day).&lt;/li&gt;&lt;li&gt;Time range of more than 30 days: Default granularity is 259200000 (3 days).&lt;/li&gt;&lt;/ul&gt;The response includes one result for each interval. For example, if you specify a time range value of last_7_days, the default granularity is 1 day, and the response will return 7 results.&lt;br/&gt;The response timestamps are in milliseconds since January 1, 1970 (midnight UTC/GMT)&lt;br/&gt;Minimum granularity is 5 minutes (300000).&lt;br/&gt;Note: Time series statistics are presented oldest to newest.&lt;br/&gt; | [optional] 

### Return type

[**InlineResponse20010**](InlineResponse20010.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_visits**
> InlineResponse20011 get_visits(site_id, time_range=time_range, start=start, end=end, page_size=page_size, page_num=page_num, security=security, country=country, ip=ip, visit_id=visit_id, list_live_visits=list_live_visits, use_previous_region=use_previous_region)

Get visits

Use this operation to get a log of recent visits to a website.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
site_id = 'site_id_example' # str | Numeric identifier of the site to operate on.
time_range = 'time_range_example' # str | Time range to fetch data for. Default is last_7_days.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)
start = 'start_example' # str | Start date in milliseconds since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)
end = 'end_example' # str | End date in milliseconds since 1970.<br/>Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:<br/><ul><li><b>today</b> Retrieve data from midnight today until the current time.</li><li><b>last_7_days</b> Retrieve data from midnight of 7 days ago until the current time.</li><li><b>last_30_days</b> Retrieve data from midnight of 30 days ago until the current time.</li><li><b>last_90_days</b> Retrieve data from midnight of 90 days ago until the current time.</li><li><b>month_to_date</b> Retrieve data from midnight of the first day of the month until the current time.</li><li><b>custom</b> Specify a custom time range using two additional parameters: start and end.<br/>Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.<br/>For example:<ul><li>A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.</li><li>A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.</li> <li>A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.</li></ul></li></ul> (optional)
page_size = 'page_size_example' # str | The number of objects to return in the response. Defaults to 10. Maximum is 100. (optional)
page_num = 'page_num_example' # str | The page to return starting from 0. Default to 0. (optional)
security = 'security_example' # str | Filter the sessions that were handled according to the security-related specifications. Multiple values are supported, e.g.: \"api.threats.sql_injection, api.acl.blacklisted_ips\". (optional)
country = 'country_example' # str | Filter the sessions coming from the specified country. (optional)
ip = 'ip_example' # str | Filter the sessions coming from the specified IP. (optional)
visit_id = 'visit_id_example' # str | Comma separated list of visit IDs to load. (optional)
list_live_visits = 'list_live_visits_example' # str | Whether or not to list visits that did not end and that may still be updated.<br/>Possible values: true, false<br/>Default: true (optional)
use_previous_region = 'use_previous_region_example' # str | Whether or not to list visits from old region data. Valid only if a data region was changed in the last 90 days. One of: true | false. Default: false (optional)

try:
    # Get visits
    api_response = api_instance.get_visits(site_id, time_range=time_range, start=start, end=end, page_size=page_size, page_num=page_num, security=security, country=country, ip=ip, visit_id=visit_id, list_live_visits=list_live_visits, use_previous_region=use_previous_region)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->get_visits: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **str**| Numeric identifier of the site to operate on. | 
 **time_range** | **str**| Time range to fetch data for. Default is last_7_days.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 
 **start** | **str**| Start date in milliseconds since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 
 **end** | **str**| End date in milliseconds since 1970.&lt;br/&gt;Some operations require the user to specify a time range. This is done via the time_range parameter, which accepts the following values:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;today&lt;/b&gt; Retrieve data from midnight today until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_7_days&lt;/b&gt; Retrieve data from midnight of 7 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_30_days&lt;/b&gt; Retrieve data from midnight of 30 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;last_90_days&lt;/b&gt; Retrieve data from midnight of 90 days ago until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;month_to_date&lt;/b&gt; Retrieve data from midnight of the first day of the month until the current time.&lt;/li&gt;&lt;li&gt;&lt;b&gt;custom&lt;/b&gt; Specify a custom time range using two additional parameters: start and end.&lt;br/&gt;Results are provided for full days only, starting from midnight. A time range of less than 24 hours gives results for the full day.&lt;br/&gt;For example:&lt;ul&gt;&lt;li&gt;A time range of 14:00 - 20:00 yesterday gives results for all of yesterday (midnight to midnight) - a full day.&lt;/li&gt;&lt;li&gt;A time range of 14:00 last Tuesday to 14:00 last Wednesday gives results for all of Tuesday and Wednesday - two full days.&lt;/li&gt; &lt;li&gt;A time range of 14:00 yesterday to 14:00 today gives results for all of yesterday starting from midnight until the current time today.&lt;/li&gt;&lt;/ul&gt;&lt;/li&gt;&lt;/ul&gt; | [optional] 
 **page_size** | **str**| The number of objects to return in the response. Defaults to 10. Maximum is 100. | [optional] 
 **page_num** | **str**| The page to return starting from 0. Default to 0. | [optional] 
 **security** | **str**| Filter the sessions that were handled according to the security-related specifications. Multiple values are supported, e.g.: \&quot;api.threats.sql_injection, api.acl.blacklisted_ips\&quot;. | [optional] 
 **country** | **str**| Filter the sessions coming from the specified country. | [optional] 
 **ip** | **str**| Filter the sessions coming from the specified IP. | [optional] 
 **visit_id** | **str**| Comma separated list of visit IDs to load. | [optional] 
 **list_live_visits** | **str**| Whether or not to list visits that did not end and that may still be updated.&lt;br/&gt;Possible values: true, false&lt;br/&gt;Default: true | [optional] 
 **use_previous_region** | **str**| Whether or not to list visits from old region data. Valid only if a data region was changed in the last 90 days. One of: true | false. Default: false | [optional] 

### Return type

[**InlineResponse20011**](InlineResponse20011.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_lc_public_key**
> InlineResponse20012 upload_lc_public_key(config_id, public_key)

Upload public key

Available only for Enterprise Plan customers that purchased the Security Logs Integration SKU.

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
api_instance = swagger_client.TrafficStatisticsAndLogsApi(swagger_client.ApiClient(configuration))
config_id = 'config_id_example' # str | The Logs Collector configuration identifier.
public_key = 'public_key_example' # str | The public key file (2048bit) in base64 format (without password protection).

try:
    # Upload public key
    api_response = api_instance.upload_lc_public_key(config_id, public_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrafficStatisticsAndLogsApi->upload_lc_public_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **config_id** | **str**| The Logs Collector configuration identifier. | 
 **public_key** | **str**| The public key file (2048bit) in base64 format (without password protection). | 

### Return type

[**InlineResponse20012**](InlineResponse20012.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

