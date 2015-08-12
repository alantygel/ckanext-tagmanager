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
	

