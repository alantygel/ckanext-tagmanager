import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

import ckan.plugins as p
from ckan.lib.base import BaseController, response, request

c = p.toolkit.c
render = p.toolkit.render

class TagmanagerController(BaseController):

    #index function for display form to load datasets for managing their relations
    def index(self):
	return render('tagmanager/index.html')

    def merge_confirm(self):
	return render('tagmanager/merge_confirm.html')	

    def merge(self):
	"assign all elements tagged with tag2 with tag1; delete tag2"

	tag2_datasets = p.toolkit.get_action('tag_show')({},{'id' : request.POST['tag2'], 'include_datasets': True})

	for dataset in tag2_datasets['packages']:
	    #dataset = p.toolkit.get_action('package_show')({},{'id': ds['id'] })
	    dataset['tags'].append(p.toolkit.get_action('tag_show')({},{'id':request.POST['tag1']}))
	    #print ds['tags']	

	    #p.toolkit.get_action('package_update')({},{'id':dataset['id'], 'tags':dataset['tags']})

	#p.toolkit.get_action('tag_delete')({}{'id': request.POST['tag2']})


	

	print "Tag merged!"



	return #render('tagmanager/index.html')	
