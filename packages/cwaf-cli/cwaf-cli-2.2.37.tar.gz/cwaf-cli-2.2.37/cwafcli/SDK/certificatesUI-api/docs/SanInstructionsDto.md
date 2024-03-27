# SanInstructionsDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**domain** | **str** | Domain to validate | [optional] 
**expiration_date** | **int** | SAN expiration date | [optional] 
**validation_email** | **str** | Validation email | [optional] 
**validation_method** | **str** | Validation method of the SAN | [optional] 
**record_type** | **str** | Record type for the validation | [optional] 
**verification_code** | **str** | Verification code of the SAN | [optional] 
**verification_code_expiration_date** | **int** | Verification code expiration date | [optional] 
**last_notification_date** | **int** | Last date an email was sent | [optional] 
**related_sans_details** | [**list[RelatedSansDetails]**](RelatedSansDetails.md) | List of related SANs using the same domain for validation | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

