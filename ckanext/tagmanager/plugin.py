import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import Levenshtein
from unidecode import unidecode
import db
import ckan.model as model
import ckan.model.meta as meta

def list_tags():
    return plugins.toolkit.get_action('tag_list')({},{'all_fields' : True})

def tag_show(id):
    return plugins.toolkit.get_action('tag_show')({},{'id' : id, 'include_datasets': True})

def get_name(id):
    return plugins.toolkit.get_action('tag_show')({},{'id' : id, 'include_datasets': False})['display_name']

def tags_stats():
	total_tags = len(model.Tag.all().all())

	total_taggings = len(meta.Session.query(model.PackageTag).all())

	return {'tags': total_tags, 'taggings': total_taggings}
    #tags_count = []
    #for t in range(0,len(tags)):
	#print tags[t]
	#tags_count[t] = plugins.toolkit.get_action('tag_show')({},{'id' : tags[t]['id']})

def tag_count(id):
    return plugins.toolkit.get_action('tag_show')({},{'id' : id, 'include_datasets': True})

def get_suggestions(suggestion_type=0, limit=None):
	return db.TagMergeSuggestion.by_type(suggestion_type, limit)

#def tags_merge_list_0(limit=None):
#	tags = list_tags()
#	T = len(tags)
#	merge_list = []
#	count = 0
#	if limit == None:
#		limit = 1000 #MAX_LIMIT
#	for t in range(0,T-1):
#		for s in range(t+1, T-1):
#			if unidecode(tags[s]['name'].lower()) == unidecode(tags[t]['name'].lower()):
#				merge_list.append([tags[s],tags[t]])
#				count += 1
#				if count > limit:
#					return merge_list

#	return merge_list

	

#def tags_merge_list_1(limit = None):
#	tags = list_tags()
#	T = len(tags)
#	merge_list = []
#	count = 0
#	if limit == None:
#		limit = 1000 #MAX_LIMIT
#	for t in range(0,T-1):
#		#check if there are numbers
#		stri = tags[t]['name'] 
#		if ([int(stri[i]) for i in range(0,len(stri)) if stri[i].isdigit()] == []) and (len(stri) > 3):
#			for s in range(t,T-1):
#				strj = tags[s]['name']
#				if (len(strj) > 3) and ([int(strj[i]) for i in range(0,len(strj)) if strj[i].isdigit()] == []):
#					if unidecode(tags[s]['name'].lower()) != unidecode(tags[t]['name'].lower()):
#						d = Levenshtein.distance(tags[t]['name'],tags[s]['name'])
#						if d < 3:
#							merge_list.append([tags[s],tags[t]])
#							count += 1
#							if count > limit:
#			   					return merge_list
#		
#	return merge_list

#def tags_merge_list_2(limit = None):
#	from nltk.corpus import wordnet as wn
#	tags = list_tags()
#	T = len(tags)
#	merge_list = []
#	count = 0
#	if limit == None:
#		limit = 1000 #MAX_LIMIT
#	for t in range(0,T-1):
#	#check if there are numbers
#		stri = tags[t]['name'] 
#		if ([int(stri[i]) for i in range(0,len(stri)) if stri[i].isdigit()] == []) and (len(stri) > 3):
#			syn1=wn.synsets(stri)
#			if syn1 != []:
#				for s in range(t,T-1):
#					strj = tags[s]['name']
#					if (len(strj) > 3) and ([int(strj[i]) for i in range(0,len(strj)) if strj[i].isdigit()] == []):
#						syn2=wn.synsets(strj)
#						if syn2 != []:
#							if unidecode(tags[s]['name'].lower()) != unidecode(tags[t]['name'].lower()):
#								if Levenshtein.distance(tags[t]['name'],tags[s]['name']) > 3:
#									b = max(syn2[i].wup_similarity(syn1[0]) for i in range(len(syn2)))
#									if b >= 1:
#										merge_list.append([tags[s],tags[t]])
#										count += 1
#										if count > limit:
#						   					return merge_list
#		
#	return merge_list

def has_suggestions(suggestion_type='all'):
	if suggestion_type == 'all':
		suggestions = db.TagMergeSuggestion.all();
	else: 
		suggestions = db.TagMergeSuggestion.by_type(suggestion_type);

	return len(suggestions)

class TagmanagerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IRoutes, inherit=True)
    #p.implements(p.IDomainObjectModification, inherit=True)
    #p.implements(p.IResourceUrlChange)
    plugins.implements(plugins.ITemplateHelpers)

    def configure(self, config):
        self.site_url = config.get('ckan.site_url')

    def before_map(self, map):
        tagmanager = 'ckanext.tagmanager.controller:TagmanagerController'

        map.connect('/tagmanager', 'tagmanager', controller=tagmanager, action='index')
        map.connect('/tagmanager/edit', controller=tagmanager, action='edit')
        map.connect('/tagmanager/index_process_suggestions', controller=tagmanager, action='index_process_suggestions')
        map.connect('/tagmanager/save_merge_suggestions', controller=tagmanager, action='save_merge_suggestions')
        map.connect('/tagmanager/merge_0', controller=tagmanager, action='merge_0')
        map.connect('/tagmanager/merge_1', controller=tagmanager, action='merge_1')
        map.connect('/tagmanager/merge_2', controller=tagmanager, action='merge_2')
        map.connect('/tagmanager/merge_form', controller=tagmanager, action='merge_form')
        map.connect('/tagmanager', controller=tagmanager, action='index')
        map.connect('/tagmanager/merge_confirm', controller=tagmanager, action='merge_confirm')
        map.connect('/tagmanager/merge', controller=tagmanager, action='merge')
        map.connect('/tagmanager/merge_do', controller=tagmanager, action='merge_do')
        map.connect('/tagmanager/delete_confirm', controller=tagmanager, action='delete_confirm')
        map.connect('/tagmanager/delete', controller=tagmanager, action='delete')
	return map

    def after_map(self, map):
        return map

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'tagmanager')

    def get_helpers(self):
	return {'tagmanager_list_tags':list_tags,'tagmanager_tag_show':tag_show, 'tagmanager_tags_stats': tags_stats, 'tagmanager_tag_count':tag_count, 'tagmanager_has_suggestions':has_suggestions, 'tagmanager_get_suggestions': get_suggestions, 'tagmanager_get_name':get_name}
