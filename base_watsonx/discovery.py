import os
import re
import pandas as pd
import numpy as np
import time
import pprint
import json 
from datetime import datetime, timedelta

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from base_watsonx.config import WD_API_KEY, WD_BASE_URL, WD_PROJECT_ID


class WDProcessor():
    def __init__(self):
        self._api_key = WD_API_KEY
        self._base_url = WD_BASE_URL
        self._project_id = WD_PROJECT_ID
        self._discovery_instance = self.authenticate()

    def authenticate(self):
        authenticator = IAMAuthenticator(self._api_key)
        discovery = DiscoveryV2(
            version='2023-03-31',
            authenticator=authenticator
        )

        discovery.set_service_url(self._base_url)

        return discovery

    def query_docs(self, query):
        # recent_date = datetime.now() - timedelta(days=1)
        # date_str = recent_date.strftime('%Y-%m-%dT%H:%M:%SZ')

        result = self._discovery_instance.query( 
                        project_id = self._project_id,
                        # collection_ids = ['123456-789-abcd-0000-1234567890'],
                        count = 1000,
                        query=f'{query}', 
                        ).get_result() # Replaced (metadata.ingest_datetime:{date_str[:10]}) with {query}
        
        return result

        # print("Articles: ", len(result.get("results")), "\nDatetime: ", date_str[:])
    
