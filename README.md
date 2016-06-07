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

Plugin is known to work on following platforms/Err backends:

- CentOS 7.2 / Telegram

Installation
------------

`!repos install https://github.com/br0ziliy/err-ansible.git`

You will also need to run the RQ worker in the directory where Errbot installed
the plugin (`/var/lib/err/plugins/err-ansible` by default:

```
cd /var/lib/err/plugins/err-ansible
bin/start_worker.sh
```

Make sure the user account under which you run RQ worker is able to execute
`ansible-playbook` command, and has read access to the directories/keyfile you
supply in the plugin configuration dictionary (see below).

Running worker from a different user than you run Errbot itself might lead to an
unpredictalble results - i.e. if you run Errbot process under `chat_bot`
account, you MUST run the worker under the same `chat_bot`, otherwise things
might not work. This will be fixed in the future, see br0ziliy/err-ansbile#3.

Configuration
-------------

Plugin is configured with the commands below:

- initial configuration:

`!plugin config Ansible {'ANSIBLE_SSH_KEY': u'/home/devops_bot/.ssh/id_rsa', 'INVENTORY_DIR': u'/etc/ansible/inventory', 'PLAYBOOK_DIR': u'/etc/ansible/playbooks', 'ANSIBLE_REMOTE_USER': 'root'}`

- if you want to change some parameter later:

`!plugin config Ansible {'ANSIBLE_REMOTE_USER': 'deploy_user'}`

Available parameters:

- `ANSIBLE_SSH_KEY` - SSH key to use with `ansible-playbook` command
- `ANSIBLE_REMOTE_USER` - SSH user Ansible will use to authenticate to the
    machines.
- `INVENTORY_DIR` - directory where inventory files are stored (subdirectories
  are not yet supported, see br0ziliy/err-ansbile#2)
- `PLAYBOOK_DIR` - directory where playbook files are stored (subdirectories are
  not yet supported, see br0ziliy/err-ansbile#2)

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
