import json
import os

from cwafcli.ABP.swagger_client import *
from cwafcli.ABP.swagger_client.rest import ApiException
from cwafcli.ABP.swagger_client import Configuration


def create_subparser(parent_parser, call, method, param, description):
    website_parser = parent_parser.add_parser(call, help=description)
    # Add subcommand-specific arguments
    if param is not None:
        website_parser.add_argument(param, help=description)
    if method == "PUT" or method == "POST":
        website_parser.add_argument("body", help=description)
    website_parser.set_defaults(func=read, do=call)


def read(args):
    params = vars(args)
    try:
        config = configure()
        instance = AccountApi(ApiClient(config))
        if params["do"] == "v1_account_account_id_get":
            return instance.v1_account_account_id_get(params["account_id"])
    except ApiException as e:
        print(e)
        return e


def get_params() -> list:
    with open("cwafcli/SDK/abp-api/docs/AccountApi.md", "r") as f:
        lines = f.read()
        needed = lines.split("\n------------- | ------------- | -------------\n")

        line = needed[1].split("\n\n")

        items = line[0].strip().split("\n")

        args_params = []
        for item in items:
            call, method, description = item.split("|")
            if "{" and "}" in method:
                param = method.split("}")[0].split("{")[1]
            else:
                param = None
            call = call.split("**]")[0].split("[**")[1]
            method = method.split("** ")[0].split(" **")[1]
            args_params.append((call, method, param, description))
        return args_params


def configure() -> Configuration:
    from ..Config.configuration import IncapConfigurations
    api_id = os.getenv("IMPV_API_ID", IncapConfigurations.get_config("api", 'id'))
    api_key = os.getenv("IMPV_API_KEY", IncapConfigurations.get_config("api", 'key'))
    config = Configuration()
    config.api_key['x-API-Id'] = api_id
    config.api_key['x-API-Key'] = api_key
    config.verify_ssl = True
    config.debug = False
    return config
