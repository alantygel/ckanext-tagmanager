import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

import ckan.plugins as p
from ckan.lib.base import BaseController, response, request
import json 
import db

import Levenshtein
from unidecode import unidecode


c = p.toolkit.c
render = p.toolkit.render

class TagmanagerController(BaseController):

	#index function for display form to load datasets for managing their relations
	def index(self):
		return render('tagmanager/index.html')

	def edit(self):
		return render('tagmanager/edit.html')

	def index_process_suggestions(self):
		return render('tagmanager/index_process_suggestions.html')	

	def merge_0(self):
		return render('tagmanager/index_merge_0.html')	

	def merge_1(self):
		return render('tagmanager/index_merge_1.html')	
   
	def merge_2(self):
		return render('tagmanager/index_merge_2.html')	

	def merge_form(self):
		return render('tagmanager/merge_form.html')	

	def merge_confirm(self):
		return render('tagmanager/merge_confirm.html')	

	def delete_confirm(self):
		return render('tagmanager/delete_confirm.html')	

	def delete(self):
		p.toolkit.get_action('tag_delete')({},{'id': request.POST['tag']})
		return render('tagmanager/index.html')	

	def merge(self):
		"assign all elements tagged with tag2 with tag1; delete tag2"

		tag2_datasets = p.toolkit.get_action('tag_show')({},{'id' : request.POST['tag2'], 'include_datasets': True})

		for ds in tag2_datasets['packages']:
			dataset = p.toolkit.get_action('package_show')({},{'id': ds['id'] })
			dataset['tags'].append(p.toolkit.get_action('tag_show')({},{'id':request.POST['tag1']}))
			p.toolkit.get_action('package_update')({},dataset)
		   
		p.toolkit.get_action('tag_delete')({},{'id': request.POST['tag2']})
	
		#p.toolkit.redirect_to(controller='tagmanager', action='index')

		return render('tagmanager/index.html')

	def merge_do(self):
		"assign all elements tagged with tag2 with tag1; delete tag2"

		merges = request.POST.getall('merge')
		for m in merges:
			self.merge_from_suggestion(m,request.POST["select_" + m])

		return render('tagmanager/index.html')

	def merge_from_suggestion(self, merge_id, tag_maintain):
		"assign all elements tagged with tag2 with tag1; delete tag2"
		
		merge_object = db.TagMergeSuggestion.by_id(merge_id)

		if merge_object.tag_id_1 == tag_maintain:
			tag_delete = merge_object.tag_id_2
		else:
			tag_delete = merge_object.tag_id_1

		tag_delete_datasets = p.toolkit.get_action('tag_show')({},{'id' : tag_delete, 'include_datasets': True})

		for ds in tag_delete_datasets['packages']:
			dataset = p.toolkit.get_action('package_show')({},{'id': ds['id'] })
			dataset['tags'].append(p.toolkit.get_action('tag_show')({},{'id':tag_maintain}))
			p.toolkit.get_action('package_update')({},dataset)
		   
		merge_objects = db.TagMergeSuggestion.by_tag_id(tag_delete)
		for m in merge_objects:
			m.delete()
			m.commit()

		p.toolkit.get_action('tag_delete')({},{'id': tag_delete})
		return 

	def save_merge_suggestions(self,suggestion_type='all'):

		suggestion_type = request.POST['method']

		if suggestion_type == 'all':
			suggestions = self.get_merge_suggestions(0);
			for s in suggestions:
				session = db.TagMergeSuggestion(s[0],s[1],0) 
				session.save()
			suggestions = self.get_merge_suggestions(1);
			for s in suggestions:
				session = db.TagMergeSuggestion(s[0],s[1],1) 
				session.save()
			suggestions = self.get_merge_suggestions(2);
			for s in suggestions:
				session.db.TagMergeSuggestion(s[0],s[1],2)
				session.save()

		else:
			suggestions = self.get_merge_suggestions(suggestion_type);
			for s in suggestions:
				session = db.TagMergeSuggestion(s[0],s[1],suggestion_type)
				session.save()
	
		return render('tagmanager/index.html')


	def get_merge_suggestions(self,suggestion_type=0, limit=None):
		from nltk.corpus import wordnet as wn

		print suggestion_type
		tags = p.toolkit.get_action('tag_list')({},{'all_fields' : True})
		T = len(tags)
		merge_list = []
		for t in range(0,T-1):
			if ((suggestion_type == '0') or (suggestion_type == 'all')):
				for s in range(t+1, T-1):
					if unidecode(tags[s]['name'].lower()) == unidecode(tags[t]['name'].lower()):
						merge_list.append([tags[s]['id'],tags[t]['id']])

			if (suggestion_type == '1') or (suggestion_type == 'all'):
				stri = tags[t]['name'] 
				if ([int(stri[i]) for i in range(0,len(stri)) if stri[i].isdigit()] == []) and (len(stri) > 3):
					for s in range(t,T-1):
						strj = tags[s]['name']
						if (len(strj) > 3) and ([int(strj[i]) for i in range(0,len(strj)) if strj[i].isdigit()] == []):
							if unidecode(tags[s]['name'].lower()) != unidecode(tags[t]['name'].lower()):
								d = Levenshtein.distance(tags[t]['name'],tags[s]['name'])
								if d < 3:
									merge_list.append([tags[s]['id'],tags[t]['id']])

			if (suggestion_type == '2') or (suggestion_type == 'all'):
				stri = tags[t]['name'] 
				if ([int(stri[i]) for i in range(0,len(stri)) if stri[i].isdigit()] == []) and (len(stri) > 3):
					syn1=wn.synsets(stri)
					if syn1 != []:
						for s in range(t,T-1):
							strj = tags[s]['name']
							if (len(strj) > 3) and ([int(strj[i]) for i in range(0,len(strj)) if strj[i].isdigit()] == []):
								syn2=wn.synsets(strj)
								if syn2 != []:
									if unidecode(tags[s]['name'].lower()) != unidecode(tags[t]['name'].lower()):
										if Levenshtein.distance(tags[t]['name'],tags[s]['name']) > 3:
											b = max(syn2[i].wup_similarity(syn1[0]) for i in range(len(syn2)))
											if b >= 1:
												merge_list.append([tags[s]['id'],tags[t]['id']])
		
		return merge_list

