# NotificationPolicyFull

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**policy_id** | **int** | The policy ID. Send a null value when creating a new policy. When updating a policy, send the ID of the relevant policy. | [optional] 
**account_id** | **int** | The Imperva ID of the account or subaccount. The accountId must be either null, equal to the account id associated with the API key, or equal to the caid. | [optional] 
**policy_name** | **str** | The name of the policy | 
**status** | **str** | Indicates whether policy is enabled or disabled. | 
**sub_category** | **str** | The subtype of the notification policy. | 
**notification_channel_list** | **list[OneOfNotificationPolicyFullNotificationChannelListItems]** | List of notification channels | 
**asset_list** | [**list[Asset]**](Asset.md) | List of assets to receive notifications (if assets are relevant to the sub category type) | [optional] 
**apply_to_new_assets** | **str** | If value is ‘TRUE’, all newly onboarded assets are automatically added to the notification policy&#x27;s assets list. | 
**policy_type** | **str** | If value is ‘ACCOUNT’, the policy will apply only to the current account. If the value is &#x27;SUB_ACCOUNT&#x27; the policy applies to the sub accounts only. The parent account will receive notifications for activity in the sub accounts that are specified in the subAccountList parameter. This parameter is available only in accounts that can contain sub accounts. | [optional] 
**sub_account_policy_info** | [**SubAccountPolicyInfo**](SubAccountPolicyInfo.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

