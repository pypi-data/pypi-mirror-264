import pytest

from nrdtech_utils.deprecated import deprecated


# Test deprecated class without additional message
@deprecated
class OldClass:
    def __init__(self):
        pass


def test_deprecated_class_without_message():
    with pytest.warns(DeprecationWarning) as record:
        OldClass()

    assert len(record) == 1
    assert "OldClass is deprecated" in str(record[0].message)


# Test deprecated class with additional message
@deprecated(additional_message="Use NewClass instead.")
class NewOldClass:
    def __init__(self):
        pass


def test_deprecated_class_with_message():
    with pytest.warns(DeprecationWarning) as record:
        NewOldClass()

    assert len(record) == 1
    assert "NewOldClass is deprecated. Use NewClass instead." in str(record[0].message)


# Test deprecated function without additional message
@deprecated
def old_function():
    pass


def test_deprecated_function_without_message():
    with pytest.warns(DeprecationWarning) as record:
        old_function()

    assert len(record) == 1
    assert "old_function is deprecated" in str(record[0].message)


# Test deprecated function with additional message
@deprecated(additional_message="Use new_function() instead.")
def new_old_function():
    pass


def test_deprecated_function_with_message():
    with pytest.warns(DeprecationWarning) as record:
        new_old_function()

    assert len(record) == 1
    assert "new_old_function is deprecated. Use new_function() instead." in str(
        record[0].message
    )
