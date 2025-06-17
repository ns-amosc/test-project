import form.constants as constant


def test_fields_schema_contains_data_type_tag(fake_auth_app):
    form = constant.Form

    result = fake_auth_app.user_fields_schema
    for f in result:
        assert (
                f["data_type"]
                == form.INPUT_TYPE_TO_DATA_TYPE_MAPPING[f["input_type"]]
        )
