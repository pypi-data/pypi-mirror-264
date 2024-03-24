from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='DbUnify',
    version='1.0.5',
    author='Sepehr0Day',
    description='DbUnify (Database Management) is a versatile Python library that simplifies database connectivity and management using SQLite.',
    long_description=long_description,
    author_email='sphrz2324@gmail.com', 
    url="https://github.com/Sepehr0Day/DbUnify",
    long_description_content_type='text/markdown',
    packages=['DbUnify'],
    install_requires=[
        'matplotlib',
        'aiosqlite'
    ],
    python_requires='>=3.8',
    classifiers=[ 
        'Development Status :: 5 - Production/Stable', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    keywords='DbUnify database sqlite3 sql SQL sepehr0day Management',
    project_urls={ 
        'Documentation' : 'https://Sepehr0day.github.io/DbUnify.html',
        'Source': 'https://github.com/Sepehr0Day/DbUnify',
        'Bug Reports': 'https://github.com/Sepehr0Day/DbUnify/issues'
    },
    license='MIT'
)