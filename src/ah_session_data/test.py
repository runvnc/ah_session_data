import pytest
from .session_data import (
    update_session_data,
    delete_session_data,
    add_to_session_list,
    delete_from_session_list
)

def test_update_session_data_basic():
    initial = {"a": 1, "b": {"c": 2}}
    updates = {"b": {"d": 3}}
    result = update_session_data(updates, initial)
    assert result == {"a": 1, "b": {"c": 2, "d": 3}}

def test_update_session_data_empty():
    updates = {"a": 1}
    result = update_session_data(updates)
    assert result == {"a": 1}

def test_update_session_data_nested():
    initial = {"user": {"preferences": {"theme": "light", "font": "arial"}}}
    updates = {"user": {"preferences": {"theme": "dark"}}}
    result = update_session_data(updates, initial)
    assert result["user"]["preferences"]["theme"] == "dark"
    assert result["user"]["preferences"]["font"] == "arial"

def test_update_session_data_list_replacement():
    initial = {"items": [1, 2, 3]}
    updates = {"items": [4, 5]}
    result = update_session_data(updates, initial)
    assert result["items"] == [4, 5]

def test_delete_session_data_basic():
    initial = {"a": 1, "b": {"c": 2, "d": 3}}
    result = delete_session_data(["b", "c"], initial)
    assert "c" not in result["b"]
    assert result["b"]["d"] == 3

def test_delete_session_data_invalid_path():
    initial = {"a": 1}
    with pytest.raises(KeyError):
        delete_session_data(["b", "c"], initial)

def test_delete_session_data_empty_path():
    initial = {"a": 1}
    with pytest.raises(ValueError):
        delete_session_data([], initial)

def test_add_to_session_list_new():
    initial = {}
    result = add_to_session_list(["items"], 1, initial)
    assert result["items"] == [1]

def test_add_to_session_list_existing():
    initial = {"items": [1, 2]}
    result = add_to_session_list(["items"], 3, initial)
    assert result["items"] == [1, 2, 3]

def test_add_to_session_list_nested():
    initial = {"user": {}}
    result = add_to_session_list(["user", "items"], 1, initial)
    assert result["user"]["items"] == [1]

def test_add_to_session_list_invalid_target():
    initial = {"items": 1}
    with pytest.raises(ValueError):
        add_to_session_list(["items"], 2, initial)

def test_delete_from_session_list_basic():
    initial = {"items": [1, 2, 3]}
    result = delete_from_session_list(["items"], 1, initial)
    assert result["items"] == [1, 3]

def test_delete_from_session_list_invalid_index():
    initial = {"items": [1]}
    with pytest.raises(IndexError):
        delete_from_session_list(["items"], 1, initial)

def test_delete_from_session_list_invalid_path():
    initial = {"a": 1}
    with pytest.raises(KeyError):
        delete_from_session_list(["items"], 0, initial)

def test_delete_from_session_list_not_list():
    initial = {"items": 1}
    with pytest.raises(ValueError):
        delete_from_session_list(["items"], 0, initial)
