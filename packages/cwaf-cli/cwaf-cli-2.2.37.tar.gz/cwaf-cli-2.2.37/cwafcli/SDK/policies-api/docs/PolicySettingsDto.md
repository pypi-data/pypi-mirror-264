# PolicySettingsDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Policy Settings ID | [optional] 
**policy_id** | **int** | The Policy ID of this setting | [optional] 
**settings_action** | **str** | The action taken by Imperva when a policy rule is triggered | [optional] 
**policy_setting_type** | **str** | The PolicySettings type | [optional] 
**data** | [**SettingsDataDto**](SettingsDataDto.md) |  | [optional] 
**policy_data_exceptions** | [**list[PolicyDataExceptionDto]**](PolicyDataExceptionDto.md) | The exception configuration on a given settings | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

