from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="samgpt",
    version="0.1",
    packages=["samgpt", 
              "samgpt.agents", 
              "samgpt.nlp", 
              "samgpt.planning", 
              "samgpt.ui", 
              "samgpt.utils"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "samgpt=samgpt.main:main"
        ]
    }
)
