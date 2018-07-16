from distutils.core import setup

setup(
    name='amrdb',
    version='0.1dev',
    packages=['amrdb',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    url='http://github.com/amrdb',
    author='Chao Chen',
    author_email='none@none.com', requires=['click', 'sqlalchemy']
)
