class FakeAuthApp:
    def __init__(self):
        self._user_fields_schema = [
            {
                "name": "username",
                "input_type": "text",
                "data_type": "string"
            },
            {
                "name": "email",
                "input_type": "email",
                "data_type": "string"
            },
            {
                "name": "age",
                "input_type": "number",
                "data_type": "integer"
            },
            {
                "name": "is_active",
                "input_type": "checkbox",
                "data_type": "boolean"
            },
            {
                "name": "birthday",
                "input_type": "date",
                "data_type": "datetime"
            }
        ]

    @property
    def user_fields_schema(self):
        return self._user_fields_schema
