from setuptools import setup


with open('README.rst') as readme:
    next(readme)  # skip the first line
    long_description = readme.read().strip()


setup(
    name='docker-tunnel',
    version='0.1.0',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    description='Using remote docker with SSH tunnel.',
    long_description=long_description,
    platforms=['Linux', 'Mac'],
    url='https://github.com/tonyseek/docker-tunnel',
    license='MIT',
    py_modules=['docker_tunnel'],
    entry_points={
        'console_script': 'docker-tunnel = docker_tunnel:main',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ]
)
