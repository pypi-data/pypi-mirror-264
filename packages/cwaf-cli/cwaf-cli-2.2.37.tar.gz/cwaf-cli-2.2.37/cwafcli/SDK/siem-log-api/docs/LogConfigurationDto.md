# LogConfigurationDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**configuration_name** | **str** | Log configuration name. | 
**provider** | **str** | The service providing the logs. The available providers are based on the account’s subscribed services. | 
**datasets** | **list[str]** | The log types. The available types are based on the provider. | 
**enabled** | **bool** | Enable / disable the log configuration | 
**connection_id** | **str** | The connection used for the log configuration. The connection defines the log storage repository that receives the logs. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

