from setuptools import setup, find_packages

setup(
    name='parse-sse',
    version='0.0.0.1',
    license='MIT',
    author='Gavin Bao',
    author_email='xingce.bao@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='Logic for parse SSE event',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
