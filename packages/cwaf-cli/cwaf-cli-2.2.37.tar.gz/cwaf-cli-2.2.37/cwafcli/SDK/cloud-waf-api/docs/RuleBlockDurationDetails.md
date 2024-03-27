# RuleBlockDurationDetails

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**block_duration_period_type** | **str** | Block duration types: Fixed, Randomized. Time range: 1-1440 minutes.The Fixed type blocks the IP address or session for the duration specified by the blockFixedDurationValue parameter. The Randomized type generates a random duration for each block between the specified minimum and maximum values. | [optional] 
**block_fixed_duration_value** | **int** | Value of the fixed block duration. Valid only for &#x27;fixed&#x27; blockDurationPeriodType | [optional] 
**block_randomized_duration_min_value** | **int** | The lower limit for the randomized block duration. Valid only for &#x27;randomized&#x27; blockDurationPeriodType | [optional] 
**block_randomized_duration_max_value** | **int** | The upper limit for the randomized block duration. Valid only for &#x27;randomized&#x27; blockDurationPeriodType | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

