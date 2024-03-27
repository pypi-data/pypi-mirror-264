# LikelyLeakedEvidence

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | **str** | The username of the user sending the login request. If the PII password was specified, the username is returned. If the PII password was not specified or does not match our record, a hashed/encrypted form of the username is returned. | [optional] 
**ip** | **str** | IP address from which the login attempt was made. This will be either an IPv4 (e.g. 50.3.183.2) or normalized IPv6 representation (e.g. 2001:db8:0:0:1:0:0:1). | [optional] 
**timestamp** | **int** | Timestamp, in UNIX Epoch milliseconds, of the login event. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

