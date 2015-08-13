import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

import ckan.plugins as p
from ckan.lib.base import BaseController, response, request
import json 


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

	for ds in tag2_datasets['packages']:
	    dataset = p.toolkit.get_action('package_show')({},{'id': ds['id'] })
	    dataset['tags'].append(p.toolkit.get_action('tag_show')({},{'id':request.POST['tag1']}))
	    p.toolkit.get_action('package_update')({},dataset)
	   
	p.toolkit.get_action('tag_delete')({},{'id': request.POST['tag2']})
	
	return render('tagmanager/index.html')	
