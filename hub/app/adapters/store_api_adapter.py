import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """

        # Send the data batch for saving
        try:
            print('send to ', self.api_base_url)
            endpoint = f"{self.api_base_url}/processed_agent_data"

            request_content = json.dumps([obj.model_dump() for obj in processed_agent_data_batch], default=pydantic_core.to_jsonable_python)
            
            response = requests.post(endpoint, data=request_content)
            if response.status_code == 200:
                logging.info(f"batch saved - {request_content}")
                return True
            else:
                return False

        except Exception as e:
            logging.error(e)
            return False 
