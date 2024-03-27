# swagger_client.HSMCertificatesApi

All URIs are relative to *https://api.imperva.com/certificates-ui*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_latency**](HSMCertificatesApi.md#get_latency) | **GET** /v3/certificates/hsm/latency | Get HSM latency

# **get_latency**
> HsmLatencyDetailsResponse get_latency(pop, hsm_host_name)

Get HSM latency

Get the latest HSM latency between a given Imperva data center (PoP) and a specific Fortanix region.<br/>This operation returns the time it takes for Imperva to get the private key from Fortanix.It does not include the session creation time.

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
api_instance = swagger_client.HSMCertificatesApi(swagger_client.ApiClient(configuration))
pop = 'pop_example' # str | The code of the Imperva data center (PoP) to check latency for.<br/>For the full list of PoPs and codes, see <a href='https://docs.imperva.com/bundle/cloud-application-security/page/more/pops.htm'>Imperva Data Centers</a>.
hsm_host_name = 'hsm_host_name_example' # str | The URI (host name) of the Fortanix region.<br/>Possible values: amer, uk, eu, apac, au in the required format, e.g. api.amer.smartkey.io

try:
    # Get HSM latency
    api_response = api_instance.get_latency(pop, hsm_host_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HSMCertificatesApi->get_latency: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pop** | **str**| The code of the Imperva data center (PoP) to check latency for.&lt;br/&gt;For the full list of PoPs and codes, see &lt;a href&#x3D;&#x27;https://docs.imperva.com/bundle/cloud-application-security/page/more/pops.htm&#x27;&gt;Imperva Data Centers&lt;/a&gt;. | 
 **hsm_host_name** | **str**| The URI (host name) of the Fortanix region.&lt;br/&gt;Possible values: amer, uk, eu, apac, au in the required format, e.g. api.amer.smartkey.io | 

### Return type

[**HsmLatencyDetailsResponse**](HsmLatencyDetailsResponse.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

