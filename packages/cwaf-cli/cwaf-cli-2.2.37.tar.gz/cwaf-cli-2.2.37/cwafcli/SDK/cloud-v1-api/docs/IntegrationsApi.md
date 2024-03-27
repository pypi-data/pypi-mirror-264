# swagger_client.IntegrationsApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_clapps_info**](IntegrationsApi.md#get_clapps_info) | **POST** /api/integration/v1/clapps | Get client applications info
[**get_geo_info**](IntegrationsApi.md#get_geo_info) | **POST** /api/integration/v1/geo | Get geographical info
[**get_ip_ranges**](IntegrationsApi.md#get_ip_ranges) | **POST** /api/integration/v1/ips | Get Imperva IP ranges
[**get_texts**](IntegrationsApi.md#get_texts) | **POST** /api/integration/v1/texts | Get texts

# **get_clapps_info**
> ApiResultGetClappsInfo get_clapps_info()

Get client applications info

Use this operation to retrieve a list of all the client applications.

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
api_instance = swagger_client.IntegrationsApi(swagger_client.ApiClient(configuration))

try:
    # Get client applications info
    api_response = api_instance.get_clapps_info()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IntegrationsApi->get_clapps_info: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ApiResultGetClappsInfo**](ApiResultGetClappsInfo.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_geo_info**
> GeoInfo get_geo_info()

Get geographical info

Use this operation to retrieve a list of all the countries and continents codes.

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
api_instance = swagger_client.IntegrationsApi(swagger_client.ApiClient(configuration))

try:
    # Get geographical info
    api_response = api_instance.get_geo_info()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IntegrationsApi->get_geo_info: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GeoInfo**](GeoInfo.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ip_ranges**
> InlineResponse20013 get_ip_ranges(resp_format=resp_format)

Get Imperva IP ranges

Use this operation to get the updated list of Imperva IP ranges. This list may be used to define firewall rules that restrict access to customers sites from non-Imperva IPs.

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
api_instance = swagger_client.IntegrationsApi(swagger_client.ApiClient(configuration))
resp_format = 'resp_format_example' # str | Response format.<br/>Possible values: json | apache | nginx | iptables | text<br/>Default: json (optional)

try:
    # Get Imperva IP ranges
    api_response = api_instance.get_ip_ranges(resp_format=resp_format)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IntegrationsApi->get_ip_ranges: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resp_format** | **str**| Response format.&lt;br/&gt;Possible values: json | apache | nginx | iptables | text&lt;br/&gt;Default: json | [optional] 

### Return type

[**InlineResponse20013**](InlineResponse20013.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_texts**
> ApiResultGetTexts get_texts()

Get texts

Use this operation to retrieve a list of all text messages that may be part of API responses. For each message a key and a value are provided. The key is the unique identifier of the message and the value is the message text itself, in the API's default locale (English).

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
api_instance = swagger_client.IntegrationsApi(swagger_client.ApiClient(configuration))

try:
    # Get texts
    api_response = api_instance.get_texts()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IntegrationsApi->get_texts: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ApiResultGetTexts**](ApiResultGetTexts.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

