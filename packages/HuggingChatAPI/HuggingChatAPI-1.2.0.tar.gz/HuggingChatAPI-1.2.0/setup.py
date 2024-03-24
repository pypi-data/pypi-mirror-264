from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='HuggingChatAPI',
  version='1.2.0',
  author='ILYXAAA',
  author_email='ilyagolybnichev@gmail.com',
  description='The project is an unofficial API for the site huggingface.co/chat.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/ILYXAAA/HuggingChatAPI',
  packages=find_packages(),
  install_requires=['googletrans==4.0.0-rc1', 'Pygments', 'requests', 'urllib3'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'Operating System :: OS Independent'
  ],
  keywords='files HuggingChatAPI API AI Bot',
  project_urls={
    'GitHub': 'https://github.com/ILYXAAA/HuggingChatAPI'
  },
  python_requires='>=3.6'
)