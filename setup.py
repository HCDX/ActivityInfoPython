from distutils.core import setup

setup(
    name='activityinfo_python',
    version='1.2',
    author='James Cranwell-Ward',
    author_email='jcranwellward@unicef.org',
    py_modules=['activtyinfo_client'],
    install_requires=['requests'],
    description='Simple python wrapper for ActivityInfo REST API'
)

