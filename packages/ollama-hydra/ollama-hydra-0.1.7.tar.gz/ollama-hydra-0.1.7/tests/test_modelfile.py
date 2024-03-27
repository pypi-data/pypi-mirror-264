
import os
from ollama_hydra.modelfile import Modelfile

def test_stop_w_spaces():
    modelfile = Modelfile.from_modelfile('tests/modelfiles/t2.modelfile')
    assert modelfile.parameters['stop'] == ['\"[INST] Hello World\"','\"[/INST]\"']
    assert modelfile.model == 'mistral:latest'

def test_modelfile_init():
    modelfile = Modelfile.from_modelfile('tests/modelfiles/t1.modelfile')

    assert modelfile.model ==  'codellama:latest'
    assert modelfile.parameters['temperature'] == 0.5
    assert modelfile.system_message is not None

def test_serialization():
    modelfile = Modelfile.from_modelfile('tests/modelfiles/t1.modelfile')

    modelfile_2 = Modelfile(modelfile_text=modelfile.to_modelfile_text())

    assert modelfile.model == modelfile_2.model
    assert modelfile.system_message == modelfile_2.system_message
    assert modelfile.parameters['temperature'] == modelfile_2.parameters['temperature']
    assert modelfile.to_modelfile_text() == modelfile_2.to_modelfile_text()


    
def test_messages_section():
    modelfile = Modelfile(model="mistral:latest")    

    modelfile.messages.append("Message 1")
    modelfile.messages.append("Message 2")

    text = modelfile.to_modelfile_text()
    assert "Message 1" in text
    assert "Message 2" in text


def test_stop_parameter_init():
    modelfile = Modelfile(model="mistral:latest", stop="[INST]")
    assert modelfile.parameters['stop'] == ["[INST]"]



def test_multiple_stop():
    modelfile = Modelfile(model="mistral:latest", stop=["[INST]", "[/INST]"])
    assert modelfile.parameters['stop'] == ["[INST]", "[/INST]"]





