from setuptools import setup, find_packages

setup(
    name='example_publish_pkg',
    version='0.0.3',
    author='liangsheng',
    author_email='your.email@example.com',
    description='A small example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/example_pkg_your_username',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
