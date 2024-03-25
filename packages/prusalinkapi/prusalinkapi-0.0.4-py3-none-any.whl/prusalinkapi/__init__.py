"""Prusa Link API"""

from io import BytesIO
import requests
from requests.auth import HTTPDigestAuth
from PIL import Image

class AuthError(Exception):
    """API Digest Authentication Error"""

class PrusaLink:
    """Class for a PrusaLink printer"""

    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.auth = HTTPDigestAuth(username=username, password=password)

    def __get_status(self):
        try:
            url = f'http://{self.host}/api/v1/status'
            response = requests.get(url, auth=self.auth, timeout=10)
        except requests.exceptions.Timeout as exc:
            raise TimeoutError from exc

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            raise AuthError

    def __get_job(self):
        if self.printer_state != "PRINTING":
            return None

        try:
            url = f'http://{self.host}/api/v1/job'
            response = requests.get(url, auth=self.auth, timeout=10)
        except requests.exceptions.Timeout as exc:
            raise TimeoutError from exc

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            raise AuthError

    def __get_preview(self):
        if self.printer_state != "PRINTING":
            return None

        try:
            path = self.__get_job()['file']['refs']['thumbnail']
            url = f'http://{self.host}{path}'
            response = requests.get(url, auth=self.auth, timeout=10)
        except requests.exceptions.Timeout as exc:
            raise TimeoutError from exc

        if response.status_code == 200:
            preview_str = response.content
            return Image.open(BytesIO(preview_str))
        if response.status_code == 401:
            raise AuthError

    @property
    def printer_state(self):
        """Printer State"""
        return self.__get_status()['printer']['state']

    @property
    def target_bed(self):
        """Heatbed target temperature"""
        return self.__get_status()['printer']['target_bed']

    @property
    def temp_bed(self):
        """Heatbed actual temperature"""
        return self.__get_status()['printer']['temp_bed']

    @property
    def target_nozzle(self):
        """Nozzle target temperature"""
        return self.__get_status()['printer']['target_nozzle']

    @property
    def temp_nozzle(self):
        """Nozzle actual temperature"""
        return self.__get_status()['printer']['temp_nozzle']

    @property
    def fan_hotend(self):
        """Hotend fan RPM"""
        return self.__get_status()['printer']['fan_hotend']

    @property
    def fan_print(self):
        """Print fan RPM"""
        return self.__get_status()['printer']['fan_print']

    @property
    def flow(self):
        """Extruder flow"""
        return self.__get_status()['printer']['flow']

    @property
    def axis_z(self):
        """Z Height"""
        return self.__get_status()['printer']['axis_z']

    @property
    def speed(self):
        """Print Speed"""
        return self.__get_status()['printer']['speed']

    @property
    def filename(self):
        """Print filename"""
        job = self.__get_job()
        if job is not None:
            return job['file']['name']
        return "Not Printing"

    @property
    def progress(self):
        """Print progress"""
        job = self.__get_job()
        if job is not None:
            return job['progress']
        return "Not Printing"

    @property
    def time_printing(self):
        """Time since start of print"""
        job = self.__get_job()
        if job is not None:
            return job['time_printing']
        return "Not Printing"

    @property
    def time_remaining(self):
        """Time until end of print"""
        job = self.__get_job()
        if job is not None:
            return job['time_remaining']
        return "Not Printing"

    @property
    def material(self):
        """Loaded Material"""
        job = self.__get_job()
        if job is not None:
            return job['file']['meta']['filament_type per tool'][0]
        return "Not Printing"

    @property
    def preview(self):
        """Preview of current print"""
        preview = self.__get_preview()
        if preview is not None:
            return preview
        return "Not Printing"
