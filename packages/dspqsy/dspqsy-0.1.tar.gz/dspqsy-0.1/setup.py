from setuptools import setup, find_packages
 
setup(
    name='dspqsy',
    version='0.1',
    description='A small example package',
    packages=find_packages(),
    url='http://example.com/mypackage',
    license='MIT',
    author='Your Name',
    author_email='your.email@example.com',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)