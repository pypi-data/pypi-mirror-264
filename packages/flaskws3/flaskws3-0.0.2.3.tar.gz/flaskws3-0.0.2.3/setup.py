#-*- coding: utf-8 -*-

from distutils.core import setup


packages = (
    'flaskws',
    )

setup(name='flaskws3', 
      version='0.0.2.3', 
      packages=packages, 
      install_requires=['tornado'], 
      description='Websocket for flask.',
      author='smallfz', 
      author_email='small.fz@gmail.com')


