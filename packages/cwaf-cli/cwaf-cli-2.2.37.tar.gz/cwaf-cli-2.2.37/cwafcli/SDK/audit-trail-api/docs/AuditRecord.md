# AuditRecord

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time** | **int** | Time of the audit event | [optional] 
**type_key** | **str** | The name of the action that was performed in the account, such as ACCOUNT_LOGIN or SITE_ORIGIN_SERVERS_SETTINGS_CHANGED. | [optional] 
**type_description** | **str** | A description of the action that was performed in the account, such as logging in or changing site settings. | [optional] 
**user_id** | **str** | ID of the user who performed the action | [optional] 
**user_details** | **str** | Email of the user who performed the action | [optional] 
**account_id** | **str** | ID of the account that the action was done in | [optional] 
**resource_type_key** | **str** | The type of the resource that the action was done on | [optional] 
**resource_id** | **str** | ID of the resource that the action was done on | [optional] 
**message** | **str** | Detailed description of the audit event | [optional] 
**context_key** | **str** | The audit activity context. Can be one of the following: UI, API, INTERNAL_API, JOB, NA | [optional] 
**assumed_by_user** | **str** | The user who performed the action on behalf of an account user | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

