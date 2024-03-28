from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='intelliml',
  version='0.1',
  description='An Automated Machine Learning Tool',
  long_description=open('README.txt').read(),
  url='',  
  author='Mujaffar Bhati',
  author_email='mujaffarbhati444@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='automl', 
  packages=find_packages(),
  install_requires=['pandas', 'numpy', 'scikit-learn', 'xgboost', 'lightgbm']
)