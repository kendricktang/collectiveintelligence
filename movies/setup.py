try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Kendrick Tang',
    'url': 'N/A',
    'download_url': 'N/A',
    'author_email': 'kentangsrice@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['movie_rec'],
    'scripts': [],
    'name': 'movies'
}

setup(**config)