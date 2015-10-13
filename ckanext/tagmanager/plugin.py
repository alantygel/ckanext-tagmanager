import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import Levenshtein
from unidecode import unidecode

def list_tags():
#     query = db.Tag.query()
#     query = query.filter_by(state='active')
#     return query


    return plugins.toolkit.get_action('tag_list')({},{'all_fields' : True})

def tag_show(id):
    return plugins.toolkit.get_action('tag_show')({},{'id' : id, 'include_datasets': True})


def tags_merge_list_0():
    tags = list_tags()
    T = len(tags)
    dist = [[0 for x in range(T)] for x in range(T)]
    for t in range(0,T-1):
	for s in range(t, T-1):
            if unidecode(tags[s]['name'].lower()) == unidecode(tags[t]['name'].lower()):
		dist[s][t] = 1	

    return dist

def tags_merge_list_1():
    tags = list_tags()
    T = len(tags)
    dist = [[10 for x in range(T)] for x in range(T)] 
    for t in range(0,T-1):
	#check if there are numbers
	stri = tags[t]['name'] 
	if ([int(stri[i]) for i in range(0,len(stri)) if stri[i].isdigit()] == []):
            for s in range(t,T-1):
		strj = tags[s]['name']
		if (s!=t) and ([int(strj[i]) for i in range(0,len(strj)) if strj[i].isdigit()] == []):
		    if unidecode(tags[s]['name'].lower()) != unidecode(tags[t]['name'].lower()):
	    	    	dist[s][t] = Levenshtein.distance(tags[t]['name'],tags[s]['name'])
		
    return dist

def tags_merge_list_2():
    tags = list_tags()
    T = len(tags)
    dist = [[0 for x in range(T)] for x in range(T)]
    for t in range(0,T-1):
        #check if there are numbers
        stri = tags[t]['name']
        if ([int(stri[i]) for i in range(0,len(stri)) if stri[i].isdigit()] == []):
            for s in range(t,T-1):
                strj = tags[s]['name']
                if (s!=t) and ([int(strj[i]) for i in range(0,len(strj)) if strj[i].isdigit()] == []):
                    if unidecode(tags[s]['name'].lower()) != unidecode(tags[t]['name'].lower()):
    			url = 'http://maraca.d.umn.edu/cgi-bin/similarity/similarity.cgi?word1=' + stri + '&senses1=all&word2=' + strj + '&senses2=all&measure=path&rootnode=yes'
                        dist[s][t] = Levenshtein.distance(tags[t]['name'],tags[s]['name'])

    return dist






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
        map.connect('/tagmanager/edit', 'tagmanager/edit', controller=tagmanager, action='edit')
        map.connect('/tagmanager', controller=tagmanager, action='index')
        map.connect('/tagmanager/merge_confirm', controller=tagmanager, action='merge_confirm')
        map.connect('/tagmanager/merge', controller=tagmanager, action='merge')
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
	return {'tagmanager_list_tags':list_tags,'tagmanager_tag_show':tag_show, 'tagmanager_tags_merge_list_0': tags_merge_list_0, 'tagmanager_tags_merge_list_1': tags_merge_list_1}
