from setuptools import setup

setup(name='scrampy',
      version='0.1',
      description='split, mix, and combine audio',
      url='http://github.com/machow/scrampy',
      author='Michael Chow',
      author_email='machow@princeton.edu',
      packages=['scrampy'],
      entry_points = {
          'console_scripts': ['scrampy=scrampy.scrampy:main']
          },
      install_requires=[
          'pydub',
          'argh',
          'PyYAML',
          'pandas',
          'numpy',
          ],

      zip_safe=False)
