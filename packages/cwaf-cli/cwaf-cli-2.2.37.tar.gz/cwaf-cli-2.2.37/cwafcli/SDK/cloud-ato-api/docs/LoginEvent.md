# LoginEvent

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ip** | **str** | IP address from which the login attempt was made. This will be either an IPv4 (e.g. 50.3.183.2) or normalized IPv6 representation (e.g. 2001:db8:0:0:1:0:0:1). | [optional] 
**risk** | **str** | Probability that this event was part of an attack, as computed post-factum. | [optional] 
**time** | **int** | Timestamp, in UNIX Epoch milliseconds, of the login event. | [optional] 
**user** | **str** | The username, if the PII password was specified, or a hashed/encrypted form of the username if the PII password was not specified or does not match. | [optional] 
**type** | **str** | Reason for the presence of the login event in the report. | [optional] 
**path** | **str** | The login request endpoint path. | [optional] 
**referrer** | **str** | The URL of the referring page. | [optional] 
**endpoint_id** | **str** | The endpoint ID associated with the login request. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

