# evidencedev-py

This package is a small utility to download datasets from sites created in [evidence](https://evidence.dev/)

It will read the manifest file, download the parquet files and return a pandas dataframe.

It supports authentication via header api key.

## Example usage
```python

from evidencedev import EvidenceClient
client = EvidenceClient(site_url = 'https://reports.coreflowbased.eu/', 
                        auth_key='<API KEY>',
                        auth_header='X-API-Key') # X-API-Key is the default
available_datasets = client.list_datasets()
df = client.get_dataset('da_baseload_prices')

```