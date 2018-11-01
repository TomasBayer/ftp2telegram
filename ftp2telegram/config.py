from cerberus import Validator


def _build_schema():
    string = dict(type='string')
    integer = dict(type='integer', coerce=int)

    port = dict(integer, min=1, max=65535)

    sub_dict = lambda **d: dict(type='dict', schema=d)
    sub_list = lambda d: dict(type='list', schema=d)
    required = lambda schema: dict(schema, required=True)
    with_default = lambda schema, default: dict(schema, default=default)

    return dict(
        ftp=with_default(sub_dict(
            host=with_default(string, "127.0.0.1"),
            port=with_default(port, "21")
        ), {}),
        telegram=required(sub_dict(
            token=required(string)
        )),
        users=required(sub_list(sub_dict(
            name=required(string),
            telegram_id=required(integer),
            password=required(string),
            salt=required(string)
        )))
    )


_SCHEMA = _build_schema()


class ConfigurationError(Exception):
    pass


def build_configuration(raw_config):
    v = Validator(allow_unknown=False)
    if not v.validate(raw_config, _SCHEMA):
        raise ConfigurationError(v.errors)
    else:
        return v.normalized(raw_config, _SCHEMA)
