from setuptools import setup

setup(name='scrampy',
      version='0.1',
      description='split, mix, and combine audio',
      url='http://github.com/machow/scrampy',
      author='Michael Chow',
      author_email='chowmichedu@gmail.com',
      packages=['scrampy'],
      entry_points = {
          'console_scripts': ['scrampy=scrampy.scrampy:main']
          },
      install_requires=[
          'pydub',
          'argh >= 0.26.0',
          'PyYAML',
          'pandas >= 0.16.0, < 0.17.0',
          'numpy >= 1.8.0, < 1.9.0',
          ],

      zip_safe=False)
