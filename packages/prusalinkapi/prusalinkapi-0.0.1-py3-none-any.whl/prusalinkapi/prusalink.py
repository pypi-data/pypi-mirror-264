from requests.auth import HTTPDigestAuth
import requests
from PIL import Image
from io import BytesIO

class PrusaLink:
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password
    
    def __get_status(self):
        try:
            url = f'http://{self.host}/api/v1/status'
            response = requests.get(url, auth=HTTPDigestAuth(username=self.username, password=self.password), timeout=10)
        except requests.exceptions.Timeout:
            raise TimeoutError

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("Unauthorized")
        else:
            raise Exception(f"Request Failed: {response.status_code}")
    
    def __get_job(self):
        if self.printer_state != "PRINTING":
            return None
        
        try:
            url = f'http://{self.host}/api/v1/job'
            response = requests.get(url, auth=HTTPDigestAuth(username=self.username, password=self.password), timeout=10)
        except requests.exceptions.Timeout:
            raise TimeoutError
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("Unauthorized")
        else:
            raise Exception(f"Request Failed: {response.status_code}")
    
    def __get_preview(self):
        if self.printer_state != "PRINTING":
            return None
        
        try:
            path = self.__get_job()['file']['refs']['thumbnail']
            url = f'http://{self.host}{path}'
            response = requests.get(url, auth=HTTPDigestAuth(username=self.username, password=self.password))
        except requests.exceptions.Timeout:
            raise TimeoutError
        
        if response.status_code == 200:
            preview_str = response.content
            return Image.open(BytesIO(preview_str))
        elif response.status_code == 401:
            raise Exception("Unauthorized")
        else:
            raise Exception(f"Request Failed: {response.status_code}")
    
    @property
    def printer_state(self):
        return self.__get_status()['printer']['state']
    
    @property
    def target_bed(self):
        return self.__get_status()['printer']['target_bed']
    
    @property
    def temp_bed(self):
        return self.__get_status()['printer']['temp_bed']
    
    @property
    def target_nozzle(self):
        return self.__get_status()['printer']['target_nozzle']
    
    @property
    def temp_nozzle(self):
        return self.__get_status()['printer']['temp_nozzle']
    
    @property
    def fan_hotend(self):
        return self.__get_status()['printer']['fan_hotend']
    
    @property
    def fan_print(self):
        return self.__get_status()['printer']['fan_print']
    
    @property
    def flow(self):
        return self.__get_status()['printer']['flow']

    @property
    def axis_z(self):
        return self.__get_status()['printer']['axis_z']
    
    @property
    def speed(self):
        return self.__get_status()['printer']['speed']
    
    @property
    def filename(self):
        job = self.__get_job()
        if job is not None:
            return job['file']['name']
        return "Not Printing"
    
    @property
    def progress(self):
        job = self.__get_job()
        if job is not None:
            return job['progress']
        return "Not Printing"
    
    @property
    def time_printing(self):
        job = self.__get_job()
        if job is not None:
            return job['time_printing']
        return "Not Printing"
    
    @property
    def time_remaining(self):
        job = self.__get_job()
        if job is not None:
            return job['time_remaining']
        return "Not Printing"
    
    @property
    def material(self):
        job = self.__get_job()
        if job is not None:
            return job['file']['meta']['filament_type per tool'][0]
        return "Not Printing"
    
    @property
    def preview(self):
        preview = self.__get_preview()
        if preview is not None:
            return preview
        return "Not Printing"