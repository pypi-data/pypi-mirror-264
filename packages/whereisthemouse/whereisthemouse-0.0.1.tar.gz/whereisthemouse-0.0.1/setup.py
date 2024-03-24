# coding:utf-8

#from setuptools import setup
from setuptools import setup, Extension
# or
#from distutils.core import setup  

with open('README.md',encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='whereisthemouse',   
        version='0.0.1',   
        description='show mouse position and pixel value on desktop, press alt to copy',#long_description=foruser,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/whereisthemouse',      
        packages=['whereisthemouse'],   
        include_package_data=True,
        keywords = ['mouse', 'position'],   # Keywords that define your package best
          install_requires=[            
          'keyboard',
          'pyautogui',
          'pyperclip'          
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',
      ]
)
