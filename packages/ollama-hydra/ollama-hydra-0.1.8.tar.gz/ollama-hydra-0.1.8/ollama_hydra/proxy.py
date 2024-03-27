import asyncio
import requests
import ollama
import json
from time import sleep
import os
from enum import Enum
import functools
from ollama_hydra.modelfile import Modelfile
from ollama_hydra.client import AutogenClient

model_port_mappings = {}  
ollama_port = os.environ.get("OLLAMA_PORT", 11434)  # Port for ollama.list() API
ollama_host = os.environ.get("OLLAMA_HOST", '127.0.0.1') 
next_available_port = os.environ.get("NEXT_AVAILABLE_PORT", 11435)  # Starting port for dynamic assignment


print(f"Connecting to OLLAMA on {ollama_host}")

        
ollama_url = f'http://localhost:{ollama_port}'

clients = [AutogenClient(ollama_host=ollama_host, ollama_port=ollama_port)]


class ModelMapping:

    def __init__(self, modelfile: Modelfile, port: int) -> None:        
        self.port = port
        self.modelfile = modelfile

    @staticmethod
    def create_mapping(model_reference: str, port: int) -> 'ModelMapping':
        if model_reference is not None:
            show_ret = ollama.show(model_reference)
            modelfile_text = show_ret['modelfile']
            mf = Modelfile(model_reference=model_reference, modelfile_text=modelfile_text)
        else:
            mf = None
        
        mm = ModelMapping(modelfile=mf, port=port)
        return mm
   
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ModelMapping):
            return False
        
        return self.port == value.port and \
            self.modelfile == value.modelfile
    
    @property
    def model(self):
        if self.modelfile is not None:
            return self.modelfile.model_reference
        
        return None



async def handle_request(reader, writer, port):
    try:
        request_line = await reader.readline()
        method, path, _ = request_line.decode().strip().split()
        function_name = path[1:]

        headers = {}
        while True:
            header_line = await reader.readline()
            if header_line == b'\r\n':
                break
            header_key, header_value = header_line.decode().strip().split(':', 1)
            headers[header_key] = header_value.strip()

        # Gather request data
        request_data = {}
        content_length = int(headers.get('Content-Length', 0))
        if content_length > 0:
            request_body = await reader.read(content_length)
            if headers.get('Content-Type', '').startswith('application/json'):
                request_data = json.loads(request_body.decode())
            else:
                request_data = request_body.decode()

        modelfile = model_port_mappings[port]
        
        selected_client = None
        for client in clients:
            if hasattr(client, function_name):
                selected_client = client
                break

        if selected_client:
            client_func = getattr(selected_client, function_name)
            model = modelfile.model          
            if model is None and "model" in request_data:
                model = request_data.get("model", None)
                            
            if model is not None:
                response_data = client_func(request_data, model=model)
            else:
                response_data = {
                    "message": "'model' is required parameter. Either use a mapped port, or if unmapped pass valid ollama 'model' reference",
                    "code": 404
                }
            if isinstance(response_data, dict) and "code" in response_data:
                status_code = response_data.get('code', 200)
                if status_code == 200:
                    reason = "OK"
                else:
                    reason = "Error"
            else:
                status_code = 200
                reason = "OK"
        else:        
            response_data = { "message": f"No client found to handle the request on `{path}`.", "code": 404 }
            status_code = 404
            reason = "Not Found"
    except Exception as e:
        error_message = f"Error handling request: {e}"
        response_data = { "message": error_message, "code": 503 }
        status_code = 503
        reason = "Server Error"            

    try:
        # Convert response data to JSON
        if hasattr(response_data, 'to_json'):
            response_data = response_data.to_json()
    except Exception as e:
        em = f"Error parsing object of type {type(response_data)}"
        print(em)
        response_data = {"message": em, "code": 503}
        status_code = 503
        reason = "Server Error"

    try:       
        response_body = json.dumps(response_data).encode()

        # Write response headers
        writer.write(f"HTTP/1.1 {status_code} {reason}\r\n".encode())
        writer.write(b"Content-Type: application/json\r\n")
        writer.write(f"Content-Length: {len(response_body)}\r\n".encode())
        writer.write(b"\r\n")

        # Write response body
        writer.write(response_body)
        await writer.drain()
        writer.close()

    except Exception as e:
        print(f"Error writing request to caller {e}")
        

def _update_model_mapping_helper():        
    global model_port_mappings, next_available_port
    try:
        models = ollama.list()
        models = models.get('models', [])
        new_mappings = {}
        port = next_available_port
        new_mappings[port] = ModelMapping.create_mapping(None, port)
        port += 1
        for model in models:            
            port += 1
            new_mappings[port] = ModelMapping.create_mapping(model['model'], port)

        if new_mappings != model_port_mappings:
            print("\n\nModel Mappings:\n")
            for p, m in new_mappings.items():
                if m.model is not None:
                    print(f"\t{m.port} -> {m.model}")
                else:
                    print(f"\t{m.port} -> OPEN // use 'model' to set on a call-by-call basis")

        model_port_mappings = new_mappings
        
    except Exception as e:
        print(f"Error updating model mappings: {e}")

async def start_servers(host, port):
    # Create a partial function with the port number pre-filled
    handle_request_with_port = functools.partial(handle_request, port=port)

    server = await asyncio.start_server(handle_request_with_port, host, port)
    await server.serve_forever()


def print_startup():
    print("\n\n")
    print(("-" * 50))
    print("Hydra Proxy Startup Complete")
    print(("-" * 50))
    print("\n\n")


def enable_sockets():
    try:
        host = '127.0.0.1'        
            
        if len(model_port_mappings) == 0:
            print("Unable to find any mappings. Exiting.")            
            # exit program
            return
        
        loop = asyncio.new_event_loop()
        for si in model_port_mappings.keys():
            i = int(si)
            loop.create_task(start_servers(host, i))

        print_startup()

        loop.run_forever()
    except Exception as exc:
        print(exc)

def main():
    _update_model_mapping_helper()
    enable_sockets()

if __name__ == "__main__":
    main()
