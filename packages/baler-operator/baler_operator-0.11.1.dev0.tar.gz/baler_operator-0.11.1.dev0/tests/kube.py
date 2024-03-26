from unittest.mock import MagicMock, patch

from baler_operator.kube import core


# Test manage_kubernetes_object function
@patch("baler_operator.kube.core.lookup_kubernetes_object")
@patch("baler_operator.kube.core.exponential_retry")
def test_manage_kubernetes_object_success(
    mock_exponential_retry, mock_lookup_kubernetes_object
):
    mock_lookup_kubernetes_object.return_value = {
        "api_client": MagicMock(),
        "methods": {"create": "create_namespaced_deployment"},
    }
    mock_exponential_retry.return_value = {"status": "Success"}

    response = core.manage_kubernetes_object(
        "create", "Deployment", "default", {"metadata": {"name": "test-deploy"}}
    )

    assert response == {"status": "Success"}
    mock_lookup_kubernetes_object.assert_called_once_with("Deployment")
    mock_exponential_retry.assert_called()


# Test inject_owner_label function
def test_inject_owner_label():
    manifest = {"metadata": {"labels": {"existing-label": "value"}}}
    owner_name = "test-owner"
    updated_manifest = core.inject_owner_label(manifest, owner_name)

    assert "pipelines.baler.gatecastle.com/owned-by" in updated_manifest["metadata"]["labels"]
    assert (
        updated_manifest["metadata"]["labels"]["pipelines.baler.gatecastle.com/owned-by"]
        == owner_name
    )
    assert "existing-label" in updated_manifest["metadata"]["labels"]


# Test operate_on_resource function
@patch("baler_operator.kube.core.render_jinja_template_to_yaml")
@patch("baler_operator.kube.core.manage_kubernetes_object")
def test_operate_on_resource(
    mock_manage_kubernetes_object, mock_render_jinja_template_to_yaml
):
    mock_render_jinja_template_to_yaml.return_value = [
        {"kind": "Deployment", "metadata": {"name": "test-deploy"}}
    ]
    mock_manage_kubernetes_object.return_value = {"status": "Success"}

    core.operate_on_resource(
        "test-owner", "/path/to/manifest.yaml", "create", namespace="default"
    )

    mock_render_jinja_template_to_yaml.assert_called_once_with(
        "/path/to/manifest.yaml", None
    )
    mock_manage_kubernetes_object.assert_called_with(
        "create",
        "Deployment",
        "default",
        {
            "kind": "Deployment",
            "metadata": {
                "name": "test-deploy",
                "labels": {"pipelines.baler.gatecastle.com/owned-by": "test-owner"},
            },
        },
    )
