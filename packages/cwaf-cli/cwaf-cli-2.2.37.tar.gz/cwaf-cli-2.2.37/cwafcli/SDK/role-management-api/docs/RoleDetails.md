# RoleDetails

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role_id** | **int** | ID of the role that was acted on. | [optional] 
**role_name** | **str** | The name of the role that was acted on. | [optional] 
**role_description** | **str** | Description of the role. | [optional] 
**account_id** | **int** | ID of the account that was acted on. | [optional] 
**account_name** | **str** | The name of the account that was acted on. | [optional] 
**role_abilities** | [**list[Ability]**](Ability.md) | The abilities that the role contains. | [optional] 
**user_assignment** | [**list[UserAssignment]**](UserAssignment.md) | The emails and account ids of users assigned to the role. | [optional] 
**update_date** | **str** | The last update date of this role. | [optional] 
**is_editable** | **bool** | Whether or not the role can be modified. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

