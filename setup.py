from setuptools import setup, find_packages

setup(
    name='circular-dict',
    version='1.9',
    author='Eric-Canas',
    author_email='eric@ericcanas.com',
    url='https://github.com/Eric-Canas/CircularDict',
    description='CircularDict is a high-performance Python data structure that blends the functionality of dictionaries and circular buffers. '
                'Inheriting the usage of traditional dictionaries, it allows you to define constraints on size and memory usage. '
                'This way, the CircularDict will be always up-to-date with the last N added elements, ensuring that neither the maximum length nor '
                'the memory usage limit is exceeded. It is ideal for caching large data structures while maintaining control over memory footprint. ',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Debuggers',
    ],
)