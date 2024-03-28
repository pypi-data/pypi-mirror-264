from setuptools import setup, find_packages
try:
    from sqprefect.package._package import __name__, __version__
except:
    __name__ = 'sqprefect'
    __version__ = '2.5.12'

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    long_description_content_type='text/plain',
    url='https://upload.pypi.org/legacy/',
    home_page='https://upload.pypi.org/legacy/',
    download_url='https://upload.pypi.org/legacy/',
    project_urls={'Documentation':'https://upload.pypi.org/legacy/'},
    author='Bill Johnson',
    author_email='bjohnson@squareup.com',
    install_requires=[
    ],
)
