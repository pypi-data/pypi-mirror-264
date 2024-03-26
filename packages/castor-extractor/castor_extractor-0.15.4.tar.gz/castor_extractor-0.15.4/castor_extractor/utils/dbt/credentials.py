from pydantic import BaseSettings, Extra, Field

_DEFAULT_CLOUD_URL = "https://cloud.getdbt.com"


class DbtCredentials(BaseSettings):
    """dbt credentials: host has default value"""

    host: str = Field(default=_DEFAULT_CLOUD_URL, env="CASTOR_DBT_HOST")
    job_id: str = Field(..., env="CASTOR_DBT_JOB_ID")
    token: str = Field(..., env="CASTOR_DBT_TOKEN")

    class Config:
        """constructor settings: ignore extra kwargs provided"""

        extra = Extra.ignore
