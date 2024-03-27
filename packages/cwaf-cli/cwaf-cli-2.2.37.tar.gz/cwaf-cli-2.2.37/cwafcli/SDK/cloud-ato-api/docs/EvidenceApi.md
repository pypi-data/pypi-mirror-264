# swagger_client.EvidenceApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_aggregators_evidence**](EvidenceApi.md#get_aggregators_evidence) | **POST** /v2/sites/{siteId}/report/evidence/aggregators | Retrieve aggregated login report
[**get_all_evidence**](EvidenceApi.md#get_all_evidence) | **POST** /v2/sites/{siteId}/report/evidence | Retrieve report of all user logins
[**get_compromised_evidence**](EvidenceApi.md#get_compromised_evidence) | **POST** /v2/sites/{siteId}/report/evidence/suspicious-successful | Retrieve the compromised users login report
[**get_leaked_evidence**](EvidenceApi.md#get_leaked_evidence) | **POST** /v2/sites/{siteId}/report/evidence/leaked-creds | Retrieve the leaked users login report
[**get_likely_leaked_evidence**](EvidenceApi.md#get_likely_leaked_evidence) | **POST** /v2/sites/{siteId}/report/evidence/likely-leaked | Retrieve the likely leaked users login report
[**get_mitigated_evidence**](EvidenceApi.md#get_mitigated_evidence) | **POST** /v2/sites/{siteId}/report/evidence/mitigated-request | Retrieve the mitigated (CAPTCHA, BLOCK, TARPIT) users login report

# **get_aggregators_evidence**
> Evidence get_aggregators_evidence(body, site_id, caid=caid)

Retrieve aggregated login report

Retrieve the list of login events that were classified as coming from known aggregators. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.EvidenceApi(swagger_client.ApiClient(configuration))
body = swagger_client.EvidenceRequest() # EvidenceRequest | Specify the time selection and/or endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve aggregated login report
    api_response = api_instance.get_aggregators_evidence(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EvidenceApi->get_aggregators_evidence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EvidenceRequest**](EvidenceRequest.md)| Specify the time selection and/or endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**Evidence**](Evidence.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_evidence**
> SuspiciousSuccessfulEvidence get_all_evidence(body, site_id, caid=caid)

Retrieve report of all user logins

Retrieve the list of successful login events that used publicly available leaked credentials. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.EvidenceApi(swagger_client.ApiClient(configuration))
body = swagger_client.EvidenceRequest() # EvidenceRequest | Specify the time selection and/or endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve report of all user logins
    api_response = api_instance.get_all_evidence(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EvidenceApi->get_all_evidence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EvidenceRequest**](EvidenceRequest.md)| Specify the time selection and/or endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**SuspiciousSuccessfulEvidence**](SuspiciousSuccessfulEvidence.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_compromised_evidence**
> Evidence get_compromised_evidence(body, site_id, caid=caid)

Retrieve the compromised users login report

Retrieve the list of successful login events that had a non-zero probability of being an attack. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.EvidenceApi(swagger_client.ApiClient(configuration))
body = swagger_client.EvidenceRequest() # EvidenceRequest | Specify the time selection and/or endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the compromised users login report
    api_response = api_instance.get_compromised_evidence(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EvidenceApi->get_compromised_evidence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EvidenceRequest**](EvidenceRequest.md)| Specify the time selection and/or endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**Evidence**](Evidence.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_leaked_evidence**
> Evidence get_leaked_evidence(body, site_id, caid=caid)

Retrieve the leaked users login report

Retrieve the list of successful login events that used publicly available leaked credentials. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.EvidenceApi(swagger_client.ApiClient(configuration))
body = swagger_client.EvidenceRequest() # EvidenceRequest | Specify the time selection and/or endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the leaked users login report
    api_response = api_instance.get_leaked_evidence(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EvidenceApi->get_leaked_evidence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EvidenceRequest**](EvidenceRequest.md)| Specify the time selection and/or endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**Evidence**](Evidence.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_likely_leaked_evidence**
> LikelyLeakedEvidence get_likely_leaked_evidence(body, site_id, caid=caid)

Retrieve the likely leaked users login report

Retrieve the list of likely leaked login events that potentially used publicly available leaked credentials. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.EvidenceApi(swagger_client.ApiClient(configuration))
body = swagger_client.EvidenceRequest() # EvidenceRequest | Specify the time selection and/or endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the likely leaked users login report
    api_response = api_instance.get_likely_leaked_evidence(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EvidenceApi->get_likely_leaked_evidence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EvidenceRequest**](EvidenceRequest.md)| Specify the time selection and/or endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**LikelyLeakedEvidence**](LikelyLeakedEvidence.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mitigated_evidence**
> Evidence get_mitigated_evidence(body, site_id, caid=caid)

Retrieve the mitigated (CAPTCHA, BLOCK, TARPIT) users login report

Retrieve the list of mitigated (CAPTCHA, BLOCK, TARPIT) login events. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.EvidenceApi(swagger_client.ApiClient(configuration))
body = swagger_client.EvidenceRequest() # EvidenceRequest | Specify the time selection and/or endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the mitigated (CAPTCHA, BLOCK, TARPIT) users login report
    api_response = api_instance.get_mitigated_evidence(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EvidenceApi->get_mitigated_evidence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EvidenceRequest**](EvidenceRequest.md)| Specify the time selection and/or endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**Evidence**](Evidence.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

