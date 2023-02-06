from cerberus import Validator

_SCHEMA = {
    "ftp": {
        "type": "dict",
        "schema": {
            "host": {"type": "string", "default": "127.0.0.1"},
            "port": {
                "type": "integer",
                "coerce": int,
                "min": 1,
                "max": 65535,
                "default": 21,
            },
        },
        "default": {},
    },
    "telegram": {
        "type": "dict",
        "schema": {"token": {"type": "string", "required": True}},
        "required": True,
    },
    "users": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "hashed_password": {"type": "string", "required": True},
                "telegram_id": {"type": "integer", "coerce": int, "required": True},
            },
        },
        "required": True,
    },
}


class ConfigurationError(Exception):
    pass


def build_configuration(raw_config):
    v = Validator(allow_unknown=False)
    if not v.validate(raw_config, _SCHEMA):
        raise ConfigurationError(v.errors)
    else:
        return v.normalized(raw_config, _SCHEMA)
