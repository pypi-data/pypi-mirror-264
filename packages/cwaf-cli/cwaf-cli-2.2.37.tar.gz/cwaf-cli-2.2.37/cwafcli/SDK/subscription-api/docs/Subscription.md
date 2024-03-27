# Subscription

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Subscription ID. | [optional] 
**base_plan_sku_display_names** | **list[str]** | The name of the subscription plan as displayed in the management console. | [optional] 
**subscription_status** | **str** | Indicates the status of the subscription. | [optional] 
**usage_cycle_day** | **int** | The start of the period used for calculating usage. For example, the value 10 indicates that the usage period starts on the 10th of the month and ends on the 9th of the following month. | [optional] 
**let_expire** | **date** | The date the subscription or trial period is set to end. | [optional] 
**creation_date** | **date** | Creation date of the subscription. | [optional] 
**payment_gateway** | **str** | Indicates a subscription paid for by credit card. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

