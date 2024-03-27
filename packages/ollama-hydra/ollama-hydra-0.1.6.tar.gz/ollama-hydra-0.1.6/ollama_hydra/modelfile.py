
import json
from dockerfile_parse import DockerfileParser

ModelParameterDefaults = {
    'mirostat': 0,
    'mirostat_eta': 0.1, 
    'mirostat_tau': 5.0,
    'num_ctx': 4096,
    'num_gqa': 1,
    'num_gpu': 1,   
    'num_thread': 8,
    'repeat_last_n': 64,
    'repeat_penalty': 1.0,
    'temperature': 0.7,
    'seed': 0,
    'stop': "AI assistant:",
    'tfs_z': 1,
    'num_predict': 128,
    'top_k': 40,
    'top_p': 0.9,
    'rope_frequency_base': 1e+6
}

class Modelfile:

    def __init__(self, 
                model_reference: str=None,
                modelfile_text: str=None, 
                template: str=None,
                messages: list=[],
                system_message: str=None, 
                parameters: dict={}, 
                **kwargs):
        
        self.messages = messages
        self.parameters = parameters
        self.model = model_reference
        self.model_reference = model_reference        
        self.template = template
        self.system_message = system_message

        if modelfile_text is not None:
            self._from_modelfile_text(modelfile_text)

        if kwargs is not None:
            self.set_parameters(kwargs) 
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Modelfile):
            return False
        
        return self.model_reference == value.model_reference

    def _wrap(self, value:str, single_quote: bool=False) -> str:
        if value is not None:            
            value = value.strip()
            if len(value) != 0:                    
                if not value.startswith('\"'):
                    if single_quote:
                        value = f"\"{value}\""
                    else:
                        value = f'\"\"\"{value}\"\"\"'

        return value
    
    def _from_modelfile_text(self, modelfile_text: str):
        dfp = DockerfileParser()
        dfp.content = modelfile_text
        ret = json.loads(dfp.json)
        for obj in ret:
            key = next(iter(obj)).upper()
            value = obj[key]
            if key == 'PARAMETER':
                # split the value
                toks = value.split(" ")
                param_name = toks[0]
                if len(toks) == 2:
                    param_value = Modelfile.cast_to_type(param_name, toks[1])
                else:
                    param_value = " ".join(toks[1:])
                # handle multiple stop parameters
                if param_name == 'stop':
                    if self.parameters.get(param_name) is not None:
                        self.parameters[param_name].append(param_value)
                    else: 
                        self.parameters[param_name] = [param_value]
                else:
                    # otherwise, only one param is allowed 
                    #   therefore the last key will set the final value
                    self.parameters[param_name] = param_value
            elif key == 'TEMPLATE':
                self.template = value
            elif key == "FROM":
                self.model = value
                if self.model_reference is None:
                    self.model_reference = self.model
            elif key == "SYSTEM":
                self.system_message = value
            elif key == "MESSAGE":
                self.messages.append(value)

    def to_modelfile(self, filename: str):
        with open(filename, 'w') as f:
            f.write(self.to_modelfile_text())

    @staticmethod
    def from_modelfile(filename: str) -> 'Modelfile':
        from os import path
        if path.exists(filename):
            with open(filename, 'r') as f:
                return Modelfile(modelfile_text=f.read())
            
        raise FileNotFoundError(f"File not found: {filename}")
    
    @staticmethod
    def cast_to_type(key, str_value):
        """Casts a string value to the type of the corresponding key in a dictionary.

        Args:
            key: The key in the dictionary.
            str_value: The value to be cast, as a string.

        Returns:
            The cast value.

        Raises:
            ValueError: If the key is not found in the dictionary or if the cast fails.
        """

        if key not in ModelParameterDefaults:
            raise ValueError(f"Key {key} not found in ModelParameterDefaults")

        try:
            return type(ModelParameterDefaults[key])(str_value)
        except (ValueError, TypeError):
            raise ValueError(f"Failed to cast value '{str_value}' for key {key}")
                        

    def to_modelfile_text(self):
        # start with Model name
        return_string = f"FROM {self.model}\n"

        # continue to parameters section
        return_string += self.parameter_string + '\n' 
    
        if self.template:
            return_string += f"TEMPLATE {self._wrap(self.template)}\n"

        if self.system_message:
            return_string += f"SYSTEM {self._wrap(self.system_message)}\n"

        if self.messages:
            return_string += '\n'.join([f"MESSAGE {self._wrap(message)}" for message in self.messages]) + '\n'

        return return_string
        
    @property
    def parameter_string(self):
        for key, value in self.parameters.items():
            arr = []
            if isinstance(value, list):
                arr.extend([f"PARAMETER {key} {self._wrap(v, single_quote=True)}" for v in value])
            else:
                arr.append(f"PARAMETER {key} {value}")

        return "\n".join(arr)

    def set_parameters(self, params: dict):
        for key, value in params.items(): 
              self.set_parameter(key, value)

    def set_parameter(self, key, value):
        if key not in ModelParameterDefaults:
            raise ValueError(f"Invalid parameter name: {key}")
        
        if key == 'stop' and isinstance(value, str):
            # use array
            value = [value]

        self.parameters[key] = value
