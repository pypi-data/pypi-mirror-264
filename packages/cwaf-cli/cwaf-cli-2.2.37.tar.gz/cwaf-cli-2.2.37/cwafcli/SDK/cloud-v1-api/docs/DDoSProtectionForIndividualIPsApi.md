# swagger_client.DDoSProtectionForIndividualIPsApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_sip_by_cname**](DDoSProtectionForIndividualIPsApi.md#add_sip_by_cname) | **POST** /api/prov/v1/ddos-protection/edge-ip/add/cname | Protected IP over TCP - add by origin IP
[**add_sip_by_dns_and_cname**](DDoSProtectionForIndividualIPsApi.md#add_sip_by_dns_and_cname) | **POST** /api/prov/v1/ddos-protection/edge-ip/add/dns-with-cname | Protected IP over TCP - add by DNS and CNAME
[**add_sip_by_dns_and_ip**](DDoSProtectionForIndividualIPsApi.md#add_sip_by_dns_and_ip) | **POST** /api/prov/v1/ddos-protection/edge-ip/add/dns-with-ip | Protected IP over TCP - add by DNS and origin IP
[**add_sip_by_ip**](DDoSProtectionForIndividualIPsApi.md#add_sip_by_ip) | **POST** /api/prov/v1/ddos-protection/edge-ip/add/ip | Protected IP over TCP - add by CNAME
[**edit_sip_by_cname**](DDoSProtectionForIndividualIPsApi.md#edit_sip_by_cname) | **POST** /api/prov/v1/ddos-protection/edge-ip/edit/cname | Protected IP over TCP - edit by CNAME
[**edit_sip_by_dns_and_cname**](DDoSProtectionForIndividualIPsApi.md#edit_sip_by_dns_and_cname) | **POST** /api/prov/v1/ddos-protection/edge-ip/edit/dns-with-cname | Protected IP over TCP - edit by DNS and origin IP
[**edit_sip_by_dns_and_ip**](DDoSProtectionForIndividualIPsApi.md#edit_sip_by_dns_and_ip) | **POST** /api/prov/v1/ddos-protection/edge-ip/edit/dns-with-ip | Protected IP over TCP - edit by DNS and origin IP
[**edit_sip_by_ip**](DDoSProtectionForIndividualIPsApi.md#edit_sip_by_ip) | **POST** /api/prov/v1/ddos-protection/edge-ip/edit/ip | Protected IP over TCP - edit by origin IP
[**edit_sip_ha_protocol**](DDoSProtectionForIndividualIPsApi.md#edit_sip_ha_protocol) | **POST** /api/prov/v1/ddos-protection/edge-ip/edit/ha-protocol | Protected IP over TCP - edit HA protocol setting
[**edit_sip_monitoring_settings**](DDoSProtectionForIndividualIPsApi.md#edit_sip_monitoring_settings) | **POST** /api/prov/v1/ddos-protection/edge-ip/edit/monitoring-settings | Protected IP over TCP - edit monitoring settings
[**remove_sip**](DDoSProtectionForIndividualIPsApi.md#remove_sip) | **POST** /api/prov/v1/ddos-protection/edge-ip/remove | Protected IP over TCP - remove

# **add_sip_by_cname**
> InlineResponse20040 add_sip_by_cname(cname, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)

Protected IP over TCP - add by origin IP

Use this operation to onboard a CNAME record to the 'IP Protection over TCP' service. If successful, the operation will return the generated Edge IP.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
cname = 'cname_example' # str | CNAME record to onboard to service
enable_ha_protocol = true # bool | Provide 'true' to enable the Proxy Protocol setting (disabled by default) (optional)
description = 'description_example' # str | Optional description for the generated Edge IP (optional)
monitoring_type = 'monitoring_type_example' # str | Monitoring type for the Edge IP. Possible values: 'ICMP' (default), 'TCP' or 'NONE' (optional)
tcp_monitoring_port = 56 # int | Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. (optional)

try:
    # Protected IP over TCP - add by origin IP
    api_response = api_instance.add_sip_by_cname(cname, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->add_sip_by_cname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cname** | **str**| CNAME record to onboard to service | 
 **enable_ha_protocol** | **bool**| Provide &#x27;true&#x27; to enable the Proxy Protocol setting (disabled by default) | [optional] 
 **description** | **str**| Optional description for the generated Edge IP | [optional] 
 **monitoring_type** | **str**| Monitoring type for the Edge IP. Possible values: &#x27;ICMP&#x27; (default), &#x27;TCP&#x27; or &#x27;NONE&#x27; | [optional] 
 **tcp_monitoring_port** | **int**| Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. | [optional] 

### Return type

[**InlineResponse20040**](InlineResponse20040.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sip_by_dns_and_cname**
> InlineResponse20041 add_sip_by_dns_and_cname(dns_name, cname, disable_dns_check=disable_dns_check, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)

Protected IP over TCP - add by DNS and CNAME

Use this operation to onboard a CNAME record with an associated DNS name to the 'IP Protection over TCP' service. If DNS check is enabled, the response will include the list of resolved CNAME records for the provided domain name, and the operation will only succeed if the provided CNAME will be included in that list. If successful, the operation will return the generated Edge IP.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
dns_name = 'dns_name_example' # str | Domain name to onboard to service
cname = 'cname_example' # str | CNAME record to onboard to service
disable_dns_check = true # bool | Provide 'true' to disable DNS resolution check (enabled by default) (optional)
enable_ha_protocol = true # bool | Provide 'true' to enable the Proxy Protocol setting (disabled by default) (optional)
description = 'description_example' # str | description for the generated Edge IP (optional)
monitoring_type = 'monitoring_type_example' # str | Monitoring type for the Edge IP. Possible values: 'ICMP' (default), 'TCP' or 'NONE (optional)
tcp_monitoring_port = 56 # int | Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. (optional)

try:
    # Protected IP over TCP - add by DNS and CNAME
    api_response = api_instance.add_sip_by_dns_and_cname(dns_name, cname, disable_dns_check=disable_dns_check, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->add_sip_by_dns_and_cname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dns_name** | **str**| Domain name to onboard to service | 
 **cname** | **str**| CNAME record to onboard to service | 
 **disable_dns_check** | **bool**| Provide &#x27;true&#x27; to disable DNS resolution check (enabled by default) | [optional] 
 **enable_ha_protocol** | **bool**| Provide &#x27;true&#x27; to enable the Proxy Protocol setting (disabled by default) | [optional] 
 **description** | **str**| description for the generated Edge IP | [optional] 
 **monitoring_type** | **str**| Monitoring type for the Edge IP. Possible values: &#x27;ICMP&#x27; (default), &#x27;TCP&#x27; or &#x27;NONE | [optional] 
 **tcp_monitoring_port** | **int**| Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. | [optional] 

### Return type

[**InlineResponse20041**](InlineResponse20041.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sip_by_dns_and_ip**
> InlineResponse20042 add_sip_by_dns_and_ip(dns_name, origin_ip, disable_dns_check=disable_dns_check, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)

Protected IP over TCP - add by DNS and origin IP

Use this operation to onboard a public origin IP with an associated DNS name to the 'IP Protection over TCP' service. If DNS check is enabled, the response will include the list of resolved IPs for the provided domain name, and the operation will only succeed if the provided origin IP will be included in that list. If successful, the operation will return the generated Edge IP.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
dns_name = 'dns_name_example' # str | Domain name to onboard to service
origin_ip = 'origin_ip_example' # str | Public origin IP to onboard to service
disable_dns_check = true # bool | Provide 'true' to disable DNS resolution check (enabled by default) (optional)
enable_ha_protocol = true # bool | Provide 'true' to enable the Proxy Protocol setting (disabled by default) (optional)
description = 'description_example' # str | description for the generated Edge IP (optional)
monitoring_type = 'monitoring_type_example' # str | Monitoring type for the Edge IP. Possible values: 'ICMP' (default), 'TCP' or 'NONE (optional)
tcp_monitoring_port = 56 # int | Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. (optional)

try:
    # Protected IP over TCP - add by DNS and origin IP
    api_response = api_instance.add_sip_by_dns_and_ip(dns_name, origin_ip, disable_dns_check=disable_dns_check, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->add_sip_by_dns_and_ip: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dns_name** | **str**| Domain name to onboard to service | 
 **origin_ip** | **str**| Public origin IP to onboard to service | 
 **disable_dns_check** | **bool**| Provide &#x27;true&#x27; to disable DNS resolution check (enabled by default) | [optional] 
 **enable_ha_protocol** | **bool**| Provide &#x27;true&#x27; to enable the Proxy Protocol setting (disabled by default) | [optional] 
 **description** | **str**| description for the generated Edge IP | [optional] 
 **monitoring_type** | **str**| Monitoring type for the Edge IP. Possible values: &#x27;ICMP&#x27; (default), &#x27;TCP&#x27; or &#x27;NONE | [optional] 
 **tcp_monitoring_port** | **int**| Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. | [optional] 

### Return type

[**InlineResponse20042**](InlineResponse20042.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sip_by_ip**
> InlineResponse20043 add_sip_by_ip(origin_ip, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)

Protected IP over TCP - add by CNAME

Use this operation to onboard a public origin IP to the 'IP Protection over TCP' service. If successful, the operation will return the generated Edge IP.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
origin_ip = 'origin_ip_example' # str | Public origin IP to onboard to service
enable_ha_protocol = true # bool | Provide 'true' to enable the Proxy Protocol setting (disabled by default) (optional)
description = 'description_example' # str | description for the generated Edge IP (optional)
monitoring_type = 'monitoring_type_example' # str | Monitoring type for the Edge IP. Possible values: 'ICMP' (default), 'TCP' or 'NONE' (optional)
tcp_monitoring_port = 56 # int | Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. (optional)

try:
    # Protected IP over TCP - add by CNAME
    api_response = api_instance.add_sip_by_ip(origin_ip, enable_ha_protocol=enable_ha_protocol, description=description, monitoring_type=monitoring_type, tcp_monitoring_port=tcp_monitoring_port)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->add_sip_by_ip: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **origin_ip** | **str**| Public origin IP to onboard to service | 
 **enable_ha_protocol** | **bool**| Provide &#x27;true&#x27; to enable the Proxy Protocol setting (disabled by default) | [optional] 
 **description** | **str**| description for the generated Edge IP | [optional] 
 **monitoring_type** | **str**| Monitoring type for the Edge IP. Possible values: &#x27;ICMP&#x27; (default), &#x27;TCP&#x27; or &#x27;NONE&#x27; | [optional] 
 **tcp_monitoring_port** | **int**| Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. | [optional] 

### Return type

[**InlineResponse20043**](InlineResponse20043.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_sip_by_cname**
> InlineResponse20040 edit_sip_by_cname(edge_ip, cname)

Protected IP over TCP - edit by CNAME

Use this operation to assign a new CNAME record to the provided Edge IP under the 'IP Protection over TCP' service. This operation is also able to change the type of the entity protected by the provided Edge IP (Any existing combination of Origin IP/CNAME and DNS will be overwritten). If successful, the operation will return the Edge IP. WARNING: Any entity already protected by this Edge IP prior to the change will no longer be protected once modification is successful, unless duplicate protection is used.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP
cname = 'cname_example' # str | CNAME to onboard to service

try:
    # Protected IP over TCP - edit by CNAME
    api_response = api_instance.edit_sip_by_cname(edge_ip, cname)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->edit_sip_by_cname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 
 **cname** | **str**| CNAME to onboard to service | 

### Return type

[**InlineResponse20040**](InlineResponse20040.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_sip_by_dns_and_cname**
> InlineResponse20041 edit_sip_by_dns_and_cname(edge_ip, dns_name, cname, disable_dns_check=disable_dns_check)

Protected IP over TCP - edit by DNS and origin IP

Use this operation to assign a new CNAME record with an associated DNS name to the provided Edge IP under the 'IP Protection over TCP' service.<br/>This operation is also able to change the type of the entity protected by the provided Edge IP (Any existing combination of Origin IP/CNAME and DNS name will be overwritten).<br/>If DNS check is enabled, the response will include the list of resolved CNAME records for the provided domain name, and the operation will only succeed if the provided CNAME is included in that list.<br/>If successful, the operation will return the Edge IP.<br/>WARNING: Any entity already protected by this Edge IP prior to the change will no longer be protected once modification is successful, unless duplicate protection is used.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP
dns_name = 'dns_name_example' # str | Domain name to onboard to service
cname = 'cname_example' # str | CNAME to onboard to service
disable_dns_check = true # bool | Provide 'true' to disable DNS resolution check (enabled by default) (optional)

try:
    # Protected IP over TCP - edit by DNS and origin IP
    api_response = api_instance.edit_sip_by_dns_and_cname(edge_ip, dns_name, cname, disable_dns_check=disable_dns_check)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->edit_sip_by_dns_and_cname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 
 **dns_name** | **str**| Domain name to onboard to service | 
 **cname** | **str**| CNAME to onboard to service | 
 **disable_dns_check** | **bool**| Provide &#x27;true&#x27; to disable DNS resolution check (enabled by default) | [optional] 

### Return type

[**InlineResponse20041**](InlineResponse20041.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_sip_by_dns_and_ip**
> InlineResponse20042 edit_sip_by_dns_and_ip(edge_ip, dns_name, origin_ip, disable_dns_check=disable_dns_check)

Protected IP over TCP - edit by DNS and origin IP

Use this operation to assign a new origin IP with an associated DNS name to the provided Edge IP under the 'IP Protection over TCP' service. This operation is also able to change the type of the entity protected by the provided Edge IP (Any existing combination of Origin IP/CNAME and DNS name will be overwritten). If DNS check is enabled, the response will include the list of resolved IPs for the provided domain name, and the operation will only succeed if the provided origin IP is included in that list. If successful, the operation will return the Edge IP. WARNING: Any entity already protected by this Edge IP prior to the change will no longer be protected once modification is successful, unless duplicate protection is used.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP
dns_name = 'dns_name_example' # str | Domain name to onboard to service
origin_ip = 'origin_ip_example' # str | Public origin IP to onboard to service
disable_dns_check = true # bool | Provide 'true' to disable DNS resolution check (enabled by default) (optional)

try:
    # Protected IP over TCP - edit by DNS and origin IP
    api_response = api_instance.edit_sip_by_dns_and_ip(edge_ip, dns_name, origin_ip, disable_dns_check=disable_dns_check)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->edit_sip_by_dns_and_ip: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 
 **dns_name** | **str**| Domain name to onboard to service | 
 **origin_ip** | **str**| Public origin IP to onboard to service | 
 **disable_dns_check** | **bool**| Provide &#x27;true&#x27; to disable DNS resolution check (enabled by default) | [optional] 

### Return type

[**InlineResponse20042**](InlineResponse20042.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_sip_by_ip**
> InlineResponse20043 edit_sip_by_ip(edge_ip, origin_ip)

Protected IP over TCP - edit by origin IP

Use this operation to assign a new origin IP to the provided Edge IP under the 'IP Protection over TCP' service. This operation is also able to change the type of the entity protected by the provided Edge IP (Any existing combination of Origin IP/CNAME and DNS name will be overwritten). If successful, the operation will return the Edge IP. WARNING: Any entity already protected by this Edge IP prior to the change will no longer be protected once modification is successful, unless duplicate protection is used.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP
origin_ip = 'origin_ip_example' # str | Public origin IP to onboard to service

try:
    # Protected IP over TCP - edit by origin IP
    api_response = api_instance.edit_sip_by_ip(edge_ip, origin_ip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->edit_sip_by_ip: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 
 **origin_ip** | **str**| Public origin IP to onboard to service | 

### Return type

[**InlineResponse20043**](InlineResponse20043.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_sip_ha_protocol**
> ApiResult edit_sip_ha_protocol(edge_ip, enable_ha_protocol)

Protected IP over TCP - edit HA protocol setting

Use this operation on the provided Edge IP to toggle its HA Protocol setting on or off. By default, this setting is disabled during onboarding unless explicitly set to 'true'. WARNING: Do not modify this setting unless you are familiar with the proxy protocol and understand the implications of enabling or disabling it for your account.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP
enable_ha_protocol = true # bool | Provide 'true' to enable the Proxy Protocol setting, 'false' to disable

try:
    # Protected IP over TCP - edit HA protocol setting
    api_response = api_instance.edit_sip_ha_protocol(edge_ip, enable_ha_protocol)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->edit_sip_ha_protocol: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 
 **enable_ha_protocol** | **bool**| Provide &#x27;true&#x27; to enable the Proxy Protocol setting, &#x27;false&#x27; to disable | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_sip_monitoring_settings**
> ApiResult edit_sip_monitoring_settings(edge_ip, monitoring_type, tcp_monitoring_port=tcp_monitoring_port)

Protected IP over TCP - edit monitoring settings

Use this operation on the specified Edge IP to modify its monitoring settings.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP
monitoring_type = 'monitoring_type_example' # str | Monitoring type for the Edge IP. Possible values: 'ICMP' (default), 'TCP' or 'NONE'
tcp_monitoring_port = 56 # int | Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. (optional)

try:
    # Protected IP over TCP - edit monitoring settings
    api_response = api_instance.edit_sip_monitoring_settings(edge_ip, monitoring_type, tcp_monitoring_port=tcp_monitoring_port)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->edit_sip_monitoring_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 
 **monitoring_type** | **str**| Monitoring type for the Edge IP. Possible values: &#x27;ICMP&#x27; (default), &#x27;TCP&#x27; or &#x27;NONE&#x27; | 
 **tcp_monitoring_port** | **int**| Port to use for TCP monitoring of the Edge IP. Required only when TCP monitoring is used. | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_sip**
> ApiResult remove_sip(edge_ip)

Protected IP over TCP - remove

Use this operation on the provided Edge IP to remove it from the 'IP Protection over TCP' service.<br/>WARNING: Any entity already protected by this Edge IP will no longer be protected once the operation is successful, unless duplicate protection was enabled and used.

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
api_instance = swagger_client.DDoSProtectionForIndividualIPsApi(swagger_client.ApiClient(configuration))
edge_ip = 'edge_ip_example' # str | Imperva generated Edge IP

try:
    # Protected IP over TCP - remove
    api_response = api_instance.remove_sip(edge_ip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSProtectionForIndividualIPsApi->remove_sip: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **edge_ip** | **str**| Imperva generated Edge IP | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

