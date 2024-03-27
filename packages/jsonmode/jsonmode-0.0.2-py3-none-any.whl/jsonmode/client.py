from .api_client import ApiClient
from .api.compose_api import ComposeApi
from .api.define_api import DefineApi  
from .models.prompt import Prompt
from .models.parts import Parts

class client:
    def __init__(self, base_url="http://0.0.0.0:8000"):
        self.api_client = ApiClient(base_url=base_url)
        self.compose_api = ComposeApi(api_client=self.api_client)
        self.define_api = DefineApi(api_client=self.api_client)

    def compose(self, prompt):
        prompt_model = Prompt(prompt=prompt)
        return self.compose_api.compose_prompt_compose_post(prompt=prompt_model)

    def define(self, schema_desc, data):
        parts_model = Parts(schema_desc=schema_desc, data=data)
        return self.define_api.define_prompt_parts_define_post(parts_data=parts_model)
