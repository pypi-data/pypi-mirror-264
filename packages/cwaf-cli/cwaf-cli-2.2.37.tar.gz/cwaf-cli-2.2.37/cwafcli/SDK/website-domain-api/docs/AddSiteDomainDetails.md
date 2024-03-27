# AddSiteDomainDetails

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**domain** | **str** | The name of the domain to add | 
**strict_mode** | **bool** | Internal use for Terraform. &lt;br&gt;In strict mode, add/delete of hostname is allowed only if it does not affect other hosts in the site. For example, adding a wildcard hostname is forbidden in strict mode if a subdomain of the wildcard already exists as a siteDomain, while in loose mode, the subdomain is converted to a WildCardSubDomain  | [optional] [default to False]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

