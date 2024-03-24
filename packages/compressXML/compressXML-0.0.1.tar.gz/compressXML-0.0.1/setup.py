# coding:utf-8

#from setuptools import setup
from setuptools import setup, Extension
# or
#from distutils.core import setup  

with open('README.md',encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='compressXML',   
        version='0.0.1',   
        description='compressXML',#long_description=foruser,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/compressXML',      
        packages=['compressXML'],   
        include_package_data=True,
        keywords = ['compress', 'XML'],   # Keywords that define your package best
          install_requires=[ 
          'pyperclip'          
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',
      ]
)
