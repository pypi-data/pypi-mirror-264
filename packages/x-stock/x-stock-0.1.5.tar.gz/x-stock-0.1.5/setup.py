from setuptools import setup, find_packages

setup(
    name='x-stock',
    version='0.1.5',
    author='chuck xue',
    author_email='2254379984@qq.com',
    description='个人股票分析工具',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/x-stock",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=open('requirements.txt').read().splitlines(),
)
