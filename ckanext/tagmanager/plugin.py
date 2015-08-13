import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import Levenshtein

def list_tags():
    return plugins.toolkit.get_action('tag_list')({},{'all_fields' : True})

def tag_show(id):
    return plugins.toolkit.get_action('tag_show')({},{'id' : id, 'include_datasets': True})

def tags_merge_list():
    tags = list_tags()
    T = len(tags)
    dist = [[0 for x in range(T)] for x in range(T)] 
    for t in range(0,T-1):
        for s in range(0,T-1):
	    if s != t:
	        dist[s][t] = Levenshtein.ratio(tags[t]['name'],tags[s]['name'])
		
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

        map.connect('/tagmanager', controller=tagmanager, action='index')
        map.connect('/tagmanager/merge_confirm', controller=tagmanager, action='merge_confirm')
        map.connect('/tagmanager/merge', controller=tagmanager, action='merge')
	return map

    def after_map(self, map):
        return map

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'tagmanager')

    def get_helpers(self):
	return {'tagmanager_list_tags':list_tags,'tagmanager_tag_show':tag_show, 'tagmanager_tags_merge_list': tags_merge_list}
