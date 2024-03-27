# EvidenceRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pii_password** | **str** | Specify the PII password used to encrypt login information. If not specified, the user names will be hashed or encrypted. | [optional] 
**endpoint_id** | **int** | Optional: Specify the endpoint ID you would like to fetch information for. If not specified, all endpoints would be used. If no endpoint ID is supplied, the default will be all endpoints. | [optional] 
**start_time** | **int** | Specify the timestamp, in UNIX Epoch milliseconds, from which events are retrieved. | [optional] 
**end_time** | **int** | Specify the timestamp, in UNIX Epoch milliseconds, to which events are retrieved. | [optional] 
**range_hours** | **int** | Specify the range, in hours, for which events are retrieved. If specified, range will be used. If not specified, startTime and endTime will be used instead. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

