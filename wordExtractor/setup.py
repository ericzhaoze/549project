from setuptools import setup

setup(
    name='wordextractor',
    version='0.1.0',
    packages=['wordextractor'],
    include_package_data=True,
    install_requires=[
        'Flask==0.12.2',
        'sh==1.12.14',
		'html5validator==0.2.8',
        'pycodestyle==2.3.1',
        'pydocstyle==2.0.0',
        'pylint==1.7.2',
        'arrow==0.10.0',
    ],
)
