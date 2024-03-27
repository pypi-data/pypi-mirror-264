# swagger_client.AccountManagementApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_account**](AccountManagementApi.md#add_account) | **POST** /api/prov/v1/accounts/add | Add a new managed account
[**add_sub_account**](AccountManagementApi.md#add_sub_account) | **POST** /api/prov/v1/subaccounts/add | Add a new sub account
[**delete_account**](AccountManagementApi.md#delete_account) | **POST** /api/prov/v1/accounts/delete | Delete managed account
[**delete_sub_account**](AccountManagementApi.md#delete_sub_account) | **POST** /api/prov/v1/subaccounts/delete | Delete sub account
[**get_account_status**](AccountManagementApi.md#get_account_status) | **POST** /api/prov/v1/account | Get account status
[**get_default_region**](AccountManagementApi.md#get_default_region) | **POST** /api/prov/v1/accounts/data-privacy/show | Get default data storage region
[**get_token**](AccountManagementApi.md#get_token) | **POST** /api/prov/v1/accounts/gettoken | Get account login token
[**list_accounts**](AccountManagementApi.md#list_accounts) | **POST** /api/prov/v1/accounts/list | List managed accounts
[**list_sub_accounts**](AccountManagementApi.md#list_sub_accounts) | **POST** /api/prov/v1/accounts/listSubAccounts | List account&#x27;s sub accounts
[**modify_account_configuration**](AccountManagementApi.md#modify_account_configuration) | **POST** /api/prov/v1/accounts/configure | Modify account configuration
[**modify_account_log_level**](AccountManagementApi.md#modify_account_log_level) | **POST** /api/prov/v1/accounts/setlog | Modify account log level
[**set_default_region**](AccountManagementApi.md#set_default_region) | **POST** /api/prov/v1/accounts/data-privacy/set-region-default | Set default data storage region
[**set_default_siem_storage**](AccountManagementApi.md#set_default_siem_storage) | **POST** /api/prov/v1/accounts/setDefaultSiemStorage | Set Imperva servers for log storage
[**set_storage_to_s3**](AccountManagementApi.md#set_storage_to_s3) | **POST** /api/prov/v1/accounts/setAmazonSiemStorage | Set S3 configuration for log storage
[**set_storage_to_sftp**](AccountManagementApi.md#set_storage_to_sftp) | **POST** /api/prov/v1/accounts/setSftpSiemStorage | Set SFTP server configuration for log storage
[**subscription**](AccountManagementApi.md#subscription) | **POST** /api/prov/v1/accounts/subscription | Get account subscription details
[**test_connection_s3**](AccountManagementApi.md#test_connection_s3) | **POST** /api/prov/v1/accounts/testS3Connection | Test connection with S3 bucket
[**test_connection_sftp**](AccountManagementApi.md#test_connection_sftp) | **POST** /api/prov/v1/accounts/testSftpConnection | Test connection with SFTP server

# **add_account**
> InlineResponse200 add_account(email, parent_id=parent_id, name=name, plan_id=plan_id, ref_id=ref_id, account_name=account_name, account_description=account_description, user_name=user_name, log_level=log_level, logs_account_id=logs_account_id)

Add a new managed account

Available for Reseller accounts only<br/>Use this operation to add a new account that should be managed by the account of the API client (the parent account). The new account will be configured according to the preferences set for the parent account by Imperva. Depending on these preferences, an activation e-mail will be sent to the specified e-mail address. The user responds to the activation e-mail, selects a password, and can then log directly into the Imperva console. The same e-mail address can also be used to send system notifications to the account. The new account is identified by a numeric value as provided by Imperva in the response in the field account_id.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
email = 'email_example' # str | Email address. For example: \"joe@example.com\".
parent_id = 789 # int | The newly created account's parent id. If not specified, the invoking account will be assigned as the parent. (optional)
name = 'name_example' # str | The account owner's name. For example: \"John Doe\". (optional)
plan_id = 'plan_id_example' # str | An identifier of the plan to assign to the new account. For example, ent100 for the Enterprise 100 plan.<br/>Example values:<br/>ent100 | ent50 | ent20 (optional)
ref_id = 'ref_id_example' # str | Customer specific identifier for this operation. (optional)
account_name = 'account_name_example' # str | Account name. (optional)
account_description = 'account_description_example' # str | The account description (optional)
user_name = 'user_name_example' # str | The account owner's name. For example: \"John Doe\". (optional)
log_level = 'log_level_example' # str | Sets the log reporting level for the site.<br/>Possible values: full | security | none | default<br/>Default value is <b>none</b><br/>Available only for customers that purchased the Logs Integration SKU. (optional)
logs_account_id = 'logs_account_id_example' # str | Numeric identifier of the account that purchased the logs integration SKU and which collects the logs.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. Available only for customers that purchased the Logs Integration SKU. (optional)

try:
    # Add a new managed account
    api_response = api_instance.add_account(email, parent_id=parent_id, name=name, plan_id=plan_id, ref_id=ref_id, account_name=account_name, account_description=account_description, user_name=user_name, log_level=log_level, logs_account_id=logs_account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->add_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **str**| Email address. For example: \&quot;joe@example.com\&quot;. | 
 **parent_id** | **int**| The newly created account&#x27;s parent id. If not specified, the invoking account will be assigned as the parent. | [optional] 
 **name** | **str**| The account owner&#x27;s name. For example: \&quot;John Doe\&quot;. | [optional] 
 **plan_id** | **str**| An identifier of the plan to assign to the new account. For example, ent100 for the Enterprise 100 plan.&lt;br/&gt;Example values:&lt;br/&gt;ent100 | ent50 | ent20 | [optional] 
 **ref_id** | **str**| Customer specific identifier for this operation. | [optional] 
 **account_name** | **str**| Account name. | [optional] 
 **account_description** | **str**| The account description | [optional] 
 **user_name** | **str**| The account owner&#x27;s name. For example: \&quot;John Doe\&quot;. | [optional] 
 **log_level** | **str**| Sets the log reporting level for the site.&lt;br/&gt;Possible values: full | security | none | default&lt;br/&gt;Default value is &lt;b&gt;none&lt;/b&gt;&lt;br/&gt;Available only for customers that purchased the Logs Integration SKU. | [optional] 
 **logs_account_id** | **str**| Numeric identifier of the account that purchased the logs integration SKU and which collects the logs.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. Available only for customers that purchased the Logs Integration SKU. | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sub_account**
> InlineResponse2001 add_sub_account(sub_account_name, parent_id=parent_id, ref_id=ref_id, log_level=log_level, logs_account_id=logs_account_id)

Add a new sub account

Use this operation to add a new sub account to be managed by the account of the API client (the parent account).

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
sub_account_name = 'sub_account_name_example' # str | The name of the sub account.
parent_id = 789 # int | The newly created account's parent id. If not specified, the invoking account will be assigned as the parent account. (optional)
ref_id = 'ref_id_example' # str | Customer specific identifier for this operation. (optional)
log_level = 'log_level_example' # str | Sets the log reporting level for the site.<br/>Possible values: full, security, none, default<br/>Available only for customers that purchased the Logs Integration SKU. (optional)
logs_account_id = 'logs_account_id_example' # str | Numeric identifier of the account that purchased the logs integration SKU and which collects the logs.<br/>If not specified, operation will be performed on the account identified by the authentication parameters.<br/>Available only for customers that purchased the Logs Integration SKU. (optional)

try:
    # Add a new sub account
    api_response = api_instance.add_sub_account(sub_account_name, parent_id=parent_id, ref_id=ref_id, log_level=log_level, logs_account_id=logs_account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->add_sub_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sub_account_name** | **str**| The name of the sub account. | 
 **parent_id** | **int**| The newly created account&#x27;s parent id. If not specified, the invoking account will be assigned as the parent account. | [optional] 
 **ref_id** | **str**| Customer specific identifier for this operation. | [optional] 
 **log_level** | **str**| Sets the log reporting level for the site.&lt;br/&gt;Possible values: full, security, none, default&lt;br/&gt;Available only for customers that purchased the Logs Integration SKU. | [optional] 
 **logs_account_id** | **str**| Numeric identifier of the account that purchased the logs integration SKU and which collects the logs.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters.&lt;br/&gt;Available only for customers that purchased the Logs Integration SKU. | [optional] 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_account**
> ApiResult delete_account(account_id)

Delete managed account

Available for Reseller accounts only Use this operation to delete an account.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.

try:
    # Delete managed account
    api_response = api_instance.delete_account(account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->delete_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sub_account**
> ApiResult delete_sub_account(sub_account_id)

Delete sub account

Use this operation to delete a sub account.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
sub_account_id = 789 # int | Numeric identifier of the sub account to operate on.

try:
    # Delete sub account
    api_response = api_instance.delete_sub_account(sub_account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->delete_sub_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sub_account_id** | **int**| Numeric identifier of the sub account to operate on. | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account_status**
> ApiResultAccountStatus get_account_status(account_id=account_id)

Get account status

Use this operation to get account status

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)

try:
    # Get account status
    api_response = api_instance.get_account_status(account_id=account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->get_account_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 

### Return type

[**ApiResultAccountStatus**](ApiResultAccountStatus.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_default_region**
> ApiResult get_default_region(account_id=account_id)

Get default data storage region

Use this operation to get the default data region of the account. (Available for Reseller accounts only)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)

try:
    # Get default data storage region
    api_response = api_instance.get_default_region(account_id=account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->get_default_region: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_token**
> ApiResultGetSsoToken get_token(account_id=account_id, partner_id=partner_id)

Get account login token

Tokens are used instead of user/password based authentication to log in to the Imperva Cloud Security Console. Use this operation to generate a token for an account. The token is valid for 15 minutes.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
partner_id = 'partner_id_example' # str | Numeric identifier of the parent id to operate on (optional)

try:
    # Get account login token
    api_response = api_instance.get_token(account_id=account_id, partner_id=partner_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->get_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **partner_id** | **str**| Numeric identifier of the parent id to operate on | [optional] 

### Return type

[**ApiResultGetSsoToken**](ApiResultGetSsoToken.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_accounts**
> ApiResultListUsers list_accounts(account_id=account_id, page_size=page_size, page_num=page_num)

List managed accounts

Available for Reseller accounts only.<br/>Use this operation to get the list of accounts that are managed by account of the API client (the parent account).

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
page_size = 'page_size_example' # str | The number of objects to return in the response.<br/>Default: 50<br/>Maximum: 100 (optional)
page_num = 'page_num_example' # str | The page to return starting from 0. Default: '0 (optional)

try:
    # List managed accounts
    api_response = api_instance.list_accounts(account_id=account_id, page_size=page_size, page_num=page_num)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->list_accounts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **page_size** | **str**| The number of objects to return in the response.&lt;br/&gt;Default: 50&lt;br/&gt;Maximum: 100 | [optional] 
 **page_num** | **str**| The page to return starting from 0. Default: &#x27;0 | [optional] 

### Return type

[**ApiResultListUsers**](ApiResultListUsers.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sub_accounts**
> list[SubAccountStatus] list_sub_accounts(account_id=account_id, page_size=page_size, page_num=page_num)

List account's sub accounts

Use this operation to get a list of sub accounts that are managed by the account of the API client (the parent account).

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
page_size = 'page_size_example' # str | The number of objects to return in the response.<br/>Default: 50<br/>Maximum: 100 (optional)
page_num = 'page_num_example' # str | The page to return starting from 0. Default: 0 (optional)

try:
    # List account's sub accounts
    api_response = api_instance.list_sub_accounts(account_id=account_id, page_size=page_size, page_num=page_num)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->list_sub_accounts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **page_size** | **str**| The number of objects to return in the response.&lt;br/&gt;Default: 50&lt;br/&gt;Maximum: 100 | [optional] 
 **page_num** | **str**| The page to return starting from 0. Default: 0 | [optional] 

### Return type

[**list[SubAccountStatus]**](SubAccountStatus.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_account_configuration**
> InlineResponse200 modify_account_configuration(param, value, body=body)

Modify account configuration

Use this operation to change the configuration of the account of the API client or one of its managed accounts.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
param = 'param_example' # str | Name of configuration parameter to set.<br/>Possible values for param and value parameters:<br/><ul><li><b>name</b> the updated name.</li><li><b>email</b> the updated e-mail address</li><li><b>plan_id</b> a plan id</li><li><b>error_page_template</b> a Base64 encoded template for an error page.</li><li><b>support_all_tls_versions</b> Use this operation to allow sites in the account to support all TLS versions for connectivity between clients (visitors) and the Imperva service. When this option is set, you can then enable the option per site to support all TLS versions. Possible values: true, false. Note: To remain PCI-compliant, do not enable this option.</li><li><b>naked_domain_san_for_new_www_sites</b> Use this option to determine if the naked domain SAN will be added to the SSL certificate for new www sites. Default value: true.</li><li><b>wildcard_san_for_new_sites</b> Use this option to determine if the wildcard SAN or the full domain SAN is added to the Imperva SSL certificate for new sites. Possible values: true, false, default (determined by plan) Default value: default.</li><li><b>ref_id</b> Sets the Reference ID, a free-text field that enables you to add a unique identifier to correlate an object in our service, such as a protected website, with an object on the customer side.</li><li><b>enable_http2_for_new_sites</b> Use this option to enable HTTP/2 for newly created SSL sites.</li><li><b>enable_http2_to_origin_for_new_sites</b> Use this option to enable HTTP/2 to Origin for newly created SSL sites. This option can only be enabled once HTTP/2 is enabled for newly created sites.</li><li><b>consent_required</b> Blocks Imperva from performing sensitive operations on your behalf. You can then activate consent via the Cloud Security Console UI. Possible values: true, false..</li></ul>
value = 'value_example' # str | According to the configuration paramater used.
body = 'body_example' # str |  (optional)

try:
    # Modify account configuration
    api_response = api_instance.modify_account_configuration(param, value, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->modify_account_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **param** | **str**| Name of configuration parameter to set.&lt;br/&gt;Possible values for param and value parameters:&lt;br/&gt;&lt;ul&gt;&lt;li&gt;&lt;b&gt;name&lt;/b&gt; the updated name.&lt;/li&gt;&lt;li&gt;&lt;b&gt;email&lt;/b&gt; the updated e-mail address&lt;/li&gt;&lt;li&gt;&lt;b&gt;plan_id&lt;/b&gt; a plan id&lt;/li&gt;&lt;li&gt;&lt;b&gt;error_page_template&lt;/b&gt; a Base64 encoded template for an error page.&lt;/li&gt;&lt;li&gt;&lt;b&gt;support_all_tls_versions&lt;/b&gt; Use this operation to allow sites in the account to support all TLS versions for connectivity between clients (visitors) and the Imperva service. When this option is set, you can then enable the option per site to support all TLS versions. Possible values: true, false. Note: To remain PCI-compliant, do not enable this option.&lt;/li&gt;&lt;li&gt;&lt;b&gt;naked_domain_san_for_new_www_sites&lt;/b&gt; Use this option to determine if the naked domain SAN will be added to the SSL certificate for new www sites. Default value: true.&lt;/li&gt;&lt;li&gt;&lt;b&gt;wildcard_san_for_new_sites&lt;/b&gt; Use this option to determine if the wildcard SAN or the full domain SAN is added to the Imperva SSL certificate for new sites. Possible values: true, false, default (determined by plan) Default value: default.&lt;/li&gt;&lt;li&gt;&lt;b&gt;ref_id&lt;/b&gt; Sets the Reference ID, a free-text field that enables you to add a unique identifier to correlate an object in our service, such as a protected website, with an object on the customer side.&lt;/li&gt;&lt;li&gt;&lt;b&gt;enable_http2_for_new_sites&lt;/b&gt; Use this option to enable HTTP/2 for newly created SSL sites.&lt;/li&gt;&lt;li&gt;&lt;b&gt;enable_http2_to_origin_for_new_sites&lt;/b&gt; Use this option to enable HTTP/2 to Origin for newly created SSL sites. This option can only be enabled once HTTP/2 is enabled for newly created sites.&lt;/li&gt;&lt;li&gt;&lt;b&gt;consent_required&lt;/b&gt; Blocks Imperva from performing sensitive operations on your behalf. You can then activate consent via the Cloud Security Console UI. Possible values: true, false..&lt;/li&gt;&lt;/ul&gt; | 
 **value** | **str**| According to the configuration paramater used. | 
 **body** | [**str**](str.md)|  | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_account_log_level**
> ApiResult modify_account_log_level(log_level, account_id=account_id)

Modify account log level

Available for Reseller accounts only<br/>Use this operation to change the account log configuration.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
log_level = 'log_level_example' # str | Sets the log reporting level for the site.<br/> Possible values: full | security | none | default<br/>Available only for customers that purchased the Log Integration SKU.
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)

try:
    # Modify account log level
    api_response = api_instance.modify_account_log_level(log_level, account_id=account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->modify_account_log_level: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **log_level** | **str**| Sets the log reporting level for the site.&lt;br/&gt; Possible values: full | security | none | default&lt;br/&gt;Available only for customers that purchased the Log Integration SKU. | 
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_default_region**
> ApiResult set_default_region(account_id=account_id, data_storage_region=data_storage_region)

Set default data storage region

Use this operation to set the default data region of the account for newly created sites. (Available for Reseller accounts only)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)
data_storage_region = 'data_storage_region_example' # str | The data region to use.<br/>Possible values: US | EU | APAC | AU (optional)

try:
    # Set default data storage region
    api_response = api_instance.set_default_region(account_id=account_id, data_storage_region=data_storage_region)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->set_default_region: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 
 **data_storage_region** | **str**| The data region to use.&lt;br/&gt;Possible values: US | EU | APAC | AU | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_default_siem_storage**
> ApiResult set_default_siem_storage(account_id)

Set Imperva servers for log storage

Use this operation to have your logs saved on Incapsula servers. Once configured, the logs can be retrieved by API calls.  **Note:** Before this operation can be used, logs must be activated using /api/prov/v1/waf-log-setup/activate

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on

try:
    # Set Imperva servers for log storage
    api_response = api_instance.set_default_siem_storage(account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->set_default_siem_storage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_storage_to_s3**
> ApiResult set_storage_to_s3(account_id, bucket_name, access_key, secret_key)

Set S3 configuration for log storage

Use this operation to configure your Amazon cloud storage. Once configured, Imperva logs will be uploaded to the selected location.  **Note:** Before this operation can be used, logs must be activated using /api/prov/v1/waf-log-setup/activate

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on
bucket_name = 'bucket_name_example' # str | S3 bucket name
access_key = 'access_key_example' # str | S3 access key
secret_key = 'secret_key_example' # str | S3 secret key

try:
    # Set S3 configuration for log storage
    api_response = api_instance.set_storage_to_s3(account_id, bucket_name, access_key, secret_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->set_storage_to_s3: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on | 
 **bucket_name** | **str**| S3 bucket name | 
 **access_key** | **str**| S3 access key | 
 **secret_key** | **str**| S3 secret key | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_storage_to_sftp**
> ApiResult set_storage_to_sftp(account_id, host, user_name, password, destination_folder)

Set SFTP server configuration for log storage

Use this operation to configure your SFTP server storage. Once configured, Incapsula logs will be uploaded to the selected location.  **Note:** Before this operation can be used, logs must be activated using /api/prov/v1/waf-log-setup/activate

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on
host = 'host_example' # str | The IP address of your SFTP server
user_name = 'user_name_example' # str | A user name that will be used to log in to the SFTP server
password = 'password_example' # str | A corresponding password for the user account used to log in to the SFTP server
destination_folder = 'destination_folder_example' # str | The path to the directory on the SFTP server

try:
    # Set SFTP server configuration for log storage
    api_response = api_instance.set_storage_to_sftp(account_id, host, user_name, password, destination_folder)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->set_storage_to_sftp: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on | 
 **host** | **str**| The IP address of your SFTP server | 
 **user_name** | **str**| A user name that will be used to log in to the SFTP server | 
 **password** | **str**| A corresponding password for the user account used to log in to the SFTP server | 
 **destination_folder** | **str**| The path to the directory on the SFTP server | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **subscription**
> InlineResponse2002 subscription(account_id=account_id)

Get account subscription details

Use this operation to get subscription details for an account.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 789 # int | Numeric identifier of the account to operate on.<br/>If not specified, operation will be performed on the account identified by the authentication parameters. (optional)

try:
    # Get account subscription details
    api_response = api_instance.subscription(account_id=account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **int**| Numeric identifier of the account to operate on.&lt;br/&gt;If not specified, operation will be performed on the account identified by the authentication parameters. | [optional] 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_connection_s3**
> ApiResult test_connection_s3(account_id, bucket_name, access_key, secret_key, save_on_success=save_on_success)

Test connection with S3 bucket

Use this operation to check that a connection can be created with your Amazon S3 bucket.  **Note:** Before this operation can be used, logs must be activated using /api/prov/v1/waf-log-setup/activate

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on
bucket_name = 'bucket_name_example' # str | S3 bucket name
access_key = 'access_key_example' # str | S3 access key
secret_key = 'secret_key_example' # str | S3 secret key
save_on_success = true # bool | Save this configuration if the test connection was successful. Default value:false (optional)

try:
    # Test connection with S3 bucket
    api_response = api_instance.test_connection_s3(account_id, bucket_name, access_key, secret_key, save_on_success=save_on_success)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->test_connection_s3: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on | 
 **bucket_name** | **str**| S3 bucket name | 
 **access_key** | **str**| S3 access key | 
 **secret_key** | **str**| S3 secret key | 
 **save_on_success** | **bool**| Save this configuration if the test connection was successful. Default value:false | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_connection_sftp**
> ApiResult test_connection_sftp(account_id, host, user_name, password, destination_folder, save_on_success=save_on_success)

Test connection with SFTP server

Use this operation to check that a connection can be created with your SFTP storage.  **Note:** Before this operation can be used, logs must be activated using /api/prov/v1/waf-log-setup/activate

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_id
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Id'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Id'] = 'Bearer'
# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['x-API-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['x-API-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.AccountManagementApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.
host = 'host_example' # str | The IP address of your SFTP server
user_name = 'user_name_example' # str | A user name that will be used to log in to the SFTP server
password = 'password_example' # str | A corresponding password for the user account used to log in to the SFTP server
destination_folder = 'destination_folder_example' # str | The path to the directory on the SFTP server
save_on_success = true # bool | Save this configuration if the test connection was successful. Default value: false (optional)

try:
    # Test connection with SFTP server
    api_response = api_instance.test_connection_sftp(account_id, host, user_name, password, destination_folder, save_on_success=save_on_success)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountManagementApi->test_connection_sftp: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 
 **host** | **str**| The IP address of your SFTP server | 
 **user_name** | **str**| A user name that will be used to log in to the SFTP server | 
 **password** | **str**| A corresponding password for the user account used to log in to the SFTP server | 
 **destination_folder** | **str**| The path to the directory on the SFTP server | 
 **save_on_success** | **bool**| Save this configuration if the test connection was successful. Default value: false | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

