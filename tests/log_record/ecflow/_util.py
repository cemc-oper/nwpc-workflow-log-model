def _check_attrs_value(record, attrs: dict):
    for attr_key, attr_value in attrs.items():
        if attr_value is None:
            assert getattr(record, attr_key) is None
        else:
            assert getattr(record, attr_key) == attr_value
