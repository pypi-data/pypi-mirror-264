# swagger_client.DDoSForNetworksTestAlertsApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_infra_protect_ddos_start**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_ddos_start) | **POST** /api/v1/infra-protect/test-alerts/ddos/start | DDoS start
[**post_infra_protect_ddos_stop**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_ddos_stop) | **POST** /api/v1/infra-protect/test-alerts/ddos/stop | DDoS stop
[**post_infra_protect_monitoring_attack_start_critical_alert**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_monitoring_attack_start_critical_alert) | **POST** /api/v1/infra-protect/test-alerts/monitoring/attack-start | Monitoring attack start
[**post_infra_protect_net_flow_bad_data**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_net_flow_bad_data) | **POST** /api/v1/infra-protect/test-alerts/monitoring/bad-data | Monitoring bad data
[**post_infra_protect_net_flow_start**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_net_flow_start) | **POST** /api/v1/infra-protect/test-alerts/monitoring/start | Monitoring start
[**post_infra_protect_net_flow_stop**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_net_flow_stop) | **POST** /api/v1/infra-protect/test-alerts/monitoring/stop | Monitoring stop
[**post_infra_protect_tunnel_down**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_tunnel_down) | **POST** /api/v1/infra-protect/test-alerts/connection/down | Connection down
[**post_infra_protect_tunnel_up**](DDoSForNetworksTestAlertsApi.md#post_infra_protect_tunnel_up) | **POST** /api/v1/infra-protect/test-alerts/connection/up | Connection up
[**post_protected_ip_status_down**](DDoSForNetworksTestAlertsApi.md#post_protected_ip_status_down) | **POST** /api/v1/infra-protect/test-alerts/ip-protection-status/down | IP protection status down
[**post_protected_ip_status_up**](DDoSForNetworksTestAlertsApi.md#post_protected_ip_status_up) | **POST** /api/v1/infra-protect/test-alerts/ip-protection-status/up | IP protection status up

# **post_infra_protect_ddos_start**
> InlineResponse20036 post_infra_protect_ddos_start(ip_prefix=ip_prefix, bps=bps, pps=pps)

DDoS start

Use this operation to send a test notification informing you that an Infrastructure Protection DDoS attack has started.<br/>You can optionally provide additional parameters to determine the magnitude of the attack.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
ip_prefix = 'ip_prefix_example' # str | The IP prefix to send a notification for. For example, 10.10.10.10 (optional)
bps = 56 # int | Number of bits per second (optional)
pps = 789 # int | Number of packets per second (optional)

try:
    # DDoS start
    api_response = api_instance.post_infra_protect_ddos_start(ip_prefix=ip_prefix, bps=bps, pps=pps)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_ddos_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_prefix** | **str**| The IP prefix to send a notification for. For example, 10.10.10.10 | [optional] 
 **bps** | **int**| Number of bits per second | [optional] 
 **pps** | **int**| Number of packets per second | [optional] 

### Return type

[**InlineResponse20036**](InlineResponse20036.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_ddos_stop**
> InlineResponse20036 post_infra_protect_ddos_stop(ip_prefix=ip_prefix, bps=bps, pps=pps)

DDoS stop

Use this operation to send a test notification informing you that an Infrastructure Protection DDoS attack has ended.<br/>You can optionally provide additional parameters to determine the magnitude of the attack.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
ip_prefix = 'ip_prefix_example' # str | The IP prefix to send a notification for. For example, 10.10.10.10 (optional)
bps = 56 # int | Number of bits per second (optional)
pps = 789 # int | Number of packets per second (optional)

try:
    # DDoS stop
    api_response = api_instance.post_infra_protect_ddos_stop(ip_prefix=ip_prefix, bps=bps, pps=pps)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_ddos_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_prefix** | **str**| The IP prefix to send a notification for. For example, 10.10.10.10 | [optional] 
 **bps** | **int**| Number of bits per second | [optional] 
 **pps** | **int**| Number of packets per second | [optional] 

### Return type

[**InlineResponse20036**](InlineResponse20036.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_monitoring_attack_start_critical_alert**
> InlineResponse20036 post_infra_protect_monitoring_attack_start_critical_alert(ip_prefix=ip_prefix, bps=bps, pps=pps, packet_type=packet_type)

Monitoring attack start

Use this operation to send a test notification informing you that the monitoring service has detected a DDoS attack.<br/>You can optionally provide additional parameters to determine the magnitude of the attack.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
ip_prefix = 'ip_prefix_example' # str | The IP range to send a notification for. For example, 1.1.1.0/24 (optional)
bps = 56 # int | Number of bits per second (optional)
pps = 789 # int | Number of packets per second (optional)
packet_type = 'packet_type_example' # str | Packet type. (UDP, TCP, DNS, DNS_RESPONSE, ICMP, SYN, FRAG, LARGE_SYN, NTP, NETFLOW, SSDP, GENERAL) (optional)

try:
    # Monitoring attack start
    api_response = api_instance.post_infra_protect_monitoring_attack_start_critical_alert(ip_prefix=ip_prefix, bps=bps, pps=pps, packet_type=packet_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_monitoring_attack_start_critical_alert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_prefix** | **str**| The IP range to send a notification for. For example, 1.1.1.0/24 | [optional] 
 **bps** | **int**| Number of bits per second | [optional] 
 **pps** | **int**| Number of packets per second | [optional] 
 **packet_type** | **str**| Packet type. (UDP, TCP, DNS, DNS_RESPONSE, ICMP, SYN, FRAG, LARGE_SYN, NTP, NETFLOW, SSDP, GENERAL) | [optional] 

### Return type

[**InlineResponse20036**](InlineResponse20036.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_net_flow_bad_data**
> InlineResponse20037 post_infra_protect_net_flow_bad_data(exporter_ip=exporter_ip)

Monitoring bad data

Use this operation to send a test notification informing you that the monitoring service is receiving messages that do not conform to the accepted format.<br/>You can optionally provide the exporter IP found in the Management Console’s Monitoring Settings page.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
exporter_ip = 'exporter_ip_example' # str | The exporter IP to send a notification for. For example, 10.10.10.10.<br/>The exporter IP can be found in the Cloud Security Console’s Monitoring Settings page. (optional)

try:
    # Monitoring bad data
    api_response = api_instance.post_infra_protect_net_flow_bad_data(exporter_ip=exporter_ip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_net_flow_bad_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exporter_ip** | **str**| The exporter IP to send a notification for. For example, 10.10.10.10.&lt;br/&gt;The exporter IP can be found in the Cloud Security Console’s Monitoring Settings page. | [optional] 

### Return type

[**InlineResponse20037**](InlineResponse20037.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_net_flow_start**
> InlineResponse20037 post_infra_protect_net_flow_start(exporter_ip=exporter_ip)

Monitoring start

Use this operation to send a test notification informing you that flow monitoring has started.<br/>You can optionally provide the exporter IP found in the Management Console’s Monitoring Settings page.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
exporter_ip = 'exporter_ip_example' # str | The exporter IP to send a notification for. For example, 10.10.10.10.<br/>The exporter IP can be found in the Cloud Security Console’s Monitoring Settings page. (optional)

try:
    # Monitoring start
    api_response = api_instance.post_infra_protect_net_flow_start(exporter_ip=exporter_ip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_net_flow_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exporter_ip** | **str**| The exporter IP to send a notification for. For example, 10.10.10.10.&lt;br/&gt;The exporter IP can be found in the Cloud Security Console’s Monitoring Settings page. | [optional] 

### Return type

[**InlineResponse20037**](InlineResponse20037.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_net_flow_stop**
> InlineResponse20037 post_infra_protect_net_flow_stop(exporter_ip=exporter_ip)

Monitoring stop

Use this operation to send a test notification informing you that NetFlow monitoring has stopped.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
exporter_ip = 'exporter_ip_example' # str | The exporter IP to send a notification for. For example, 10.10.10.10.<br/>The exporter IP can be found in the Cloud Security Console’s Monitoring Settings page. (optional)

try:
    # Monitoring stop
    api_response = api_instance.post_infra_protect_net_flow_stop(exporter_ip=exporter_ip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_net_flow_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exporter_ip** | **str**| The exporter IP to send a notification for. For example, 10.10.10.10.&lt;br/&gt;The exporter IP can be found in the Cloud Security Console’s Monitoring Settings page. | [optional] 

### Return type

[**InlineResponse20037**](InlineResponse20037.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_tunnel_down**
> InlineResponse20038 post_infra_protect_tunnel_down(connection_name=connection_name)

Connection down

Use this operation to send a test notification informing you that the Infrastructure Protection connection is down.<br/>You can optionally provide the name of the connection as it appears in the Management Console’s Protection Settings page.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
connection_name = 'connection_name_example' # str | The connection to send a notification for.<br/>Enter the connection name as it appears in the Cloud Security Console’s Protection Settings page. For example, Test_GRE_Tunnel. (optional)

try:
    # Connection down
    api_response = api_instance.post_infra_protect_tunnel_down(connection_name=connection_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_tunnel_down: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_name** | **str**| The connection to send a notification for.&lt;br/&gt;Enter the connection name as it appears in the Cloud Security Console’s Protection Settings page. For example, Test_GRE_Tunnel. | [optional] 

### Return type

[**InlineResponse20038**](InlineResponse20038.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_infra_protect_tunnel_up**
> InlineResponse20038 post_infra_protect_tunnel_up(connection_name=connection_name)

Connection up

Use this operation to send a test notification informing you that the Infrastructure Protection connection is up.<br/>You can optionally provide the name of the connection as it appears in the Management Console’s Protection Settings page.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
connection_name = 'connection_name_example' # str | The connection to send a notification for.<br/>Enter the connection name as it appears in the Cloud Security Console’s Protection Settings page. For example, Test_GRE_Tunnel. (optional)

try:
    # Connection up
    api_response = api_instance.post_infra_protect_tunnel_up(connection_name=connection_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_infra_protect_tunnel_up: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_name** | **str**| The connection to send a notification for.&lt;br/&gt;Enter the connection name as it appears in the Cloud Security Console’s Protection Settings page. For example, Test_GRE_Tunnel. | [optional] 

### Return type

[**InlineResponse20038**](InlineResponse20038.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_protected_ip_status_down**
> InlineResponse20039 post_protected_ip_status_down(ip_protection=ip_protection)

IP protection status down

Use this operation to send a test notification informing you that the IP Protection status is down.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
ip_protection = 'ip_protection_example' # str | The IP to send a notification for. For example, 10.10.10.10 (optional)

try:
    # IP protection status down
    api_response = api_instance.post_protected_ip_status_down(ip_protection=ip_protection)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_protected_ip_status_down: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_protection** | **str**| The IP to send a notification for. For example, 10.10.10.10 | [optional] 

### Return type

[**InlineResponse20039**](InlineResponse20039.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_protected_ip_status_up**
> InlineResponse20036 post_protected_ip_status_up(ip_protection=ip_protection)

IP protection status up

Use this operation to send a test notification informing you that the IP Protection status is up.

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
api_instance = swagger_client.DDoSForNetworksTestAlertsApi(swagger_client.ApiClient(configuration))
ip_protection = 'ip_protection_example' # str | The IP to send a notification for. For example, 10.10.10.10 (optional)

try:
    # IP protection status up
    api_response = api_instance.post_protected_ip_status_up(ip_protection=ip_protection)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DDoSForNetworksTestAlertsApi->post_protected_ip_status_up: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ip_protection** | **str**| The IP to send a notification for. For example, 10.10.10.10 | [optional] 

### Return type

[**InlineResponse20036**](InlineResponse20036.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

