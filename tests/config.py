import pytest
import yaml

class Config:
    @classmethod
    def get(cls) -> dict:
        with open('tests/dev.yaml', 'r') as file:
            data = yaml.safe_load(file)
        return data
