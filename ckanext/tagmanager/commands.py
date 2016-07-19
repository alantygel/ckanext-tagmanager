import ckan.plugins as p
import paste.script
import db
import logging

from ckan.lib.cli import CkanCommand

from ckan import model

log = logging.getLogger(__name__)

class TagmanagerCommands(CkanCommand):
	"""
	ckanext-tagmanager commands:
	Usage::
		paster tagmanager migrate
	"""
	summary = __doc__.split('\n')[0]
	usage = __doc__

	parser = paste.script.command.Command.standard_parser(verbose=True)
	parser.add_option('-c', '--config', dest='config',
		default='development.ini', help='Config file to use.')

	def command(self):
		if not len(self.args):
			print self.__doc__
			return

		cmd = self.args[0]
		self._load_config()

		if cmd == 'migrate':
			self._migrate()
		else:
			print self.__doc__

	def _migrate(self):
		if not db.tag_merge_suggestions_table.exists():
			db.tag_merge_suggestions_table.create()
			log.info('Tag Merge Suggestions table created')
			print 'Tag Merge Suggestions table created'
		else:
			log.warning('Tag Merge Suggestions table already exists')
			print 'Tag Merge Suggestions table already exists'

