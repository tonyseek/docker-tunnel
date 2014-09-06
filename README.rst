|PyPI Version| |PyPI Downloads| |Wheel Status|

docker-tunnel
=============

``docker-tunnel`` is a console utility to use remote docker with SSH tunnel.

If you are using OS X or a Linux distribution with docker-unsupported kernel,
no more running a virtual machine or ssh to a remote shell.


Installation
------------

With pip::

    $ pip install docker-tunnel

With pipsi_ (Recommended)::

    $ pipsi install docker-tunnel


Usage
-----

::

    $ docker-tunnel user@example.com
    (user@example.com) $
    (user@example.com) $ echo $DOCKER_HOST
    127.0.0.1:4243
    (user@example.com) $ docker ps  # go ahead
    ...
    (user@example.com) $ ^D  # ctrl-d
    $

More options::

    $ docker-tunnel --help


Shell Theme Integration
-----------------------

Inside the tunnel injected shell, the environment variable ``DOCKER_HOST`` and ``DOCKER_PROMPT_INFO`` will be assigned. They can be used in your shell theme to prompt you which tunnel is using.

There is an example, `my custom theme`_ for OH-MY-ZSH.


Troubleshooting
---------------

``Error response from daemon: client and server don't have same version (client : 1.14, server: 1.12)``
  The docker in source of CentOS 7 is using API 1.12 but the docker client in Homebrew of OS X is not. You can downgrade the docker client with Homebrew::

      $ brew versions docker
      ...
      1.0.0    git checkout c513c42 /usr/local/Library/Formula/docker.rb
      ...
      $ cd /usr/local/Library/Formula  # now we install the old version of docker
      $ git checkout c513c42 -- docker.rb
      $ brew unlink docker
      $ brew install docker
      $ git checkout HEAD -- docker.rb
      $ cd -
      $ brew info docker  # check the installed versions and current version
      ...
      /usr/local/Cellar/docker/1.1.1 (9 files, 9.8M) *
        Poured from bottle
      /usr/local/Cellar/docker/1.2.0 (9 files, 6.6M)
        Poured from bottle
      ...
      $ docker-tunnel user@example.com
      (user@example.com) $ docker version
      Client version: 1.0.0
      Client API version: 1.12
      ...
      (user@example.com) $ exit
      $ brew switch 1.2.0  # restore to latest


``bind: Address already in use. cannot listen to port: 4243``
  You can find out the process which held the ``4243`` port with ``sudo lsof -i :4243`` and decide to kill it or pick another port with ``--local-port``.


``channel 1: open failed: connect failed: Connection refused. 2014/09/06 13:08:57 Get http://127.0.0.1:4243/v1.14/info: EOF``
  Does the docker server listen on ``127.0.0.1:2375``? You may have to set correct server info with ``--remote-host`` and ``--remote-port``.


Known Bugs
----------

- The ssh tunnel can be authenticated with public key only. The password prompt will caused a crash.


Issues
------

If you want to report bugs or request features, please create issues on
`GitHub Issues <https://github.com/tonyseek/docker-tunnel/issues>`_.


.. _pipsi: https://github.com/mitsuhiko/pipsi
.. _`my custom theme`: https://github.com/tonyseek/oh-my-zsh-seeker-theme

.. |Wheel Status| image:: https://pypip.in/wheel/docker-tunnel/badge.svg
   :target: https://warehouse.python.org/project/docker-tunnel
   :alt: Wheel Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/docker-tunnel.svg
   :target: https://pypi.python.org/pypi/docker-tunnel
   :alt: PyPI Version
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/docker-tunnel.svg
   :target: https://pypi.python.org/pypi/docker-tunnel
   :alt: Downloads
