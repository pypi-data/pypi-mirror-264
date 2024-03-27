# EndpointResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**specification_violation_action** | **str** | The action taken when an API Specification Violation occurs | [optional] 
**violation_actions** | [**EndpointViolationActions**](EndpointViolationActions.md) |  | [optional] 
**id** | **int** | The endpoint ID | [optional] 
**path** | **str** | The endpoint path | [optional] 
**method** | **str** | The endpoint HTTP method | [optional] 
**duplicate_of_endpoint_id** | **int** | The ID of the endpoint that this endpoint is the duplicate of | [optional] 
**sensitive_data_classification_list** | [**list[SensitiveDataClassification]**](SensitiveDataClassification.md) | Sensitive data classification list for this endpoint | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

