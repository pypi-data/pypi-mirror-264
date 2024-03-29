# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/2/27 16:16
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : windmill_client.py
# @Software: PyCharm
"""
from typing import Optional
from baidubce.bce_client_configuration import BceClientConfiguration
from windmillartifactv1.client.artifact_client import ArtifactClient
from windmillcomputev1.client.compute_client import ComputeClient
from windmillendpointv1.client.endpoint_monitor_client import EndpointMonitorClient
from windmillendpointv1.client.endpoint_client import EndpointClient
from windmillmodelv1.client.model_client import ModelClient
from windmilltrainingv1.client.training_client import TrainingClient
from windmillcategoryv1.client.category_client import CategoryClient
from windmillusersettingv1.client.internal_usersetting_client import InternalUsersettingClient


class WindmillClient(ArtifactClient,
                     ModelClient,
                     TrainingClient,
                     ComputeClient,
                     EndpointClient,
                     EndpointMonitorClient,
                     CategoryClient,
                     InternalUsersettingClient):
    """
    A client class for interacting with the windmill service. Initializes with default configuration.

    This client provides an interface to send requests to the BceService.

    Args:
            config (Optional[BceClientConfiguration]): The client configuration to use.
            ak (Optional[str]): Access key for authentication.
            sk (Optional[str]): Secret key for authentication.
            endpoint (Optional[str]): The service endpoint URL.
    """

    def __init__(self, config: Optional[BceClientConfiguration] = None, ak: Optional[str] = "", sk: Optional[str] = "",
                 endpoint: Optional[str] = ""):
        """
        Initialize the WindmillClient with the provided configuration.
        """
        super(WindmillClient, self).__init__(config=config, ak=ak, sk=sk, endpoint=endpoint)
