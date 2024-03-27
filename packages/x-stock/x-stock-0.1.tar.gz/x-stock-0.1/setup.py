from setuptools import setup, find_packages

setup(
    name='x-stock',
    version='0.1',
    url='http://github.com/yourname/mypackage',
    author='chuck xue',
    author_email='2254379984@qq.com',
    description='个人股票分析工具',
    packages=find_packages(),    
    install_requires=[
      'numpy',
      'pandas',
      'akshare',
      'matplotlib',
      # other dependencies...
    ],
)
