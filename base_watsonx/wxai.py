import os
import re
import pandas as pd
import numpy as np
import time
import pprint
import json 
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes

from base_watsonx.config import WX_API_KEY, WX_BASE_URL, WX_PROJECT_ID


class WXAIProcessor():
    def __init__(self):
        self._wx_creds = {
		"url" : WX_BASE_URL,
		"apikey" : WX_API_KEY 
        }
        self._project_id = WX_PROJECT_ID

    @staticmethod
    def get_model_names(self):
        return [model.value for model in ModelTypes]

    def get_model(self, model_id, decoding_method="greedy", min_tokens=1, max_tokens=500, repetition_penalty=1):
        parameters = {
            "decoding_method": decoding_method,
            "min_new_tokens": min_tokens,
            "max_new_tokens": max_tokens,
            "repetition_penalty": repetition_penalty
        }
        model =  Model(
            model_id = model_id,
            params = parameters,
            credentials = self._wx_creds,
            project_id = self._project_id
        )
        return model
    
    def generate_text(self, model: Model, prompt_input):
        generated_text = model.generate(prompt=prompt_input)
        return generated_text
    