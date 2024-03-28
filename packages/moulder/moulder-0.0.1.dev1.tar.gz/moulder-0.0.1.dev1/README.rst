PyTower
=======
Build and deploy Pythonic apps.

Attention
---------
PRE-ALPHA RELEASE.

NOT READY FOR PRODUCTION. ONLY FOR TESTING PURPOSES. YOU MAY LOSE ALL YOUR DATA.

TL;DR
-----

.. code-block:: bash

    $ export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
    $ export DOMAIN_NAME=<enter-your-domain-name>
    $ pytower --deploy


Requires
--------
- python >= 3.8


Dependencies
------------
On Ubuntu 22.04 or Ubuntu 20.04:

.. code-block:: bash

    $ sudo apt install python3-venv docker.io docker-compose


Post-Installation
-----------------

.. code-block:: bash

    $ sudo usermod -aG docker $USER
    $ newgrp docker


Deploy
------

.. code-block:: bash

    $ cd ~
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install --upgrade pip
    (.venv) $ pip install pytower

    (.venv) $ export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
    (.venv) $ export DOMAIN_NAME=<enter-your-domain-name>
    (.venv) $ pytower --deploy


License
-------
Copyright (C) 2022-2023 Salman Mohammadi <salman@pytower.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see https://www.gnu.org/licenses/.
