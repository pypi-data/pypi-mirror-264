from openfinance.utils.singleton import singleton
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.webgpt import WebGPT
from openfinance.agentflow.llm.aliyungpt import AliyunGPT
from openfinance.config import Config

@singleton
class ModelManager:
    def __init__(
        self, 
        config
    ):
        self.config = config
        self.models = {}        
        for k, v in self.config.get("models").items():
            if k == "aliyungpt":
                self.register_model(
                    k, AliyunGPT(
                        model=self.conf(k, "model_name"),
                        api_key=self.conf(k, "token"),
                        base_url=self.conf(k, "api_base"),                                                
                    )
                )
            elif k == "webgpt":
                self.register_model(
                    k, WebGPT(
                        model=self.conf(k, "model_name"),
                        api_key=self.conf(k, "token"),
                        base_url=self.conf(k, "api_base"),                                                
                    )
                )
            elif k == "chatgpt":
                self.register_model(
                    k, ChatGPT(
                        model=self.conf(k, "model_name"),
                        api_key=self.conf(k, "token"),
                        base_url=self.conf(k, "api_base"),                                                
                    )
                )                

    def conf(
        self,
        model,
        key
    ):
        return self.config.get("models")[model][key]

    def register_model(
        self, 
        model_name, 
        model_class
    ):
        self.models[model_name] = model_class
        
        if not self.config.get(model_name):
            self.config.set(model_name, {})
            
    def get_model(
        self, 
        model_name
    ):
        return self.models[model_name]

