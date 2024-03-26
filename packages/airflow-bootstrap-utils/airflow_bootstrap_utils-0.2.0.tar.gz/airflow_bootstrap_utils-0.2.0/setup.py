#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "jinja2",
    "Rich",
    "PyYAML",
    "simple-template-toolkit",
]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python tools to generate Airflow DAGs from control and configuration files.",
    entry_points={
        'console_scripts': [
            'generate-airflow-dag-script=airflow_bootstrap_utils.generate_dag:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='airflow_bootstrap_utils',
    name='airflow_bootstrap_utils',
    packages=find_packages(include=['airflow_bootstrap_utils', 'airflow_bootstrap_utils.*']),
    package_data={
        "airflow_bootstrap_utils": [
            "conf/config.yaml",
            "templates/dag_template.py",
            "templates/task_template.py",
            "template/manager.py",
        ]
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/airflow_bootstrap_utils',
    version='0.2.0',
    zip_safe=False,
)
