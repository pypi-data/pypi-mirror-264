# swagger_client.GeneralApi

All URIs are relative to *https://api.imperva.com/ato*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_to_allow_list**](GeneralApi.md#add_to_allow_list) | **POST** /v2/sites/{siteId}/allowlist | Update the allowlist for a specific site
[**get_allow_list**](GeneralApi.md#get_allow_list) | **GET** /v2/sites/{siteId}/allowlist | Retrieve the allowlist for a specific site
[**get_leaked_report**](GeneralApi.md#get_leaked_report) | **POST** /v2/sites/{siteId}/report/evidence/leaked | Retrieve the leaked users login report
[**get_mitigated_report**](GeneralApi.md#get_mitigated_report) | **POST** /v2/sites/{siteId}/report/evidence/mitigated | Retrieve the mitigated (CAPTCHA, BLOCK) users login report
[**get_successful_and_suspicious_report**](GeneralApi.md#get_successful_and_suspicious_report) | **POST** /v2/sites/{siteId}/report/evidence/suspicious/successful | Retrieve the compromised users login report
[**remove_from_allow_list**](GeneralApi.md#remove_from_allow_list) | **DELETE** /v2/sites/{siteId}/allowlist | Remove IPs from the allowlist for a specific site
[**reset_risk**](GeneralApi.md#reset_risk) | **POST** /v2/sites/{siteId}/reset-risk | Reset the risk level of IPs for a specific site
[**set_allow_list**](GeneralApi.md#set_allow_list) | **PUT** /v2/sites/{siteId}/allowlist | Overwrite the allowlist for a specific site

# **add_to_allow_list**
> add_to_allow_list(body, site_id)

Update the allowlist for a specific site

Update the list of IPs and subnets excluded from traffic mitigation by ATO Protection. All traffic from these IPs will not be mitigated. The input should be a comma separated JSON list containing the IPs to add to the site allowlist. Each allowed IP object can have a mask property to be applied to that IP and allow that whole subnet. For example: [{\"ip\":\"192.20.1.1\",\"desc\":\"My own IP\"},{\"ip\":\"15.5.0.0\",\"mask\":\"16\",\"desc\":\"Office subnet\"},{\"ip\":\"20.1.1.0\",\"mask\":\"24\",\"desc\":\"Home subnet\"}]

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = [swagger_client.AllowlistIp()] # list[AllowlistIp] | List of IPs/subnets
site_id = 789 # int | The Imperva ID of the website

try:
    # Update the allowlist for a specific site
    api_instance.add_to_allow_list(body, site_id)
except ApiException as e:
    print("Exception when calling GeneralApi->add_to_allow_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[AllowlistIp]**](AllowlistIp.md)| List of IPs/subnets | 
 **site_id** | **int**| The Imperva ID of the website | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_allow_list**
> AllowlistIp get_allow_list(site_id)

Retrieve the allowlist for a specific site

Retrieve the list of IPs and subnets excluded from traffic mitigation by ATO Protection. All traffic from these IPs will not be mitigated.

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | The Imperva ID of the website

try:
    # Retrieve the allowlist for a specific site
    api_response = api_instance.get_allow_list(site_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneralApi->get_allow_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| The Imperva ID of the website | 

### Return type

[**AllowlistIp**](AllowlistIp.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_leaked_report**
> LoginEvent get_leaked_report(body, site_id, caid=caid)

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = swagger_client.ReportRequest() # ReportRequest | Specify event selection range, PII password and endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the leaked users login report
    api_response = api_instance.get_leaked_report(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneralApi->get_leaked_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReportRequest**](ReportRequest.md)| Specify event selection range, PII password and endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**LoginEvent**](LoginEvent.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mitigated_report**
> LoginEvent get_mitigated_report(body, site_id, caid=caid)

Retrieve the mitigated (CAPTCHA, BLOCK) users login report

Retrieve the list of mitigated (CAPTCHA, BLOCK) login events. If the API key used is for a parent account, and the website belongs to a sub account, the caid of the sub account must be specified.

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = swagger_client.ReportRequest() # ReportRequest | Specify event selection range, PII password and endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the mitigated (CAPTCHA, BLOCK) users login report
    api_response = api_instance.get_mitigated_report(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneralApi->get_mitigated_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReportRequest**](ReportRequest.md)| Specify event selection range, PII password and endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**LoginEvent**](LoginEvent.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_successful_and_suspicious_report**
> LoginEvent get_successful_and_suspicious_report(body, site_id, caid=caid)

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = swagger_client.ReportRequest() # ReportRequest | Specify event selection range, PII password and endpoint ID
site_id = 789 # int | The Imperva ID of the website
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Retrieve the compromised users login report
    api_response = api_instance.get_successful_and_suspicious_report(body, site_id, caid=caid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneralApi->get_successful_and_suspicious_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReportRequest**](ReportRequest.md)| Specify event selection range, PII password and endpoint ID | 
 **site_id** | **int**| The Imperva ID of the website | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

[**LoginEvent**](LoginEvent.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_from_allow_list**
> remove_from_allow_list(body, site_id)

Remove IPs from the allowlist for a specific site

Remove the list of IPs and subnets from the current allowlist configuration of the site. Matching the IPs and subnets will be done by comparing the 'ip' and 'mask' fields of the entries. For example: [{\"ip\":\"192.20.1.1\"},{\"ip\":\"15.5.0.0\",\"mask\":\"16\"}]

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = [swagger_client.AllowlistIp()] # list[AllowlistIp] | List of IPs/subnets to remove
site_id = 789 # int | The Imperva ID of the website

try:
    # Remove IPs from the allowlist for a specific site
    api_instance.remove_from_allow_list(body, site_id)
except ApiException as e:
    print("Exception when calling GeneralApi->remove_from_allow_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[AllowlistIp]**](AllowlistIp.md)| List of IPs/subnets to remove | 
 **site_id** | **int**| The Imperva ID of the website | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_risk**
> reset_risk(body, site_id, caid=caid)

Reset the risk level of IPs for a specific site

Resets the risk level assigned to an IP address by Account Takeover Protection. Risk level indicates the severity of risk.  If there is continued suspicious activity from an IP, the risk level will escalate again afterwards.  For example: [\"192.20.1.1\",\"15.5.0.0\"]  For sites with ATO fingerprint enabled, not all devices will have their risk reset. Priority will be given to devices that were most recently active.  IPV4 and IPV6 values are accepted but IP ranges will be rejected  There is a limit of 10 IPs per request  

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = ['body_example'] # list[str] | List of IPs. The input must be a comma separated list of IP addresses in JSON format. It can take up to one minute to fully process the request after it has been sent.
site_id = 789 # int | 
caid = -1 # int | The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. (optional) (default to -1)

try:
    # Reset the risk level of IPs for a specific site
    api_instance.reset_risk(body, site_id, caid=caid)
except ApiException as e:
    print("Exception when calling GeneralApi->reset_risk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)| List of IPs. The input must be a comma separated list of IP addresses in JSON format. It can take up to one minute to fully process the request after it has been sent. | 
 **site_id** | **int**|  | 
 **caid** | **int**| The Imperva account ID. By default, the API operates on account (A) associated with the API credentials used for authentication. To operate on a different account (an account under the account (A)), specify the account ID. | [optional] [default to -1]

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_allow_list**
> set_allow_list(body, site_id)

Overwrite the allowlist for a specific site

Overwrite the list of IPs and subnets excluded from traffic mitigation by ATO Protection. THIS CALL WILL REPLACE THE EXISTING LIST. All traffic from these IPs will not be mitigated. The input should be a comma separated JSON list containing all the IPs in the allowlist for the site. Each allowed IP object can have a mask property to be applied to that IP and allow that whole subnet.

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
api_instance = swagger_client.GeneralApi(swagger_client.ApiClient(configuration))
body = [swagger_client.AllowlistIp()] # list[AllowlistIp] | Complete list of IPs/subnets
site_id = 789 # int | The Imperva ID of the website

try:
    # Overwrite the allowlist for a specific site
    api_instance.set_allow_list(body, site_id)
except ApiException as e:
    print("Exception when calling GeneralApi->set_allow_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[AllowlistIp]**](AllowlistIp.md)| Complete list of IPs/subnets | 
 **site_id** | **int**| The Imperva ID of the website | 

### Return type

void (empty response body)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

