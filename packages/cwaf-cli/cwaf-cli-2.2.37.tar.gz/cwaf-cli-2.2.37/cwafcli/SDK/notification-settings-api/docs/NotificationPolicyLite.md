# NotificationPolicyLite

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**policy_id** | **int** | The Imperva ID of the policy. | [optional] 
**account_id** | **int** | The Imperva ID of the account. | [optional] 
**name** | **str** | The name of the policy | [optional] 
**status** | **str** | Indicates whether policy is enabled or disabled. | [optional] 
**sub_category** | **str** | The notification policy subtype, such as ACCOUNT_NOTIFICATIONS. | [optional] 
**sub_category_display_name** | **str** | Displayed name of the notification policy subtype. | [optional] 
**channel_type_list** | [**list[ChannelType]**](ChannelType.md) | List of the channel types of the policy. | [optional] 
**assets_in_used_count** | **int** | The number of assets in the account to which the policy is applied. | [optional] 
**assets_total_count** | **int** | The total number of assets available in the account. | [optional] 
**category** | **str** | The notification policy type, such as ACCOUNT_AND_SITE. | [optional] 
**category_display_name** | **str** | Displayed name of the notification policy category. | [optional] 
**sub_accounts_applied_count** | **int** | The number of sub accounts that the parent account will receive notifications for, as specified by the subAccountList parameter. | [optional] 
**sub_accounts_total_count** | **int** | The number of sub accounts in the account. | [optional] 
**policy_type** | **str** | If value is ‘ACCOUNT’, the policy will apply only to the current account. If the value is &#x27;SUB_ACCOUNT&#x27; the policy applies to the sub accounts only. The parent account will receive notifications for activity in the sub accounts that are specified in the subAccountList parameter. The &#x27;SUB_ACCOUNT&#x27; value is available only in accounts that can contain sub accounts. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

