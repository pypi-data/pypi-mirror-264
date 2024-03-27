# swagger_client.LoginProtectApi

All URIs are relative to *https://my.imperva.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_lp_user**](LoginProtectApi.md#add_lp_user) | **POST** /api/prov/v1/sites/lp/add-user | Add login protect user
[**configure_protected_app_by_lp**](LoginProtectApi.md#configure_protected_app_by_lp) | **POST** /api/prov/v1/sites/lp/configure-app | Configure login protect on admin areas
[**edit_lp_user**](LoginProtectApi.md#edit_lp_user) | **POST** /api/prov/v1/sites/lp/edit-user | Edit login protect user
[**get_lp_users**](LoginProtectApi.md#get_lp_users) | **POST** /api/prov/v1/sites/lp/users | Get login protect users
[**modify_lp_site_configuration**](LoginProtectApi.md#modify_lp_site_configuration) | **POST** /api/prov/v1/sites/lp/configure | Modify Site Login Protect Configuration
[**remove_lp_user**](LoginProtectApi.md#remove_lp_user) | **POST** /api/prov/v1/sites/lp/remove | Remove login protect user
[**send_sms**](LoginProtectApi.md#send_sms) | **POST** /api/prov/v1/sites/lp/send-sms | Send SMS to user

# **add_lp_user**
> ApiResult add_lp_user(account_id, email, name=name, phone=phone, is_phone_verified=is_phone_verified, is_email_verified=is_email_verified, should_send_activation_email=should_send_activation_email)

Add login protect user

Use this operation to add a Login Protect user for a site.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.
email = 'email_example' # str | Email address.
name = 'name_example' # str | Example: John Smith (optional)
phone = 'phone_example' # str | Phone number. For example: \"1-8662507659\" (optional)
is_phone_verified = true # bool | Whether or not to skip phone verification. (optional)
is_email_verified = true # bool | Whether or not to skip email address verification. (optional)
should_send_activation_email = true # bool | Whether or not to send activation email to user. (optional)

try:
    # Add login protect user
    api_response = api_instance.add_lp_user(account_id, email, name=name, phone=phone, is_phone_verified=is_phone_verified, is_email_verified=is_email_verified, should_send_activation_email=should_send_activation_email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->add_lp_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 
 **email** | **str**| Email address. | 
 **name** | **str**| Example: John Smith | [optional] 
 **phone** | **str**| Phone number. For example: \&quot;1-8662507659\&quot; | [optional] 
 **is_phone_verified** | **bool**| Whether or not to skip phone verification. | [optional] 
 **is_email_verified** | **bool**| Whether or not to skip email address verification. | [optional] 
 **should_send_activation_email** | **bool**| Whether or not to send activation email to user. | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **configure_protected_app_by_lp**
> InlineResponse20014 configure_protected_app_by_lp(site_id, protected_app=protected_app)

Configure login protect on admin areas

Use this operation to configure Login Protect on wordpress | joomla | phpbb admin areas.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | Numeric identifier of the site to operate on.
protected_app = 'protected_app_example' # str | Protect admin areas of joomla | wordpress | phpBB. (optional)

try:
    # Configure login protect on admin areas
    api_response = api_instance.configure_protected_app_by_lp(site_id, protected_app=protected_app)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->configure_protected_app_by_lp: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| Numeric identifier of the site to operate on. | 
 **protected_app** | **str**| Protect admin areas of joomla | wordpress | phpBB. | [optional] 

### Return type

[**InlineResponse20014**](InlineResponse20014.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_lp_user**
> ApiResult edit_lp_user(account_id, email, name=name, phone=phone, is_phone_verified=is_phone_verified, is_email_verified=is_email_verified, should_send_activation_email=should_send_activation_email)

Edit login protect user

Edit Login Protect user's settings.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.
email = 'email_example' # str | Email address.
name = 'name_example' # str | Example: John Smith (optional)
phone = 'phone_example' # str | Phone number. For example: \"1-8662507659\" (optional)
is_phone_verified = true # bool | Whether or not to skip phone verification. (optional)
is_email_verified = true # bool | Whether or not to skip email address verification. (optional)
should_send_activation_email = true # bool | Whether or not to send activation email to user. (optional)

try:
    # Edit login protect user
    api_response = api_instance.edit_lp_user(account_id, email, name=name, phone=phone, is_phone_verified=is_phone_verified, is_email_verified=is_email_verified, should_send_activation_email=should_send_activation_email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->edit_lp_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 
 **email** | **str**| Email address. | 
 **name** | **str**| Example: John Smith | [optional] 
 **phone** | **str**| Phone number. For example: \&quot;1-8662507659\&quot; | [optional] 
 **is_phone_verified** | **bool**| Whether or not to skip phone verification. | [optional] 
 **is_email_verified** | **bool**| Whether or not to skip email address verification. | [optional] 
 **should_send_activation_email** | **bool**| Whether or not to send activation email to user. | [optional] 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_lp_users**
> InlineResponse20015 get_lp_users(account_id)

Get login protect users

Use this operation to get the account's login protect user list.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.

try:
    # Get login protect users
    api_response = api_instance.get_lp_users(account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->get_lp_users: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 

### Return type

[**InlineResponse20015**](InlineResponse20015.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_lp_site_configuration**
> InlineResponse20014 modify_lp_site_configuration(site_id, enabled=enabled, specific_users_list=specific_users_list, send_lp_notifications=send_lp_notifications, allow_all_users=allow_all_users, authentication_methods=authentication_methods, urls=urls, url_patterns=url_patterns)

Modify Site Login Protect Configuration

Use this operation to change Login Protect settings for a site.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
site_id = 789 # int | Numeric identifier of the site to operate on.
enabled = true # bool | Pass true to enable login protect on site, and false to disable it.<br/>Default: true (optional)
specific_users_list = 'specific_users_list_example' # str | Comma separated email list to set login protect users for the site. If the list is empty all users will be allowed to access the site using Login Protect. (optional)
send_lp_notifications = true # bool | Pass true to send notification on successful login using login protect.<br/>Default: false (optional)
allow_all_users = true # bool | Pass true to allow all login protect users to access the site. If you want to allow only a specific list of users to access the site using Login Protect set this to false, and add the list to specific_user_list.<br/>Default: true (optional)
authentication_methods = 'authentication_methods_example' # str | Comma separated list of allowed authentication methods: sms | email | ga (optional)
urls = 'urls_example' # str | A comma separated list of resource paths. For example, /home and /admin/index.html are resource paths, while <a href=\"http://www.example.com/home\">http://www.example.com/home</a> is not. Each URL should be encoded separately using percent encoding as specified by RFC 3986 (<a href=\"http://tools.ietf.org/html/rfc3986#section-2.1\">http://tools.ietf.org/html/rfc3986#section-2.1</a>). An empty URL list will remove all URLs. (optional)
url_patterns = 'url_patterns_example' # str | A comma separated list of url patterns. Possible values: contains | equals | prefix | suffix | not_equals | not_contain | not_prefix | not_suffix. The patterns should be in accordance with the matching urls sent by the urls parameter. (optional)

try:
    # Modify Site Login Protect Configuration
    api_response = api_instance.modify_lp_site_configuration(site_id, enabled=enabled, specific_users_list=specific_users_list, send_lp_notifications=send_lp_notifications, allow_all_users=allow_all_users, authentication_methods=authentication_methods, urls=urls, url_patterns=url_patterns)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->modify_lp_site_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **int**| Numeric identifier of the site to operate on. | 
 **enabled** | **bool**| Pass true to enable login protect on site, and false to disable it.&lt;br/&gt;Default: true | [optional] 
 **specific_users_list** | **str**| Comma separated email list to set login protect users for the site. If the list is empty all users will be allowed to access the site using Login Protect. | [optional] 
 **send_lp_notifications** | **bool**| Pass true to send notification on successful login using login protect.&lt;br/&gt;Default: false | [optional] 
 **allow_all_users** | **bool**| Pass true to allow all login protect users to access the site. If you want to allow only a specific list of users to access the site using Login Protect set this to false, and add the list to specific_user_list.&lt;br/&gt;Default: true | [optional] 
 **authentication_methods** | **str**| Comma separated list of allowed authentication methods: sms | email | ga | [optional] 
 **urls** | **str**| A comma separated list of resource paths. For example, /home and /admin/index.html are resource paths, while &lt;a href&#x3D;\&quot;http://www.example.com/home\&quot;&gt;http://www.example.com/home&lt;/a&gt; is not. Each URL should be encoded separately using percent encoding as specified by RFC 3986 (&lt;a href&#x3D;\&quot;http://tools.ietf.org/html/rfc3986#section-2.1\&quot;&gt;http://tools.ietf.org/html/rfc3986#section-2.1&lt;/a&gt;). An empty URL list will remove all URLs. | [optional] 
 **url_patterns** | **str**| A comma separated list of url patterns. Possible values: contains | equals | prefix | suffix | not_equals | not_contain | not_prefix | not_suffix. The patterns should be in accordance with the matching urls sent by the urls parameter. | [optional] 

### Return type

[**InlineResponse20014**](InlineResponse20014.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_lp_user**
> ApiResult remove_lp_user(account_id, email)

Remove login protect user

Use this operation to remove a login protect user from an account's user list.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.
email = 'email_example' # str | Email address.

try:
    # Remove login protect user
    api_response = api_instance.remove_lp_user(account_id, email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->remove_lp_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 
 **email** | **str**| Email address. | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_sms**
> ApiResult send_sms(account_id, email, sms_text)

Send SMS to user

Use this operation to send an SMS to a login protect user.

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
api_instance = swagger_client.LoginProtectApi(swagger_client.ApiClient(configuration))
account_id = 'account_id_example' # str | Numeric identifier of the account to operate on.
email = 'email_example' # str | Email address.
sms_text = 'sms_text_example' # str | Text that will be sent in SMS.

try:
    # Send SMS to user
    api_response = api_instance.send_sms(account_id, email, sms_text)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginProtectApi->send_sms: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| Numeric identifier of the account to operate on. | 
 **email** | **str**| Email address. | 
 **sms_text** | **str**| Text that will be sent in SMS. | 

### Return type

[**ApiResult**](ApiResult.md)

### Authorization

[api_id](../README.md#api_id), [api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

