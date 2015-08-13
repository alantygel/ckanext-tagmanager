=============
ckanext-tagmanager
=============

This is extensions aims to fill the tag managament gap of CKAN. CKAN core offers only a listing of tags, and edition through the the specific datasets. 

Tagmanager offers a graphical interface for adding, editing, removing and merging tags. This is usefull for big open data portals with many contributors, where tags are not always kept consistent.

In the future, we plan to offer the creation of relationships between tags, and connection to a central semantic tag server.

------------
Requirements
------------

Before installing tagmanager, make sure you have:

* CKAN 2.0+
* Levenshtein python library: https://github.com/ztane/python-Levenshtein/

------------
Installation
------------

To install ckanext-tagmanager:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-tagmanager Python package into your virtual environment::

     pip install ckanext-tagmanager

3. Add ``tagmanager`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

------------------------
Development Installation
------------------------

To install ckanext-tagmanager for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/alantygel/ckanext-tagmanager.git
    cd ckanext-tagmanager
    python setup.py develop
    pip install -r dev-requirements.txt

----------------------
Use
---------------------

Navigate to yoursite/tagamanager
