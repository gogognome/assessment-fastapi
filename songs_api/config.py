import yaml
from pydantic import BaseModel


# Define a Pydantic model for the configuration.
class DatabaseConfig(BaseModel):
    url: str


class Config(BaseModel):
    database: DatabaseConfig


def load_config(file_path: str) -> Config:
    with open(file_path) as file:
        config_data = yaml.safe_load(file)

    return Config(**config_data)
