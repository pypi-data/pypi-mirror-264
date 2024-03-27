# swagger_client.UsersApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_aggregators_stats**](UsersApi.md#get_aggregators_stats) | **POST** /v2/sites/{siteId}/stats/users/aggregators | Get aggregators successful requests of unique users for the current time period compared to previous time period
[**get_all_unique_users_stats**](UsersApi.md#get_all_unique_users_stats) | **POST** /v2/sites/{siteId}/stats/users | Get all the unique users stats (leaked, aggregator, likely-leaked, suspicious-successful).
[**get_leaked_stats**](UsersApi.md#get_leaked_stats) | **POST** /v2/sites/{siteId}/stats/users/leaked | Get leaked successful requests of unique users for the current time period compared to previous time period
[**get_likely_leaked_credentials_stats**](UsersApi.md#get_likely_leaked_credentials_stats) | **POST** /v2/sites/{siteId}/stats/users/likely-leaked | Get likely leaked successful requests of unique users for the current time period compared to previous time period
[**get_suspicious_successful_stats**](UsersApi.md#get_suspicious_successful_stats) | **POST** /v2/sites/{siteId}/stats/users/suspicious-successful | Get suspicious successful requests of unique users for the current time period compared to previous time period

# **get_aggregators_stats**
> UsersStats get_aggregators_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get aggregators successful requests of unique users for the current time period compared to previous time period

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
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 789 # int |  (optional)

try:
    # Get aggregators successful requests of unique users for the current time period compared to previous time period
    api_response = api_instance.get_aggregators_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_aggregators_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **int**|  | [optional] 

### Return type

[**UsersStats**](UsersStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_unique_users_stats**
> AllUserStats get_all_unique_users_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get all the unique users stats (leaked, aggregator, likely-leaked, suspicious-successful).

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
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get all the unique users stats (leaked, aggregator, likely-leaked, suspicious-successful).
    api_response = api_instance.get_all_unique_users_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_all_unique_users_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**AllUserStats**](AllUserStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_leaked_stats**
> UsersStats get_leaked_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get leaked successful requests of unique users for the current time period compared to previous time period

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
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 789 # int |  (optional)

try:
    # Get leaked successful requests of unique users for the current time period compared to previous time period
    api_response = api_instance.get_leaked_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_leaked_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **int**|  | [optional] 

### Return type

[**UsersStats**](UsersStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_likely_leaked_credentials_stats**
> UsersStats get_likely_leaked_credentials_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get likely leaked successful requests of unique users for the current time period compared to previous time period

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
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 'endpoint_id_example' # str |  (optional)

try:
    # Get likely leaked successful requests of unique users for the current time period compared to previous time period
    api_response = api_instance.get_likely_leaked_credentials_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_likely_leaked_credentials_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **str**|  | [optional] 

### Return type

[**UsersStats**](UsersStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_suspicious_successful_stats**
> UsersStats get_suspicious_successful_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)

Get suspicious successful requests of unique users for the current time period compared to previous time period

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
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatsRequest() # StatsRequest | Specify the time selection
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)
endpoint_id = 789 # int |  (optional)

try:
    # Get suspicious successful requests of unique users for the current time period compared to previous time period
    api_response = api_instance.get_suspicious_successful_stats(body, site_id, caid=caid, endpoint_id=endpoint_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_suspicious_successful_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatsRequest**](StatsRequest.md)| Specify the time selection | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]
 **endpoint_id** | **int**|  | [optional] 

### Return type

[**UsersStats**](UsersStats.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

