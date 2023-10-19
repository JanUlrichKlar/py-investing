import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='finanzenpy_org', # Replace with your own username
    version='0.0.1',
    author='Jan-Ulrich Klar',
    author_email='jan.klar@gmx.net',
    description='API to fetch historical stock data and fundamentals from finanzen.net',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JanUlrichKlar/finanzenpy',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'finanzenpy_org': ['data/*.csv']},
    install_requires=['requests', 'bs4', 'lxml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
	'Intended Audience :: Financial and Insurance Industry',
	'Intended Audience :: Science/Research',
	'Topic :: Office/Business :: Financial',
	'Topic :: Office/Business :: Financial :: Investment'
	
    ],
    python_requires='>=3.6',
)
