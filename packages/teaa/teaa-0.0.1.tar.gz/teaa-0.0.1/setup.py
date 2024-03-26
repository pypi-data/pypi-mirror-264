from setuptools import setup

setup(
    author='CryptoGu1',
    author_email='Kriptoairdrop9@gmail.com',
    name='teaa',
    version='0.0.1',
    description='A simple package for https://app.tea.xyz/. Example tea-xyz1 - https://github.com/madest92/tea-xyz1 and tea-xyz2 - https://github.com/madest92/tea-xyz2',
    url='https://github.com/CryptoGu1/teaa.git',
    project_urls={
        'Homepage': 'https://github.com/CryptoGu1/teaa.git',
        'Source': 'https://github.com/CryptoGu1/teaa.git',
    },
    py_modules=['hi_tea'],
    entry_points={
        'console_scripts': [
            'hi-tea=hi_tea:hello_tea_xyz'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'teaa1',
        'teaa2',
        # add your projects
    ],
)
