# swagger_client.TopSourcesApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_top_sources_stats**](TopSourcesApi.md#get_all_top_sources_stats) | **POST** /v2/sites/{siteId}/stats/top | Get all the top stats (country, client, reputation, successful user, ip, ip+fingerprint).
[**get_top_clients**](TopSourcesApi.md#get_top_clients) | **POST** /v2/sites/{siteId}/stats/top/client | Get top number of requests by client of unique users for the current time period compared to previous time period
[**get_top_countries**](TopSourcesApi.md#get_top_countries) | **POST** /v2/sites/{siteId}/stats/top/country | Get top number of requests by country of unique users for the current time period compared to previous time period
[**get_top_ips**](TopSourcesApi.md#get_top_ips) | **POST** /v2/sites/{siteId}/stats/top/ip | Get top number of requests by IP of unique users for the current time period compared to previous time period
[**get_top_ips_fps**](TopSourcesApi.md#get_top_ips_fps) | **POST** /v2/sites/{siteId}/stats/top/ip-fingerprint | Get top number of requests by IP + Fingerprint of unique users for the current time period compared to previous time period
[**get_top_reputation**](TopSourcesApi.md#get_top_reputation) | **POST** /v2/sites/{siteId}/stats/top/reputation | Get top number of requests by reputation of unique users for the current time period compared to previous time period

# **get_all_top_sources_stats**
> TopStats get_all_top_sources_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get all the top stats (country, client, reputation, successful user, ip, ip+fingerprint).

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.TopSourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get all the top stats (country, client, reputation, successful user, ip, ip+fingerprint).
    api_response = api_instance.get_all_top_sources_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TopSourcesApi->get_all_top_sources_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**TopStats**](TopStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_top_clients**
> TopSource get_top_clients(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get top number of requests by client of unique users for the current time period compared to previous time period

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.TopSourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get top number of requests by client of unique users for the current time period compared to previous time period
    api_response = api_instance.get_top_clients(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TopSourcesApi->get_top_clients: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**TopSource**](TopSource.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_top_countries**
> TopSource get_top_countries(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get top number of requests by country of unique users for the current time period compared to previous time period

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.TopSourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get top number of requests by country of unique users for the current time period compared to previous time period
    api_response = api_instance.get_top_countries(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TopSourcesApi->get_top_countries: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**TopSource**](TopSource.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_top_ips**
> TopSource get_top_ips(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get top number of requests by IP of unique users for the current time period compared to previous time period

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.TopSourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get top number of requests by IP of unique users for the current time period compared to previous time period
    api_response = api_instance.get_top_ips(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TopSourcesApi->get_top_ips: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**TopSource**](TopSource.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_top_ips_fps**
> TopSource get_top_ips_fps(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get top number of requests by IP + Fingerprint of unique users for the current time period compared to previous time period

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.TopSourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get top number of requests by IP + Fingerprint of unique users for the current time period compared to previous time period
    api_response = api_instance.get_top_ips_fps(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TopSourcesApi->get_top_ips_fps: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**TopSource**](TopSource.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_top_reputation**
> TopSource get_top_reputation(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get top number of requests by reputation of unique users for the current time period compared to previous time period

If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.TopSourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get top number of requests by reputation of unique users for the current time period compared to previous time period
    api_response = api_instance.get_top_reputation(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TopSourcesApi->get_top_reputation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**TopSource**](TopSource.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

