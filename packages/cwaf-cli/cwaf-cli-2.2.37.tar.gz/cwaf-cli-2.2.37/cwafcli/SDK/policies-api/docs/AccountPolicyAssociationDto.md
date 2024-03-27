# AccountPolicyAssociationDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **int** | The Imperva ID of the current account. | [optional] 
**available_policy_ids** | **list[int]** | The account’s available policies. These policies can be applied to the websites in the account | [optional] 
**default_non_mandatory_non_distinct_policy_ids** | **list[int]** | The Imperva IDs of the account’s default, optional and simultaneously applied policies. An account can have multiple policies for each of these policy types. (e.g ACL, WHITELIST) | [optional] 
**default_waf_policy_id** | **int** | The Imperva ID of the account’s default WAF Rules policy. Each Imperva account and sub account includes a default WAF Rules policy. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

