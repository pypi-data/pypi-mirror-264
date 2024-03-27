# PolicyDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The Policy name | 
**description** | **str** | The Policy description | [optional] 
**enabled** | **bool** | Enable or disable the policy. A WAF Rules policy is always created in the enabled state, and cannot be disabled. | 
**account_id** | **int** | The Account Id Of the Policy | [optional] 
**policy_type** | **str** | The Policy type | 
**default_policy_config** | [**list[DefaultPolicyConfigDto]**](DefaultPolicyConfigDto.md) | Sets the specified policy as default for the account, or indicates that the policy is set as default. A default policy is used by any new website added to the account. | [optional] 
**policy_settings** | [**list[PolicySettingsDto]**](PolicySettingsDto.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

