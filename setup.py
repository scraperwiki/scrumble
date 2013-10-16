from setuptools import setup, find_packages

long_desc = """TODO"""


setup(
    name='scrumble',
    version='1.0.1',
    description="Get clean numbers, dates etc. from text",
    long_description=long_desc,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='',
    author='ScraperWiki',
    author_email='feedback@scraperwiki.com',
    url='http://scraperwiki.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'python-dateutil>=1.5.0,<2.0.0',
    ],
    extras_require={},
    tests_require=[],
    entry_points="",
)

