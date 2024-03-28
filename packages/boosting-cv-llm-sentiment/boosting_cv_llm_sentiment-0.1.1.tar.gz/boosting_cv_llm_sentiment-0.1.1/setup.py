#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'numpy==1.24.3',
    'openai==1.14.3',
    'opencv_python==4.5.5.64',
    'Pillow==10.2.0',
    'pytest==6.2.4',
    'setuptools==58.0.4',
    'transformers==4.34.1',
    'torch',
    'torchvision',
]

test_requirements = ['pytest>=3', ]

setup(
    author="Ricard Santiago Raigada García",
    author_email='ricard.raigada@ieee.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python library enhancing conversational AI with emotion detection, using computer vision and NLP. It tags emotions from facial expressions in real-time and integrates them with a Large Language Model for empathetic responses.",
    entry_points={
        'console_scripts': [
            'boosting_cv_llm_sentiment=boosting_cv_llm_sentiment.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='boosting_cv_llm_sentiment',
    name='boosting_cv_llm_sentiment',
    packages=find_packages(include=['boosting_cv_llm_sentiment', 'boosting_cv_llm_sentiment.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ToroData/boosting_cv_llm_sentiment',
    version='0.1.1',
    zip_safe=False,
)
