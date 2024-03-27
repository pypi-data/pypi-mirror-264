# ReportRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **int** | Specify the timestamp, in UNIX Epoch milliseconds, from which events are retrieved. | [optional] 
**limit** | **int** | Specify the maximum number of events in the report (maximum 10000, default 10000). | [optional] 
**pii_password** | **str** | Specify the PII password used to encrypt login information. If not specified, the user names will be hashed or encrypted in the response. | [optional] 
**endpoint_id** | **str** | Optional: Specify the endpoint ID to fetch information for. If no endpoint ID is specified, details of all endpoints defined for the website are returned. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

