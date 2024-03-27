# ApiViolationActions

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**missing_param_violation_action** | **str** | The action taken when a missing parameter Violation occurs. Assigning DEFAULT will inherit the action from parent object, DEFAULT is not applicable for site-level configuration APIs | [optional] 
**invalid_param_value_violation_action** | **str** | The action taken when an invalid parameter value Violation occurs. Assigning DEFAULT will inherit the action from parent object, DEFAULT is not applicable for site-level configuration APIs | [optional] 
**invalid_param_name_violation_action** | **str** | The action taken when an invalid parameter name Violation occurs. Assigning DEFAULT will inherit the action from parent object, DEFAULT is not applicable for site-level configuration APIs | [optional] 
**invalid_url_violation_action** | **str** | The action taken when an invalid URL Violation occurs. Assigning DEFAULT will inherit the action from parent object, DEFAULT is not applicable for site-level configuration APIs | [optional] 
**invalid_method_violation_action** | **str** | The action taken when an invalid method Violation occurs. Assigning DEFAULT will inherit the action from parent object, DEFAULT is not applicable for site-level configuration APIs | [optional] 
**other_traffic_violation_action** | **str** | The action taken when traffic that does not belong to the APIs defined in the OAS files or integrated from API Discovery is identified. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

