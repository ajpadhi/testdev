import pathlib
import tomllib

from pydantic_settings import BaseSettings, SettingsConfigDict

path = pathlib.Path(__file__).parent.absolute()
with open(f"{path}/../pyproject.toml", mode="rb") as f:
    project_data = tomllib.load(f)


app_version = project_data["tool"]["poetry"]["version"]
app_name = project_data["tool"]["poetry"]["name"]
app_title = project_data["tool"]["metadata"]["title"]
app_description = project_data["tool"]["metadata"]["full_description"]


class Settings(BaseSettings):
    mongo_uri: str
    environment: str = "prod"
    logging_level: str = "INFO"
    root_path: str = ""
    ci: bool = False
    mongo_db: str = "acts-activity"
    static_token: str
    acts_gen_user: str
    acts_gen_password: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
