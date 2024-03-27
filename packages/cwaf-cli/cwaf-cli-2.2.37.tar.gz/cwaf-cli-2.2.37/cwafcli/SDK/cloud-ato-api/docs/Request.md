# Request

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | **str** | The username of the user sending the login request. If the PII password was specified, the username is returned. If the PII password was not specified or does not match our record, a hashed/encrypted form of the username is returned. | [optional] 
**client** | **str** | The client application used to send the request. | [optional] 
**declared_client** | **str** | The client application used to send the request, according to the declaration in the UserAgent HTTP header. | [optional] 
**clients** | **list[str]** | All client applications used to send requests during the specified timeframe. | [optional] 
**declared_clients** | **list[str]** | All client applications used to send requests during the specified timeframe, according to the declaration in the UserAgent HTTP header. | [optional] 
**request_id** | **int** | A unique identifier assigned to the request. | [optional] 
**session_id** | **int** | A unique identifier assigned to the session. | [optional] 
**ip** | **str** | IP address from which the login attempt was made. This will be either an IPv4 (e.g. 50.3.183.2) or normalized IPv6 representation (e.g. 2001:db8:0:0:1:0:0:1). | [optional] 
**timestamp** | **int** | Timestamp, in UNIX Epoch milliseconds, of the login event. | [optional] 
**path** | **str** | The login request endpoint path. | [optional] 
**country** | **str** | Country code where the login attempt was made. | [optional] 
**referrer** | **str** | The URL of the referring page. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

