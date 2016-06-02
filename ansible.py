from errbot import BotPlugin, arg_botcmd
from os import path
from subprocess import STDOUT, check_output, CalledProcessError
from lib import utils

class Ansible(BotPlugin):
    """
    Err plugin to run Ansible commands/playbooks
    """

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return {'INVENTORY_DIR': u"/etc/ansible/inventory", \
                'PLAYBOOK_DIR': u"/etc/ansible/playbooks", \
                'ANSIBLE_SSH_KEY': u"/root/.ssh/id_rsa.pub" \
               }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation
        """
        # TODO: check_configuration: check supplied plugin configuration
        self.log.debug("Checking plugin configuration: {}".format(configuration))
        if not configuration['INVENTORY_DIR'].endswith('/'):
            configuration['INVENTORY_DIR'] = \
            "".join([configuration['INVENTORY_DIR'],'/'])
        if not configuration['PLAYBOOK_DIR'].endswith('/'):
            configuration['PLAYBOOK_DIR'] = \
            "".join([configuration['PLAYBOOK_DIR'],'/'])
        super(Ansible, self).check_configuration(configuration)

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself
        """
        # TODO: callback_message
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself
        """
        # TODO: callback_botmessage
        pass

    @arg_botcmd('inventory', type=str, \
                help="filename of the inventory file")
    @arg_botcmd('playbook', type=str, \
                help="filename of the playbook file")
    def ansible(self, mess, inventory=None, playbook=None):
        """
        Runs specified Ansible playbook on the specific inventory
        """
        inventory_file = "".join([self.config['INVENTORY_DIR'], inventory])
        playbook_file = "".join([self.config['PLAYBOOK_DIR'], playbook])
        # path come from "os" module
        if not path.isfile(inventory_file) or not path.isfile(playbook_file):
            return "*ERROR*: inventory/playbook file not found (was looking for \
                    {} {})".format(inventory_file, playbook_file)
        ansible_cmd = ['ansible-playbook', '-u', 'root', '--private-key', self.config['ANSIBLE_SSH_KEY'], \
                        '-v', '-D', '-i', inventory_file, playbook_file]
        # PIPE and check_output come from "subprocess" module
        try:
            raw_result = check_output(ansible_cmd, stderr=STDOUT)
        except CalledProcessError, e:
            raw_result = e.output
        except OSError:
            raw_result = "*ERROR*: ansible-playbook command not found"
        return raw_result

    @arg_botcmd('objects', type=str, default='all', nargs='?', \
                help="objects to list; choises are: playbooks, inventories, all (default)", \
                template='list_objects')
    def ansible_list(self, mess, objects=None):
        """
        Lists available playbooks/inventory files
        """
        # TODO: make this recursive
        playbooks = []
        inventories = []
        if objects is 'playbooks' or objects is 'all':
            playbooks = utils.myreaddir(self.config['PLAYBOOK_DIR'])
        if objects is 'inventories' or objects is 'all':
            inventories = utils.myreaddir(self.config['INVENTORY_DIR'])
        return { 'playbooks': playbooks, 'inventories': inventories }
