from errbot import BotPlugin, botcmd, webhook


class Ansible(BotPlugin):
    """
    Err plugin to run Ansible commands/playbooks
    """

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return {'ANSIBLE_BASEDIR': "/etc/ansible/",
                'ANSIBLE_SSH_KEY': "/root/.ssh/id_rsa.pub"
               }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation
        """
        # TODO: check_configuration: check supplied plugin configuration
        super(Ansible, self).check_configuration()

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

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @arg_botcmd('inventory', type=str, default='/etc/ansible/hosts')
    @arg_botcmd('playbook', type=str, default='/etc/ansible/site.yml')
    def ansible(self, mess, inventory=None, playbook=None):
        """Working horse of this plugin"""
        return "This does nothing yet"

    @arg_botcmd('objects', type=str, default='playbooks')
    def ansible_list(self, mess, objects=None):
        """Lists available playbooks/inventory files"""
        return "This does nothing yet"
