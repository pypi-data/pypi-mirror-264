# ApiResultSiteStatus

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**res** | **int** | res - contains specific error code | [optional] 
**res_message** | **str** |  | [optional] 
**debug_info** | **list[dict(str, object)]** |  | [optional] 
**site_id** | **int** |  | [optional] 
**status_enum** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**domain** | **str** |  | [optional] 
**account_id** | **int** |  | [optional] 
**acceleration_level** | **str** |  | [optional] 
**acceleration_level_raw** | **str** |  | [optional] 
**site_creation_date** | **int** |  | [optional] 
**ips** | **list[object]** |  | [optional] 
**dns** | [**list[DnsInstructionItem]**](DnsInstructionItem.md) |  | [optional] 
**original_dns** | [**list[DnsInstructionItem]**](DnsInstructionItem.md) |  | [optional] 
**warnings** | [**list[SiteConfigurationWarning]**](SiteConfigurationWarning.md) |  | [optional] 
**active** | **str** |  | [optional] 
**support_all_tls_versions** | **bool** |  | [optional] 
**use_wildcard_san_instead_of_full_domain_san** | **bool** |  | [optional] 
**add_naked_domain_san** | **bool** |  | [optional] 
**set_site_cookies_without_domain** | **bool** |  | [optional] 
**enable_http_between_imperva_and_origin** | **str** |  | [optional] 
**additional_errors** | **list[object]** |  | [optional] 
**display_name** | **str** |  | [optional] 
**security** | **list[dict(str, object)]** |  | [optional] 
**ssl** | **list[dict(str, object)]** |  | [optional] 
**site_dual_factor_settings** | [**SiteDualFactorSettings**](SiteDualFactorSettings.md) |  | [optional] 
**request_body_timeouts** | [**RequestBodyTimeoutDTO**](RequestBodyTimeoutDTO.md) |  | [optional] 
**login_protect** | [**LoginProtectApiResult**](LoginProtectApiResult.md) |  | [optional] 
**performance_configuration** | [**PerformanceConfigurationApiResult**](PerformanceConfigurationApiResult.md) |  | [optional] 
**extended_ddos** | **int** |  | [optional] 
**incap_rules** | [**list[IncapRuleApiResult]**](IncapRuleApiResult.md) |  | [optional] 
**restricted_cname_reuse** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

