import sys

from calculator.operators import Operators
from form.fake_auth_app import FakeAuthApp
from form import constants


def run_calculator_demo():
    print("=" * 50)
    calc = Operators()

    result2 = calc.subtract(10, 3)
    print(f"10 - 3 = {result2}")

    print("✅ Calculator demo completed!")


def run_form_demo():
    """執行表單示範"""
    print("=" * 50)
    print("📋 Form Schema Demo")

    app = FakeAuthApp()
    schema = app.user_fields_schema

    print(f"Total fields: {len(schema)}")
    print("\nField definitions:")

    for field in schema:
        print(f"  • {field['name']}: {field['input_type']} → {field['data_type']}")

    form = constants.Form()
    print(f"\nInput type mapping: {form.INPUT_TYPE_TO_DATA_TYPE_MAPPING}")
    print("✅ Form demo completed!")


def main():
    print("🚀 Application Starting...")
    print("This application demonstrates calculator and form modules")

    try:
        run_calculator_demo()

        run_form_demo()

        print("=" * 50)
        print("🎉 All modules executed successfully!")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

