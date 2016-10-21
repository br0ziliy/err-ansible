# -*- coding: utf8 -*-

from errbot import BotPlugin, arg_botcmd
from os import path
from lib import utils, tasks
from itertools import chain
import argparse

CONFIG_TEMPLATE = {'INVENTORY_DIR': u"/etc/ansible/inventory",
                   'PLAYBOOK_DIR': u"/etc/ansible/playbooks",
                   'ANSIBLE_SSH_KEY': u"/root/.ssh/id_rsa.pub",
                   'ANSIBLE_REMOTE_USER': u"root",
                   'ANSIBLE_BIN_DIR': u'/usr/bin'}

class Ansible(BotPlugin):
    """
    Err plugin to run Ansible commands/playbooks
    """

    def activate(self):
        """
        Plugin "constructor", triggers on plugin activation
        """

        # array of task UUIDs for tasks.task_poller() to watch
        super(Ansible, self).activate()
        self.start_poller(5, self.task_poller)

    def configure(self, configuration):
        """
        Creates a Python dictionary object which contains all the values from our
        CONFIG_TEMPLATE and then updates that dictionary with the configuration
        received when calling the "!plugin config Ansible" command.
        """

        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE
        super(Ansible, self).configure(config)

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return CONFIG_TEMPLATE

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation
        """

        self.log.debug("Checking plugin configuration: {}".format(configuration))
        if not configuration['INVENTORY_DIR'].endswith('/'):
            configuration['INVENTORY_DIR'] = \
            "".join([configuration['INVENTORY_DIR'], '/'])
        if not configuration['PLAYBOOK_DIR'].endswith('/'):
            configuration['PLAYBOOK_DIR'] = \
            "".join([configuration['PLAYBOOK_DIR'], '/'])
        super(Ansible, self).check_configuration(configuration)

    @arg_botcmd('variables', type=str, nargs=argparse.REMAINDER, default=None,
                help="optional playbook variables")
    @arg_botcmd('timeout', type=int,
                help="Timeout for playbook execution")
    @arg_botcmd('inventory', type=str,
                help="filename of the inventory file")
    @arg_botcmd('playbook', type=str,
                help="filename of the playbook file")
    def ansible(self, mess, inventory=None, playbook=None, timeout=180,
                variables=None):
        """
        Runs specified Ansible playbook on the specific inventory
        """

        _from = mess.frm
        inventory_file = "".join([self.config['INVENTORY_DIR'], inventory])
        playbook_file = "".join([self.config['PLAYBOOK_DIR'], playbook])
        ssh_key = self.config['ANSIBLE_SSH_KEY']
        remote_user = self.config['ANSIBLE_REMOTE_USER']
        ansible_bin = path.join(self.config['ANSIBLE_BIN_DIR'],
                                u'ansible-playbook')
        # path come from "os" module
        if not path.isfile(inventory_file) or not path.isfile(playbook_file):
            return "*ERROR*: inventory/playbook file not found (was looking for \
                    {} {})".format(inventory_file, playbook_file)
        ansible_cmd = [ansible_bin, '-u', remote_user, '--private-key', ssh_key,
                       '-v', '-D', '-i', inventory_file, playbook_file]
        if variables:
            ansible_cmd.extend(['-e', " ".join(variables)])
        self.log.info("Running task with timeout of : %d" % timeout)
        raw_result = tasks.run_task(self, ansible_cmd, _from, timeout)
        return raw_result

    @arg_botcmd('objects', type=str, default='all', nargs='?',
                help="objects to list; choises are: playbooks, inventories, all (default)",
                template='list_objects')
    def ansible_list(self, mess=None, objects=None):
        """
        Lists available playbooks/inventory files
        """

        playbooks = []
        inventories = []
        backend = self._bot.mode
        if objects is 'playbooks' or objects is 'all':
            playbooks = utils.myreaddir(self.config['PLAYBOOK_DIR'])
        if objects is 'inventories' or objects is 'all':
            inventories = utils.myreaddir(self.config['INVENTORY_DIR'])
        return {'playbooks': playbooks, 'inventories': inventories, 'backend': backend}

    @arg_botcmd('command', type=str, nargs=argparse.REMAINDER,
                help="command to run on the host(s), or one of: ping, facts")
    @arg_botcmd('inventory', type=str,
                help="filename of the inventory file")
    @arg_botcmd('host', type=str,
                help="host pattern or group name from the inventory to run the command on")
    def ansible_cmd(self, mess, inventory=None, host=None, command=None):
        """
        Runs commands on remote servers using Ansible `command` module,
        with "ping" and "facts" having special meaning.
        """

        self.log.debug("Got command: {} for Host: {} "
                       "in Inventory: {}".format(command, host, inventory))
        _from = mess.frm
        command = " ".join(command)
        ssh_key = self.config['ANSIBLE_SSH_KEY']
        remote_user = self.config['ANSIBLE_REMOTE_USER']
        inventory_file = "".join([self.config['INVENTORY_DIR'], inventory])
        ansible_bin = path.join(self.config['ANSIBLE_BIN_DIR'],
                                u'ansible')
        self.log.debug("Full path to ansible command is: %s" % ansible_bin)
        # path come from "os" module
        if not path.isfile(inventory_file):
            return "*ERROR*: inventory file not found (was looking for \
                    {})".format(inventory_file)
        ansible_cmd = [ansible_bin, host, '-u', remote_user, '--private-key', ssh_key,
                       '-v', '-i', inventory_file, '-m']
        if command == 'ping':
            ansible_cmd.extend(['ping'])
        elif command == 'facts':
            ansible_cmd.extend(['setup'])
        else:
            ansible_cmd.extend(['command', '-a', command])
        raw_result = tasks.run_task(self, ansible_cmd, _from)
        return raw_result

    @arg_botcmd('uuid', type=str, nargs='?',
                help="Task UUID")
    def task_info(self, mess, uuid=None):
        """
        Obtains various types of information about queued tasks
        """

        if not uuid:
            return "Listing all jobs not implemented yet, please specify UUID of a job"
        (result, status) = tasks.get_task_info(uuid)
        if result:
            return "Task {} status: {}\n\n{}".format(uuid, status, result)
        else: return "Task {} status: {}".format(uuid, status)

    def task_poller(self):
        """
        Polls for in-progress tasks to notify users about task completion
        """

        self.log.debug("Polling for completed tasks...")
        if 'tasks' not in self:
            self['tasks'] = {}
        self.log.debug("Task list: {}".format(self['tasks']))
        tasklist = self['tasks']
        for uuid in list(tasklist):
            author = tasklist[uuid]
            (result, status) = tasks.get_task_info(uuid)
            self.log.debug("Processing task: {}; status: {},"
                           "result:\n{}".format(uuid, status, result))
            if status in ['finished', 'failed'] and result:
                self.send(self.build_identifier(author),
                          "Task {} status: {}\n\n{}".format(
                              uuid, status, result))
                del tasklist[uuid]
                self['tasks'] = tasklist
            else:
                self.log.debug("Task {} looks weird, ignoring. Status: {}"
                               "Result: {}".format(uuid, status, result))
                del tasklist[uuid]
                self['tasks'] = tasklist

