# swagger_client.DiscoveryStatisticsApi

All URIs are relative to *https://api.imperva.com/api-security*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dashboard_classification_statistics**](DiscoveryStatisticsApi.md#get_dashboard_classification_statistics) | **GET** /v2/discovery/statistics/classification/from/{from-timestamp}/to/{to-timestamp} | Retrieve account level baselined endpoints&#x27; classification statistics
[**get_dashboard_general_statistics**](DiscoveryStatisticsApi.md#get_dashboard_general_statistics) | **GET** /v2/discovery/statistics/usage/from/{from-timestamp}/to/{to-timestamp} | Retrieve account level baselined endpoints&#x27; usage statistics
[**get_dashboard_geolocation_statistics**](DiscoveryStatisticsApi.md#get_dashboard_geolocation_statistics) | **GET** /v2/discovery/statistics/geolocation/from/{from-timestamp}/to/{to-timestamp} | Retrieve account level baselined endpoints&#x27; geolocation statistics
[**get_dashboard_volume_stats**](DiscoveryStatisticsApi.md#get_dashboard_volume_stats) | **GET** /v2/discovery/statistics/volume/from/{from-timestamp}/to/{to-timestamp} | Retrieve account level baselined endpoints&#x27; volume statistics

# **get_dashboard_classification_statistics**
> GetDashboardClassificationStatisticsSuccessfulResponse get_dashboard_classification_statistics(from_timestamp, to_timestamp, host_ids=host_ids)

Retrieve account level baselined endpoints' classification statistics

Retrieve account level baselined endpoints' classification statistics

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
api_instance = swagger_client.DiscoveryStatisticsApi(swagger_client.ApiClient(configuration))
from_timestamp = 789 # int | Start Date or Start Time of the statistics  in milliseconds (epoch time).
to_timestamp = 789 # int | End Date or End Time of the statistics  in milliseconds (epoch time).
host_ids = 'host_ids_example' # str | Comma separated list of host ids (optional)

try:
    # Retrieve account level baselined endpoints' classification statistics
    api_response = api_instance.get_dashboard_classification_statistics(from_timestamp, to_timestamp, host_ids=host_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryStatisticsApi->get_dashboard_classification_statistics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_timestamp** | **int**| Start Date or Start Time of the statistics  in milliseconds (epoch time). | 
 **to_timestamp** | **int**| End Date or End Time of the statistics  in milliseconds (epoch time). | 
 **host_ids** | **str**| Comma separated list of host ids | [optional] 

### Return type

[**GetDashboardClassificationStatisticsSuccessfulResponse**](GetDashboardClassificationStatisticsSuccessfulResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dashboard_general_statistics**
> GetDashboardGeneralStatisticsSuccessfulResponse get_dashboard_general_statistics(from_timestamp, to_timestamp, host_ids=host_ids)

Retrieve account level baselined endpoints' usage statistics

Retrieve account level baselined endpoints' usage statistics

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
api_instance = swagger_client.DiscoveryStatisticsApi(swagger_client.ApiClient(configuration))
from_timestamp = 789 # int | Start Date or Start Time of the statistics  in milliseconds (epoch time).
to_timestamp = 789 # int | End Date or End Time of the statistics in milliseconds (epoch time).
host_ids = 'host_ids_example' # str | Comma separated list of host IDs (optional)

try:
    # Retrieve account level baselined endpoints' usage statistics
    api_response = api_instance.get_dashboard_general_statistics(from_timestamp, to_timestamp, host_ids=host_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryStatisticsApi->get_dashboard_general_statistics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_timestamp** | **int**| Start Date or Start Time of the statistics  in milliseconds (epoch time). | 
 **to_timestamp** | **int**| End Date or End Time of the statistics in milliseconds (epoch time). | 
 **host_ids** | **str**| Comma separated list of host IDs | [optional] 

### Return type

[**GetDashboardGeneralStatisticsSuccessfulResponse**](GetDashboardGeneralStatisticsSuccessfulResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dashboard_geolocation_statistics**
> GetDashboardGeolocationStatisticsSuccessfulResponse get_dashboard_geolocation_statistics(from_timestamp, to_timestamp, host_ids=host_ids)

Retrieve account level baselined endpoints' geolocation statistics

Retrieve account level baselined endpoints' geolocation statistics

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
api_instance = swagger_client.DiscoveryStatisticsApi(swagger_client.ApiClient(configuration))
from_timestamp = 789 # int | Start Date or Start Time of the statistics  in milliseconds (epoch time).
to_timestamp = 789 # int | End Date or End Time of the statistics  in milliseconds (epoch time).
host_ids = 'host_ids_example' # str | Comma separated list of host ids (optional)

try:
    # Retrieve account level baselined endpoints' geolocation statistics
    api_response = api_instance.get_dashboard_geolocation_statistics(from_timestamp, to_timestamp, host_ids=host_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryStatisticsApi->get_dashboard_geolocation_statistics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_timestamp** | **int**| Start Date or Start Time of the statistics  in milliseconds (epoch time). | 
 **to_timestamp** | **int**| End Date or End Time of the statistics  in milliseconds (epoch time). | 
 **host_ids** | **str**| Comma separated list of host ids | [optional] 

### Return type

[**GetDashboardGeolocationStatisticsSuccessfulResponse**](GetDashboardGeolocationStatisticsSuccessfulResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dashboard_volume_stats**
> GetDashboardVolumeStatisticsSuccessfulResponse get_dashboard_volume_stats(from_timestamp, to_timestamp, host_ids=host_ids)

Retrieve account level baselined endpoints' volume statistics

Retrieve account level baselined endpoints' volume statistics

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
api_instance = swagger_client.DiscoveryStatisticsApi(swagger_client.ApiClient(configuration))
from_timestamp = 789 # int | Start Date or Start Time of the statistics  in milliseconds (epoch time).
to_timestamp = 789 # int | End Date or End Time of the statistics  in milliseconds (epoch time).
host_ids = 'host_ids_example' # str | Comma separated list of host ids (optional)

try:
    # Retrieve account level baselined endpoints' volume statistics
    api_response = api_instance.get_dashboard_volume_stats(from_timestamp, to_timestamp, host_ids=host_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DiscoveryStatisticsApi->get_dashboard_volume_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_timestamp** | **int**| Start Date or Start Time of the statistics  in milliseconds (epoch time). | 
 **to_timestamp** | **int**| End Date or End Time of the statistics  in milliseconds (epoch time). | 
 **host_ids** | **str**| Comma separated list of host ids | [optional] 

### Return type

[**GetDashboardVolumeStatisticsSuccessfulResponse**](GetDashboardVolumeStatisticsSuccessfulResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

