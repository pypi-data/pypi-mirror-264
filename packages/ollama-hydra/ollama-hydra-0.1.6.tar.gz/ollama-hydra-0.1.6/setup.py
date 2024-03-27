from setuptools import setup, find_packages

setup(
    name='ollama-hydra',
    version='0.1.6',
    description='Proxy server for managing multiple Ollama models for AutoGen Agents', 
    long_description='', 
    author='Cyrus Radfar',
    author_email='support@v1.co',  
    url='https://github.com/sendthis-ai/ollama-hydra',
    packages=find_packages(),
    install_requires=[
        'requests',
        'ollama', 
        'pyautogen',
        'dockerfile-parse'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ollama-hydra = ollama_hydra.proxy:main',
            'ohydra = ollama_hydra.proxy:main'  # Added alias
        ],
    },
)
