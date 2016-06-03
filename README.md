err-ansible
============

Err plugin to run Ansible playbooks/commands asynchronously

Prerequisites
-------------

Plugin uses [RQ](http://python-rq.org/) library for jobs/queues management (this
way the whole bot is not waiting for a particular long-running playbook to
finish), which requires [Redis](http://redis.io/) running on the same machine
where your bot runs.

Plugin will still work without Redis installed, but this way you will lose
asynchronous capabilities, so having Redis is still highly recommended for
production use.

Installation
------------

`!repos install https://github.com/br0ziliy/err-ansible.git`

You will also need to run the RQ worker in the directory where Errbot installed
the plugin (`/var/lib/err/plugins/err-ansible` by default:

```
cd /var/lib/err/plugins/err-ansible
bin/start_worker.sh
```

Configuration
-------------

Plugin is configured with the command below:

`!plugin config Ansible {'ANSIBLE_SSH_KEY': u'/home/devops_bot/.ssh/id_rsa', 'INVENTORY_DIR': u'/etc/ansible/inventory', 'PLAYBOOK_DIR': u'/etc/ansible/playbooks'}`

- `ANSIBLE_SSH_KEY` - SSH key to use with `ansible-playbook -u root` command
- `INVENTORY_DIR` - directory where inventory files are stored (subdirectories
  are not yet supported)
- `PLAYBOOK_DIR` - directory where playbook files are stored (subdirectories are
  not yet supported)

Usage
-----

To run a playbook:

`!ansible playbook.yml my_awesome_servers`

To list available inventories/playbooks:

`!ansible list`

To query task status:

`!task info [task UUID]`

If you want a nice overview of RQ tasks queue, install
[rq-dashboard](https://github.com/ducu/rq-dashboard) Python
package, and run it:

```
pip install rq-dashboard
rq-dashboard
```

Licence
-------

GNU GPLv3. See `LICENSE` file for details.
