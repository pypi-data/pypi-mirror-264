# AllowlistIp

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ip** | **str** | IP address to exclude. This will be either an IPv4 (e.g. 50.3.183.2) or normalized IPv6 representation (e.g. 2001:db8:0:0:1:0:0:1). | 
**mask** | **str** | [Optional] IP subnet mask to use for excluding a range of IPs. This is the number of bits to use from the IP address as a subnet mask to apply on the source IP of incoming traffic. | [optional] 
**updated** | **int** | Timestamp, in UNIX Epoch milliseconds, of the latest update of this entry. | [optional] 
**desc** | **str** | Description of the IP/subnet. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

