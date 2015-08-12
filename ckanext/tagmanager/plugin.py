import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def list_tags():
    return plugins.toolkit.get_action('tag_list')({},{'all_fields' : True})

def tag_show(id):
    return plugins.toolkit.get_action('tag_show')({},{'id' : id, 'include_datasets': True})

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
	return map

    def after_map(self, map):
        return map

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'tagmanager')

    def get_helpers(self):
	return {'tagmanager_list_tags':list_tags,'tagmanager_tag_show':tag_show}
