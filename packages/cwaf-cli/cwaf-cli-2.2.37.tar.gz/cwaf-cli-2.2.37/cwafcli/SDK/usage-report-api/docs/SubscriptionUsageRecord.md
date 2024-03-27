# SubscriptionUsageRecord

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Subscription Usage Record ID. | [optional] 
**subscription_id** | **str** | Subscription ID. | [optional] 
**account_id** | **int** | Account ID. | [optional] 
**record_status** | **str** | Subscription Record Status. | [optional] 
**usage_cycle_day** | **int** | The start of the period used for calculating usage. For example, the value 10 indicates that the usage period starts on the 10th of the month and ends on the 9th of the following month. | [optional] 
**cycle_start_date** | **date** | The start of the usage cycle. | [optional] 
**cycle_end_date** | **date** | The end of the usage cycle. | [optional] 
**resource_usage_records** | [**list[ResourceUsageRecord]**](ResourceUsageRecord.md) | a list of the Subscription&#x27;s resources&#x27; usage records. | [optional] 
**base_plan_sku_display_names** | **list[str]** | The name of the subscription plan as displayed in the management console. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

