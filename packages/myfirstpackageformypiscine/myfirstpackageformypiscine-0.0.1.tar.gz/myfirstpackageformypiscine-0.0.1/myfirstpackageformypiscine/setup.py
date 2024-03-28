from setuptools import setup, find_packages

setup(
    name='myfirstpackageformypiscine',  # Replace with your package name
    version='0.0.1',   # Replace with your package version
    author='theoske',  # Replace with your name
    author_email='theokempf@protonmail.com',  # Replace with your email
    description='just to try',
    url='https://github.com/theoske/python_piscine/Starting/ex09/',  # Replace with your package URL
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3',
)