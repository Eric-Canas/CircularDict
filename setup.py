from setuptools import setup, find_packages

setup(
    name='circular-dict',
    version='1.0',
    author='Eric-Canas',
    author_email='eric@ericcanas.com',
    url='https://github.com/Eric-Canas/CircularDict',
    description='CircularDict is a high-performance Python data structure that combines the best of dictionaries and circular buffers. '
                'It provides a data structure that acts as a dictionary but operates as a circular buffer, efficiently removing '
                'the oldest item when a predetermined maximum length is exceeded. Ideal for caching large items while minimizing '
                'memory usage, CircularDict provides a unique solution for developers requiring dictionary-like and '
                'circular-queue-like operations in a single, efficient data structure.',
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
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Monitoring',
    ],
)