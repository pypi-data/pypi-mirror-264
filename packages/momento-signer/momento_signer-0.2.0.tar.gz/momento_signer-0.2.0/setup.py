# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['momento_signer']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==3.4.8', 'pyjwt==2.4.0']

setup_kwargs = {
    'name': 'momento-signer',
    'version': '0.2.0',
    'description': 'Signed URL SDK for Momento',
    'long_description': '# Momento client-sdk-python-signer\n\n:warning: Experimental SDK :warning:\n\nPython SDK for Momento is experimental and under active development.\nThere could be non-backward compatible changes or removal in the future.\nPlease be aware that you may need to update your source code with the current version of the SDK when its version gets upgraded.\n\n---\n\n<br/>\n\nPython SDK for Momento, a serverless cache that automatically scales without any of the operational overhead required by traditional caching solutions.\n\n<br/>\n\n## Getting Started :running:\n\n### Requirements\n\n- [Python 3.7](https://www.python.org/downloads/) or above is required\n- A Momento Auth Token is required, you can generate one using the [Momento CLI](https://github.com/momentohq/momento-cli)\n\n<br/>\n\n### Installing Momento and Running the Example\n\nCheck out our [Python SDK example](/examples/)!\n\n<br/>\n\n### Using Momento\n\n```python\nimport os\nfrom momento import simple_cache_client as scc\n\n# Initializing Momento\n_MOMENTO_AUTH_TOKEN = os.getenv(\'MOMENTO_AUTH_TOKEN\')\n_ITEM_DEFAULT_TTL_SECONDS = 60\nwith scc.SimpleCacheClient(_MOMENTO_AUTH_TOKEN, _ITEM_DEFAULT_TTL_SECONDS) as cache_client:\n    # Creating a cache named "cache"\n    _CACHE_NAME = \'cache\'\n    cache_client.create_cache(_CACHE_NAME)\n\n    # Sets key with default TTL and get value with that key\n    _KEY = \'MyKey\'\n    _VALUE = \'MyValue\'\n    cache_client.set(_CACHE_NAME, _KEY, _VALUE)\n    get_resp = cache_client.get(_CACHE_NAME, _KEY)\n    print(f\'Looked up Value: {str(get_resp.value())}\')\n\n    # Sets key with TTL of 5 seconds\n    cache_client.set(_CACHE_NAME, _KEY, _VALUE, 5)\n\n    # Permanently deletes cache\n    cache_client.delete_cache(_CACHE_NAME)\n```\n\n<br/>\n',
    'author': 'Momento',
    'author_email': 'hello@momentohq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gomomento.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
