import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.app_deployment_state import AppDeploymentState  # noqa: E501
from openapi_server.models.dingman_error import DingmanError  # noqa: E501
from openapi_server import util


def get_deployment_states(app_service_name):  # noqa: E501
    """Get Deployment State under an app service

    This operation returns the Deployment state list under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str

    :rtype: Union[AppDeploymentState, Tuple[AppDeploymentState, int], Tuple[AppDeploymentState, int, Dict[str, str]]
    """
    return 'do some magic!'
