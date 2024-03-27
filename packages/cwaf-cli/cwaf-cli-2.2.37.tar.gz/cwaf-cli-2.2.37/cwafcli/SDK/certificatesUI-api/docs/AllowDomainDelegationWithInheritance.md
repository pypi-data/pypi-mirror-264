# AllowDomainDelegationWithInheritance

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The domain id. | [optional] 
**name** | **str** | The domain name. | [optional] 
**creation_date** | **int** | The domain creation date. | [optional] 
**status** | **str** | The domain status. Possible values: CONFIGURED, NOT_CONFIGURED | [optional] 
**status_since** | **int** | The date the domain status was last modified. | [optional] 
**last_status_check** | **int** | The date the domain status was last verified. | [optional] 
**inherited** | **bool** | CNAME validation is automatically inherited from a parent domain that is delegated to Imperva. When domain delegation configured (true) for a specific subdomain, its CNAME value overrides the current setting of the parent domain. | [optional] 
**cname_record_value** | **str** | The CNAME record value to use to configure this domain for delegation. | [optional] 
**cname_record_host** | **str** | The CNAME record host to use. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

