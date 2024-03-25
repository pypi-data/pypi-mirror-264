from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='beautider',
  version='0.1.1',
  author='bolgaro4ka',
  author_email='bolgaro4ka.github@gmail.com',
  description='Module for creating progress bars.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/bolgaro4ka',
  packages=find_packages(),
  install_requires=['colorama>=0.4.6'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='progress bar',
  project_urls={
    'GitHub': 'https://github.com/bolgaro4ka'
  },
  python_requires='>=3.8'
)
