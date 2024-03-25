import os

from django.conf import settings

config_default = (
    'DJANGO_SETTINGS_MODULE',
    'papamana_django.config.settings'
)


def updateconfig(env: dict = {}, list_env: list = []) -> None:
    """
        Function for update config
        config: path settings
        kwargs: environtment
        Example args for update config:
        {
            "HELLO": "test",
            "KAFKA": "127.0.0.1"
        }
    """

    if env:
        for attr, val in env.items():
            setattr(settings, attr, val)
    if list_env:
        for env in list_env:
            attr = env.get("attribute")
            value = env.get("value")
            os.environ[attr] = value
            setattr(settings, attr, value)
    return 
