from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'A vectorized approach to Genetic Programming - TensorFlow version'

setup(
    name='tensorgp_tf',
    version=VERSION,
    author='Francisco Baeta',
    author_email='<fjrbaeta@dei.uc.pt>',
    description=DESCRIPTION,
    keywords=['Genetic Programming', 'Vectorization', 'GPU', 'Python', 'TensorFlow'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls = {
        "Source": "https://github.com/AwardOfSky/TensorGP/tree/dev",
    },
    install_requires = ['tensorflow==2.16.1', 'scikit-image', 'matplotlib'],
    packages=find_packages(),
    include_package_data=True,
)