# DataCenterServerConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | **str** | Server address as: host name, ipv4, or ipv6 | 
**id** | **int** | Server id | [optional] 
**is_enabled** | **bool** | For each data center, at least one server must be enabled | [optional] [default to True]
**server_mode** | **str** | Single IP allows single active server plus optionally single standny server. Each server may have multiple webservers (listening to different port). Multiple IPs allow multiple servers having single webserver and listening port per server. | [optional] [default to 'ACTIVE']
**weight** | **int** | Weight in percentage. Mandatory when Data center&#x27;s lbAlgorithm &#x3D; WEIGHTED | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

