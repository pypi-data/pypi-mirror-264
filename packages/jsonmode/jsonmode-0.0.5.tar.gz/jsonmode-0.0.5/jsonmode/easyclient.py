from .api.compose_api import ComposeApi
from .api.define_api import DefineApi
from .models.prompt import Prompt
from .models.parts import Parts
from .configuration import Configuration
from .api_client import ApiClient


class ExtendedApiClient(ApiClient):
    def __init__(self, configuration=None, auth_token=None):
        super().__init__(configuration=configuration)
        if auth_token:
            # Directly set the Authorization header to be used in all requests
            self.default_headers["Authorization"] = f"Bearer {auth_token}"


class client:
    def __init__(self, auth_token=None, base_url="https://jsonmode.com/v1/"):
        config = Configuration()
        config.host = base_url
        self.api_client = ExtendedApiClient(configuration=config, auth_token=auth_token)

    def compose(self, prompt_text):
        api_instance = ComposeApi(self.api_client)
        prompt = Prompt(prompt=prompt_text)
        prompt_dict = prompt.dict()
        return api_instance.compose_prompt_compose_post(prompt_dict)

    def define(self, schema_desc, data):
        api_instance = DefineApi(self.api_client)
        parts = Parts(schema_desc=schema_desc, data=data)
        parts_json = parts.dict()
        return api_instance.define_prompt_parts_define_post(parts=parts_json)
