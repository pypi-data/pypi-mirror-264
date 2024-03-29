import os.path

from setuptools import setup, find_packages

root = os.path.dirname(__file__)
with open(os.path.join(root, "requirements.txt")) as f:
    requirements = f.read().split("\n")

setup(
    name='build_vocabulary',
    version='0.1.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
    ],
    packages=["build_vocabulary"],
    url='https://gitee.com/gfanqi/build_vocabulary',
    license='MIT License',
    author='gfanqi',
    author_email='gfanqi@qq.com',
    description='This program is capable of splitting English text into individual words'
                ' and can focus on learning unfamiliar words through its filtering feature..',
    entry_points={
        'console_scripts': [
            'build_vocabulary = build_vocabulary.main:main',
        ],
    },
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    package_data={
        "build_vocabulary": ['./.assert/60000.txt'],
    },
    install_requires=requirements
)

import nltk

nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
