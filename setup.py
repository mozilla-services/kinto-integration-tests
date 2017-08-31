from distutils.core import setup

REQUIREMENTS = [
    'requests==2.11.1',  # Because of pytest-testrail
    'kinto-http',
    'kinto-signer',
    'pytest',
    'pytest-asyncio',
    'pytest-testrail',
    'smwogger',
]


setup(name='fxtesteng',
      url='https://mozilla.org',
      author='Chris Hartjes',
      author_email='chartjes@mozilla.com',
      version='1.0',
      packages=['fxtesteng'],
      install_requires=REQUIREMENTS,
)
