import pytest

import app

passed_tests = []


def pytest_runtest_logreport(report):
    if report.when == "call" and report.passed:
        passed_tests.append(report.nodeid)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if passed_tests:
        terminalreporter.section("Passed tests")
        for test_name in passed_tests:
            terminalreporter.write_line(f"[PASSED] {test_name}")


@pytest.fixture
def client():
    app.app.config.update(TESTING=True)
    return app.app.test_client()


@pytest.fixture
def listing_payload():
    return {
        "item_name": "Test book",
        "item_description": "Test description",
        "item_price": 10,
        "item_type": "Book",
        "seller_id": 2,
        "image_data": "image-bytes",
    }
