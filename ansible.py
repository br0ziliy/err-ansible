from errbot import BotPlugin, arg_botcmd
from os import walk


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
                help="filename (w/o extension) of the inventory file")
    @arg_botcmd('playbook', type=str, \
                help="filename (w/o extension) of the playbook file")
    def ansible(self, mess, inventory=None, playbook=None):
        """
        Runs specified Ansible playbook on the specific inventory
        """
        inventory_file = "".join([self.config['INVENTORY_DIR'], inventory])
        playbook_file = "".join([self.config['PLAYBOOK_DIR'], playbook])
        return "This does nothing yet"

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
        # walk() comes from package "os"
        for (dirpath, dirnames, filenames) in walk(self.config['PLAYBOOK_DIR']):
            playbooks.extend(filenames)
            break
        for (dirpath, dirnames, filenames) in walk(self.config['INVENTORY_DIR']):
            inventories.extend(filenames)
            break
        # TODO: below code sucks rocks, but it's 11pm and I have a bottle of
        # cold beer waiting for me.
        if objects == 'playbooks': return { 'objects': objects, 'objlist': playbooks }
        elif objects == 'inventories': return { 'objects': objects, 'objlist': inventories }
        return { 'objects': 'all', 'objlist': playbooks + inventories }
