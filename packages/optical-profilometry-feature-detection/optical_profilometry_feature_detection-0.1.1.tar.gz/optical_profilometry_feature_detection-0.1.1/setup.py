from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='optical_profilometry_feature_detection',
      version='0.1.1',
      description='A suite of feature detection tools for optical profilometry data',
      long_description_content_type= "text/markdown",
      long_description=long_description,
      url='https://engineering.case.edu/centers/sdle/',
      author='Kai Zheng, Priyan Rajamohan, Addison Klinke, Bereket Tadesse, Mirra Rasmussen, Mahamad Salah Mahmoud, Laura Bruckman',
      author_email='zheng@case.edu, priyan@case.edu, agk38@case.edu, bereket.tadesse@case.edu, mirra.rasmussen@case.edu, mohamed.mahmoud2@case.edu, laura.bruckman@case.edu',
      packages=['optical_profilometry_feature_detection'],
      install_requires = ['numpy','scipy', 'statsmodels', 'pandas' ],
      zip_safe=False,
      project_urls = {'Documentation': 'https://cwrusdle.bitbucket.io/sphinx/docs/build/html/index.html'},

      # BSD 3-Clause License:
      # - http://choosealicense.com/licenses/bsd-3-clause
      # - http://opensource.org/licenses/BSD-3-Clause
      license='BSD License (BSD-3)',
      )