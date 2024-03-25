from setuptools import setup

setup(
    author='Alex',
    author_email='madest92@mail.com',
    name='teaxyzzz6',
    version='1.0.66',
    description='A simple package for https://app.tea.xyz/. Example teaxyzzz6',
    url='https://github.com/madest92/teaxyzzz6',
    project_urls={
        'Homepage': 'https://github.com/madest92/teaxyzzz6',
        'Source': 'https://github.com/madest92/teaxyzzz6',
        },
    py_modules=['hello_teaxyzzz6'],
    entry_points={
        'console_scripts': [
            'hello-tea=hello_tea:hello_tea_func'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.20.0',
        'tea-xyz1',
        'tea-xyz2',
    ],
)
