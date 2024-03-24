from setuptools import setup, find_packages

install_requires = [
    "click>=8.1.7",
    "colorama>=0.4.6"
]

extras_require = {
    'dev': ['pylint>=3.1.0', 'click>=8.1.7', 'twine>=5.0.0'],
}

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name="dailytasks",
    version="2.1.2",
    description="A tasks manager for those who like work from shell.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="LuisanaMTDev",
    author_email="luisanamartineztorres25@gmail.com",
    url='https://github.com/LuisanaMTDev/dailytasks',
    license="Apache-2.0",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ],
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    package_data={'data_files': ['*.json']},
    python_requires=">=3.11",
    entry_points={
        'console_scripts': [
            'dailytasks = daily_tasks.commands.main:daily_tasks',
        ],
    },
)
