import os
from typing import Literal
from pydantic import model_validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='PAPERMERGE__AUTH__')

    oidc_client_id: str | None = None
    oidc_authorize_url: str | None = None
    oidc_redirect_url: str | None = None
    oidc_logout_url: str | None = None
    oidc_scope: str = 'openid email'

    login_provider: Literal['db', 'ldap'] = 'db'
    remote: bool = False
    remote_logout_endpoint: str | None = None

    @field_validator('login_provider')
    @classmethod
    def db_or_ldap(cls, v: str) -> str:
        if os.environ.get('PAPERMERGE__AUTH__LDAP_URL'):
            return 'ldap'

        return 'db'

    @model_validator(mode='after')
    def check_oidc_params(self):
        three_values = [
            self.oidc_client_id,
            self.oidc_authorize_url,
            self.oidc_redirect_url,
            self.oidc_logout_url
        ]
        count = len([v for v in three_values if v])

        if count not in (0, 4):
            raise ValueError(
                'oidc_client_id, oidc_authorize_url, oidc_redirect_url'
                ' and oidc_logout_url'
                ' should be either all absent or all present'
            )

        return self


def get_settings():
    return Settings()
