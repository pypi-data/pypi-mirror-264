import pytest
from nebula._internal.compatibility.deprecated import NebulaDeprecationWarning

from nebula_gcp.aiplatform import VertexAICustomTrainingJob
from nebula_gcp.cloud_run import CloudRunJob


@pytest.mark.parametrize(
    "InfraBlock, kwargs, expected_message",
    [
        (
            CloudRunJob,
            {"image": "foo", "region": "us-central1"},
            "nebula_gcp.cloud_run.CloudRunJob has been deprecated."
            " It will not be available after Sep 2024."
            " Use the Cloud Run or Cloud Run v2 worker instead."
            " Refer to the upgrade guide for more information",
        ),
        (
            VertexAICustomTrainingJob,
            {"image": "foo", "region": "us-central1"},
            "nebula_gcp.aiplatform.VertexAICustomTrainingJob has been deprecated."
            " It will not be available after Sep 2024."
            " Use the Vertex AI worker instead."
            " Refer to the upgrade guide for more information",
        ),
    ],
)
def test_infra_blocks_emit_a_deprecation_warning(
    InfraBlock, kwargs, expected_message, gcp_credentials
):
    with pytest.warns(NebulaDeprecationWarning, match=expected_message):
        if InfraBlock == CloudRunJob:
            InfraBlock(**kwargs, credentials=gcp_credentials)
        else:
            InfraBlock(**kwargs, gcp_credentials=gcp_credentials)
