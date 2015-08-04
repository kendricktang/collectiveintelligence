try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Clustering package',
    'author': 'Kendrick Tang',
    'url': 'N/A',
    'download_url': 'N/A',
    'author_email': 'kentangsrice@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'feedparser', 're', 'random'],
    'packages': ['algs'],
    'scripts': [],
    'name': 'Clustering'
}

setup(**config)