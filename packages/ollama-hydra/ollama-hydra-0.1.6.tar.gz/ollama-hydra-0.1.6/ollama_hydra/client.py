import ollama
from typing import List, Optional, Union, Dict, Any
from dataclasses import dataclass, field, asdict
from autogen.oai.client import ModelClient
import json

class OllamaClient(ModelClient):
    
    def __init__(self, ollama_host:str = '127.0.0.1', 
                 ollama_port: int = 11434, 
                 **kwargs) -> None:
        super().__init__(kwargs)
        self.ollama_host = ollama_host
        self.ollama_port = ollama_port


@dataclass
class OllamaMessage:
    content: Optional[str] = None
    function_call: Optional[dict] = None


@dataclass
class OllamaChoice:
    message: OllamaMessage

@dataclass
class ModelClientResponse:
    class Choice:
        @dataclass
        class Message:
            content: Optional[str] = None  # Initialize with None

        message: Message = field(default_factory=Message)

    choices: List[Choice] = field(default_factory=list)
    model: str = ""

    def to_json(self):
        return json.dumps(asdict(self))


class AutogenClient(OllamaClient):
    def __init__(self,**kwargs):
        super().__init__(kwargs)
        

    def create(self, params: Dict[str, Any], model) -> ModelClient.ModelClientResponseProtocol:
         
        num_of_responses = params.get("n", 1)
        messages = params.get("messages", [])        
        system_message = params.get("system", None)
        stream = params.get("stream", False)
        prompt = params.get("prompt", None)

        # error handling // gating
        if prompt is not None and messages:
            return {
                "message": "Error, use either 'messages' or 'prompt' but not both",
                "code": 404
            }
        elif prompt is None and not messages:
            return {
                "message": "Must pass 'messages' or 'prompt'",
                "code": 404
            }        

        response = ModelClientResponse()
        response.choices = []
        response.model = model

        args = {
            "model": model            
        }
        if prompt is not None:
            args['prompt'] = prompt
            if system_message is not None:
                args['system'] = system_message
        else:
            args['messages'] = messages
            if system_message is not None:
                return {
                    "message": "'system' isn't valid when using 'messages', only when generating with 'prompt'",
                    "code": 404
                }        

        if messages:
            # Use ollama.chat for conversation-style interactions
            chat_response = ollama.chat(**args)
            for _ in range(num_of_responses):
                choice = OllamaChoice(message=OllamaMessage(content=chat_response['message']['content']))
                response.choices.append(choice)
        else:
            # Use ollama.generate for single-prompt generations            
            for _ in range(num_of_responses):
                output = ollama.generate(**args)  #), max_length=max_length)
                choice = OllamaChoice(message=OllamaMessage(content=output))
                response.choices.append(choice)

        return response

    def message_retrieval(
        self, response: ModelClient.ModelClientResponseProtocol
    ) -> Union[List[str], List[ModelClient.ModelClientResponseProtocol.Choice.Message]]:
        choices = response.choices
        return [choice.message for choice in choices]

    def cost(self, response: ModelClient.ModelClientResponseProtocol) -> float:
        # Assuming Ollama doesn't provide cost information, return 0
        return 0.0

    @staticmethod
    def get_usage(response: ModelClient.ModelClientResponseProtocol) -> Dict:
        # Assuming Ollama doesn't provide usage information, return an empty dict
        return {}



