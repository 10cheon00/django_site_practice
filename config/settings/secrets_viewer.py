import json
import os

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


class SecretsViewer:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.secret_file = os.path.join(self.BASE_DIR, "config/settings/secrets.json")
        with open(self.secret_file) as f:
            self.secrets = json.loads(f.read())

    def get_secret(self, settings):
        try:
            return self.secrets[settings]
        except KeyError:
            error_msg = f"Set the {settings} environment variable."
            raise ImproperlyConfigured(error_msg)
