err-ansible
============

Err plugin to run Ansible playbooks/commands asynchronously

Prerequisites
------------

Plugin uses [RQ](http://python-rq.org/) library for jobs/queues management (this
way the whole bot is not waiting for a particular long-running playbook to
finish), which requires [Redis](http://redis.io/) running on the same machine
where your bot runs.

Plugin will still work without Redis installed, but this way you will lose
asynchronous capabilities, so having Redis is still highly recommended for
production use.

Installation
------------

Configuration
-------------

Usage
-----

Licence
-------

GNU GPLv3. See `LICENSE` file for details.
