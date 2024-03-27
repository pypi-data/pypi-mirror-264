# RiskData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**risk_score** | **str** | An assessment of the risk level posed by this IP, based on activity of this IP across the Imperva customer base over the past week (clean and malicious traffic).The calculation takes into account the number of attacks, the number of Imperva customer accounts that were attacked, and the severity of attacks by this IP. Possible values: CRITICAL, HIGH, MEDIUM, LOW. (CRITICAL: Risk score number of 75 or above. HIGH: Risk score number of 50-74. MEDIUM: Risk score number of 25-49. LOW: Risk score number below 25.) | [optional] 
**risk_description** | **str** | Additional details on the risk assessment. | [optional] 
**risk_score_number** | **str** | risk score number between 0 and 100 | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

