from setuptools import setup


setup(
    name='docker-tunnel',
    version='0.1.0.dev',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    url='https://github.com/tonyseek/docker-tunnel',
    py_modules=['docker_tunnel'],
    entry_points={
        'console_script': 'docker-tunnel = docker_tunnel:main',
    },
)
