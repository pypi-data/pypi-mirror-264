from setuptools import setup, find_packages

setup(
    name='gpu_fit_llm',
    version='0.1.0',
    author='Harish Vadaparty',
    author_email='harishvadaparty@gmail.com',
    description='Helps estimate the memory requirements for a model on a GPU.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='http://github.com/Harryalways317/gpu-fit-llm',
    packages=find_packages(exclude=["tests*", "examples*"]),
    install_requires=[
        'torch>=1.8.0',
        'transformers>=4.0.0',
        'accelerate>=0.5.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
