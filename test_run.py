from testdata import generatetestdata as gd
from testdata import test_ai


def test_generate_data():
    gd.create_test_user()
    gd.create_test_category()
    gd.create_test_screenshot()


def test_ai_module():
    test_ai.test_ai_module()