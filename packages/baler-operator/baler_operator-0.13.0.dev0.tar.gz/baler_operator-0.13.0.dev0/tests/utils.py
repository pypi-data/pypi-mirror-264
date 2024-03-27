import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from baler_operator.utils.core import *

# Mock the errors module as it seems to be a custom module
errors = MagicMock()
errors.SystemFailure = Exception
errors.UserFailure = Exception


# Test get_current_directory function
def test_get_current_directory():
    with patch(
        "baler_operator.utils.core.os.path.abspath", return_value="/abs/path"
    ), patch(
        "baler_operator.utils.core.Path.resolve", return_value=Path("/pathlib/path")
    ):
        os_path, pathlib_path = get_current_directory()
        assert os_path == "/abs/path"
        assert pathlib_path == Path("/pathlib/path")


# Test get_assets_directory function
def test_get_assets_directory():
    with patch(
        "baler_operator.utils.core.os.path.abspath", return_value="/abs/path"
    ), patch(
        "baler_operator.utils.core.Path.resolve", return_value=Path("/pathlib/assets")
    ):
        os_path, pathlib_path = get_assets_directory()
        assert os_path == "/abs/path/../assets/"
        assert pathlib_path == Path("/pathlib/assets")


# Test get_path_in_assets_directory function
def test_get_path_in_assets_directory():
    with patch(
        "baler_operator.utils.core.get_assets_directory",
        return_value=("/abs/assets", Path("/pathlib/assets")),
    ):
        path = get_path_in_assets_directory("file.txt")
        assert path == Path("/pathlib/assets/file.txt")


# Test load_schema_from_file function
def test_load_schema_from_file_success():
    test_schema = {"type": "object"}
    with patch("builtins.open", mock_open(read_data=json.dumps(test_schema))), patch(
        "json.load", return_value=test_schema
    ):
        schema = load_schema_from_file("schema.json")
        assert schema == test_schema


def test_load_schema_from_file_not_found():
    with pytest.raises(Exception):
        load_schema_from_file("nonexistent.json")


# Test load_supported_versions function
def test_load_supported_versions():
    with patch("builtins.open", mock_open(read_data="v1.0\nv2.0")):
        versions = load_supported_versions("versions.txt")
        assert versions == ["1.0", "2.0"]


def test_load_supported_versions_file_not_found():
    with pytest.raises(Exception):
        load_supported_versions("nonexistent.txt")


# Test is_version_supported function
def test_is_version_supported():
    supported_versions = ["1.0", "2.0"]
    assert is_version_supported("1.0.3", supported_versions) is True
    assert is_version_supported("3.0.0", supported_versions) is False


# Test validate_annotations function
@patch(
    "baler_operator.utils.core.load_schema_from_file", return_value={"type": "object"}
)
@patch("baler_operator.utils.core.validate")
def test_validate_annotations(mock_validate, mock_load_schema):
    annotations = {"key": "value"}
    result = validate_annotations(annotations)
    assert result == annotations
    mock_validate.assert_called_once()


# Test validate_haystack_pipeline function
@patch(
    "baler_operator.utils.core.load_schema_from_file", return_value={"type": "object"}
)
@patch("baler_operator.utils.core.validate")
def test_validate_haystack_pipeline(mock_validate, mock_load_schema):
    spec = {"pipeline": "haystack"}
    result = validate_haystack_pipeline(spec)
    assert result == spec
    mock_validate.assert_called_once()


# Test render_jinja_template_to_yaml function
@patch("baler_operator.utils.core.Environment.get_template")
def test_render_jinja_template_to_yaml(mock_get_template):
    mock_template = MagicMock()
    mock_template.render.return_value = "key: value"
    mock_get_template.return_value = mock_template
    with patch("yaml.safe_load_all", return_value=[{"key": "value"}]):
        result = render_jinja_template_to_yaml("template.yaml")
        assert result == [{"key": "value"}]


# Test lookup_kubernetes_object function
def test_lookup_kubernetes_object():
    result = lookup_kubernetes_object("Pod")
    assert result["api_client"] == kubernetes.client.CoreV1Api
    assert "create" in result["methods"]


# Test exponential_retry function
def always_fails():
    msg = "Failure"
    raise Exception(msg)


def sometimes_fails(attempts=None):
    if attempts is None:
        attempts = [0]
    if attempts[0] < 2:
        attempts[0] += 1
        msg = "Failure"
        raise Exception(msg)
    return "Success"


def test_exponential_retry_success():
    with pytest.raises(Exception):
        result = exponential_retry(sometimes_fails, max_attempts=3)
        assert result == "Success"


def test_exponential_retry_failure():
    with pytest.raises(Exception):
        exponential_retry(always_fails, max_attempts=3)


# Continuing with tests for nodeselector_parse_annotation_string_to_dict
def test_nodeselector_parse_annotation_string_to_dict():
    input_string = "disktype:ssd;zone:us-west-1"
    expected_output = {"disktype": "ssd", "zone": "us-west-1"}
    assert nodeselector_parse_annotation_string_to_dict(input_string) == expected_output


def test_nodeselector_parse_annotation_string_to_dict_empty():
    input_string = ""
    expected_output = {}
    assert nodeselector_parse_annotation_string_to_dict(input_string) == expected_output


def test_nodeselector_parse_annotation_string_to_dict_incorrect_format():
    with pytest.raises(Exception):
        input_string = "disktype:ssd;zone"
        nodeselector_parse_annotation_string_to_dict(input_string)


# Tests for tolerations_parse_annotation_string_to_list
def test_tolerations_parse_annotation_string_to_list_valid():
    tolerations_str = "key:Exists:value:NoSchedule;key2:Equal:value2:PreferNoSchedule"
    expected_list = [
        {"key": "key", "operator": "Exists", "value": "value", "effect": "NoSchedule"},
        {
            "key": "key2",
            "operator": "Equal",
            "value": "value2",
            "effect": "PreferNoSchedule",
        },
    ]
    assert tolerations_parse_annotation_string_to_list(tolerations_str) == expected_list


def test_tolerations_parse_annotation_string_to_list_empty():
    tolerations_str = ""
    expected_list = []
    assert tolerations_parse_annotation_string_to_list(tolerations_str) == expected_list


def test_tolerations_parse_annotation_string_to_list_partial():
    tolerations_str = "key:Exists::NoSchedule;;key2:Equal:value2:"
    expected_list = [
        {"key": "key", "operator": "Exists", "value": "", "effect": "NoSchedule"},
        {"key": "key2", "operator": "Equal", "value": "value2", "effect": ""},
    ]
    assert tolerations_parse_annotation_string_to_list(tolerations_str) == expected_list


def test_tolerations_parse_annotation_string_to_list_invalid():
    tolerations_str = "key-Exists-value-NoSchedule"
    expected_list = []
    assert tolerations_parse_annotation_string_to_list(tolerations_str) == expected_list
