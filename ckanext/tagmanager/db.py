import vdm.sqlalchemy
from sqlalchemy.orm import relation, relationship
from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint, or_

import ckan.model.tag as _tag
import ckan.model.extension as _extension
import ckan.model.core as core
import ckan.model.meta as meta
import ckan.model.types as _types
import ckan.model.domain_object as domain_object
import ckan.model.activity as activity
import ckan  # this import is needed
import ckan.lib.dictization

__all__ = ['tag_merge_suggestions_table', 'TagMergeSuggestion']

tag_id_1 = Column('tag_id_1', types.UnicodeText, ForeignKey('tag.id',ondelete="CASCADE"))
tag_id_2 = Column('tag_id_2', types.UnicodeText, ForeignKey('tag.id',ondelete="CASCADE"))

tag_merge_suggestions_table = Table('tag_merge_suggestions', meta.metadata,
		Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
		tag_id_1,
		tag_id_2,
		Column('suggestion_type', types.Unicode)
)

#vdm.sqlalchemy.make_table_stateful(tag_semantictag_table)
# TODO: this has a composite primary key ...
#tag_semantictag_revision_table = core.make_revisioned_table(tag_semantictag_table)

class TagMergeSuggestion(domain_object.DomainObject):
	def __init__(self, tag_id_1, tag_id_2, suggestion_type):
		self.tag_id_1 = tag_id_1
		self.tag_id_2 = tag_id_2
		self.suggestion_type = suggestion_type

	def __repr__(self):
		return '<TagMergeSuggestion ' + self.tag_id_1 + ' ' + self.tag_id_2 + '>'   

	# not stateful so same as purge
	def delete(self):
		self.purge()
		return

	@classmethod
	def by_id(cls, id, autoflush=True):
		'''Return the suggestion with the given id, or None.

		:param id: the id of the tag merge suggestion
		:type id: string

		:returns: the suggestion with correspondent id or none
		:rtype: ckan.model.tag_merge_suggestion.TagMergeSuggestion

		'''
		query = meta.Session.query(TagMergeSuggestion).\
		filter(TagMergeSuggestion.id == id)

		return query.autoflush(autoflush).first()

	@classmethod
	def by_tag_id(cls, tag_id, autoflush=True):
		'''Return the suggestion with the given tag id, or None.

		:param tag_id: the id of the tag to look for suggestion
		:type tag_id: string

		:returns: the suggestions containing the specific tag id
		:rtype: ckan.model.tag.Tag # TODO check this

		'''
		query = meta.Session.query(TagMergeSuggestion).\
		filter(or_(TagMergeSuggestion.tag_id_1==tag_id,TagMergeSuggestion.tag_id_2==tag_id))

		query = query.autoflush(autoflush)
		tag_merge_suggestions = query.all()
		return tag_merge_suggestions

	@classmethod
	def by_type(cls, suggestion_type, limit=None, autoflush=True):
		'''Return the suggestion for a given type. Type options are: 0 (difference of capitals or special characters), 1 (levensthein distance smaller than 3) and 2 (synonyms).

		:param suggestion_type: suggestion_type (values 0 to 2)
		:type suggestion_type: integer (0-2)

		:returns: the suggestions objects
		:rtype: ckan.model.tag_merge_suggestion.TagMergeSuggestion

		'''

		if limit:
			query = meta.Session.query(TagMergeSuggestion).\
			filter(TagMergeSuggestion.suggestion_type == str(suggestion_type)).\
			limit(limit)
		else:
			query = meta.Session.query(TagMergeSuggestion).\
			filter(TagMergeSuggestion.suggestion_type == str(suggestion_type))

		query = query.autoflush(autoflush)
		tag_merge_suggestions = query.all()
		return tag_merge_suggestions

	@classmethod
	def all(cls,autoflush=True):
		'''Return the all suggestions in Database.

		:param suggestion_type: suggestion_type (values 0 to 2)
		:type suggestion_type: integer (0-2)

		:returns: the suggestions objects
		:rtype: ckan.model.tag_merge_suggestion.TagMergeSuggestion

		'''
		query = meta.Session.query(TagMergeSuggestion)
		return query.all()

#class TagSemanticTag(vdm.sqlalchemy.RevisionedObjectMixin,
#		vdm.sqlalchemy.StatefulObjectMixin,
#		domain_object.DomainObject):i


meta.mapper(TagMergeSuggestion, tag_merge_suggestions_table, properties={
	'tag_1': relation(_tag.Tag, foreign_keys=[tag_id_1]),
	'tag_2': relation(_tag.Tag, foreign_keys=[tag_id_2])
	}
	)


#meta.mapper(TagSemanticTag, tag_semantictag_table, properties={
#	'smtag':relation(_tag.Tag, backref='tag_semantictag_all',
#		cascade='none',
#		)
#	},
#	order_by=tag_semantictag_table.c.id,
##	extension=[vdm.sqlalchemy.Revisioner(tag_semantictag_revision_table),
##			   _extension.PluginMapperExtension(),
##			   ],
#	)

