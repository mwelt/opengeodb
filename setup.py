from distutils.core import setup

setup(name='opengeodb',
      version='0.1',
      description='interface in python to OpenGeoDB',
      author='Michael Welt',
      author_email='',
      url='https://github.com/mwelt/opengeodb/',
      packages=['opengeodb'], requires=['pymysql']
      )