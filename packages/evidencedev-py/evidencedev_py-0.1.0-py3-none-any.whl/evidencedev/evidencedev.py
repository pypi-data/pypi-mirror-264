import pandas as pd
import requests
from io import BytesIO
from requests.exceptions import JSONDecodeError

__title__ = "evidencedev"
__version__ = "0.1.0"
__author__ = "Frank Boerman"
__license__ = "MIT"


class EvidenceClient:
    def __init__(self, siteurl: str, auth_key: str = None, auth_header: str = 'X-API-Key'):
        self.baseurl = siteurl.strip('/') + '/'

        self.s = requests.Session()
        self.s.headers.update({
            'user-agent': f'evidencedev {__version__}'
        })
        if auth_key is not None:
            self.s.headers.update({
                auth_header: auth_key
            })

        r = self.s.get(self.baseurl + "data/manifest.json")
        r.raise_for_status()
        try:
            manifest = r.json()['renderedFiles']
        except JSONDecodeError:
            raise Exception('Invalid manifest! Please check your authentication')
        self.datasets = {}
        for _, values in manifest.items():
            for value in values:
                self.datasets[value.split('/')[-1].replace('.parquet', '')] = value

    def list_datasets(self) -> list:
        return list(self.datasets.keys())

    def get_dataset(self, dataset: str) -> pd.DataFrame:
        if dataset not in self.datasets:
            raise Exception(f'Dataset {dataset} does not exist!')

        r = self.s.get(self.baseurl + self.datasets[dataset].replace('static/', ''))
        r.raise_for_status()
        stream = BytesIO(r.content)
        df = pd.read_parquet(stream, engine='pyarrow')

        return df