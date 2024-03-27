from .api.compose_api import ComposeApi
from .api.define_api import DefineApi
from .models.prompt import Prompt
from .models.parts import Parts
from .configuration import Configuration
from .api_client import ApiClient


class client:
    def __init__(self, auth_token=None, base_url="https://jsonmode.com/v1/"):
        config = Configuration()
        config.host = base_url
        if auth_token:
            config.api_key["Authorization"] = f"Bearer {auth_token}"
        self.api_client = ApiClient(configuration=config)

    def compose(self, prompt_text):
        api_instance = ComposeApi(self.api_client)
        prompt = Prompt(prompt=prompt_text)
        return api_instance.compose_prompt_compose_post(prompt)

    def define(self, schema_desc, data):
        api_instance = DefineApi(self.api_client)
        parts = Parts(schema_desc=schema_desc, data=data)
        return api_instance.define_prompt_parts_define_post(parts=parts)
