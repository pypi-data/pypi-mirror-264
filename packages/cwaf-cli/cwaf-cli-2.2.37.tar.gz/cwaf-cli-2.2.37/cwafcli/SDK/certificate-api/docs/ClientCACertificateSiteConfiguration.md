# ClientCACertificateSiteConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mandatory** | **bool** | When set to true, the end user is required to present the client certificate in order to access the site.By default, set to false. | [optional] 
**ports** | **list[int]** | The ports on which client certificate authentication is supported. If left empty, client certificates are supported on all ports. | [optional] 
**is_ports_exception** | **bool** | When set to true, client certificates are not supported on the ports listed in the Ports field (&#x27;blacklisted&#x27;). By default, set to false. | [optional] 
**hosts** | **list[str]** | The hosts on which client certificate authentication is supported. If left empty, client certificates are supported on all hosts. | [optional] 
**is_hosts_exception** | **bool** | When set to true, client certificates are not supported on the hosts listed in the Hosts field (&#x27;blacklisted&#x27;).By default, set to false. | [optional] 
**fingerprints** | **list[str]** | Permitted client certificate fingerprints. If left empty, all fingerprints are permitted. | [optional] 
**forward_to_origin** | **bool** | When set to true, the contents specified in headerValue are sent to the origin server in the header specified by headerName. By default, set to false. | [optional] 
**header_name** | **str** | The name of the header to send header content in. By default, the header name is &#x27;clientCertificateInfo&#x27;. | [optional] 
**header_value** | **str** | The content to send in the header specified by headerName. One of the following:   FULL_CERT (for full certificate in Base64)  COMMON_NAME (for certificate&#x27;s common name (CN)) FINGERPRINT (for the certificate fingerprints in SHA1) SERIAL_NUMBER (for the certificate&#x27;s serial number) | [optional] 
**is_disable_session_resumption** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

