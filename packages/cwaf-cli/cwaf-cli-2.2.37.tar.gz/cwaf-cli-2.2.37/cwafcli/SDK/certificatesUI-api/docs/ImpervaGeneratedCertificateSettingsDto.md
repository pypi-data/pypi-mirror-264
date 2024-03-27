# ImpervaGeneratedCertificateSettingsDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delegation** | [**AccountDtoSSLDelegationSettingsDto**](AccountDtoSSLDelegationSettingsDto.md) |  | [optional] 
**use_wild_card_san_instead_of_fqdn** | **bool** | Adds the wildcard SAN to the Imperva SSL certificate instead of the full domain SAN. The value you assign is used as the default option when onboarding new websites. | [optional] [default to True]
**add_naked_domain_san_for_www_sites** | **bool** | For sites with the www prefix, adds the naked domain SAN to the Imperva SSL certificate. The value you assign is used as the default option when onboarding new websites. | [optional] [default to True]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

