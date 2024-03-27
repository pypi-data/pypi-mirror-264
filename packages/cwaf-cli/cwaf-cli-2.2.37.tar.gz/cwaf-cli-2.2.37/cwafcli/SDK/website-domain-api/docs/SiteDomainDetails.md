# SiteDomainDetails

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The ID of the alternative domain | [optional] 
**site_id** | **int** | The Imperva ID of the onboarded website. | [optional] 
**domain** | **str** | The name of the domain to add | [optional] 
**auto_discovered** | **bool** | CNAME reuse domain that was discovered automatically by Imperva proxy | [optional] 
**main_domain** | **bool** | Indicates if the domain is primary domain or alternative domain | [optional] 
**managed** | **bool** | Indicates that the primary domain does not have any alternative domains | [optional] 
**sub_domains** | [**list[WildCardSubDomainDetails]**](WildCardSubDomainDetails.md) |  | [optional] 
**validation_method** | **str** | The method used to validate ownership of the domain. Possible values: CNAME, TXT, A | [optional] 
**validation_code** | **str** | The code that should be used to validate ownership of the domain | [optional] 
**cname_redirection_record** | **str** | The CNAME value that should be used for CNAME reuse for the alternative domains. | [optional] 
**status** | **str** | The domain ownership verification status. Possible values: BYPASSED, MISCONFIGURED, VERIFIED, PROTECTED | [optional] 
**creation_date** | **int** | The date of the domain creation  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

