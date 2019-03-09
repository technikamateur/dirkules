from setuptools import setup

setup(
    name='dirkules',
	packages=['dirkules'],
    version='1.0',
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy',
        'Flask-APScheduler',
        'APScheduler',
    ],
)
