# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# ADMIN MENU
# ----------------------------------------------------------------------------------------------------------------------

active_path = request.controller

response.admin_menu = [ (T('Site'), False, URL('default','index'), []),
        #(T('Dash'), True if active_path == 'index' else False, URL('admin','index'), []),
        (T('Pages'), True if active_path == 'cms_page' else False, URL('admin','index'), []),
        (T('Files'), True if active_path == 'file' else False, URL('admin','file'), []),
        ]

response.admin_menu += [
        (T('Users'), True if active_path == 'users' else False, URL('admin','list_users'), []),
        (T('CSS'), True if active_path == 'css' else False, URL('admin','style_sheet'), []),
        ]

response.admin_menu += [
        (T('Help'), True if active_path == 'help' else False, URL('admin','help'), []),]


# ----------------------------------------------------------------------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# shortcuts
app = request.application
ctr = request.controller
cms_pages = None

if not auth.user:
    cms_pages = db((db.cms_page.page_index >= 0) & (db.cms_page.main_menu == True) & (db.cms_page.published == True) & (db.cms_page.members_only == False)).select(db.cms_page.ALL, orderby=[db.cms_page.page_index])
elif auth.has_membership('user', auth.user.id):
    cms_pages = db((db.cms_page.page_index >= 0) & (db.cms_page.main_menu == True) & (db.cms_page.published == True)).select(db.cms_page.ALL, orderby=[db.cms_page.page_index])
else:
    cms_pages = db((db.cms_page.page_index >= 0) & (db.cms_page.main_menu == True) & (db.cms_page.published == True) & (db.cms_page.members_only == False)).select(db.cms_page.ALL, orderby=[db.cms_page.page_index])

for cms_page in cms_pages:
    try:
        if cms_page.title == 'Register' and auth.has_membership('user', auth.user.id):
            continue
    except AttributeError:
        pass
       
    if cms_page.page_index == 0:
        response.title = cms_page.title
    else:
        if cms_page.published and not cms_page.parent_menu and not cms_page.url:
            sub_items = []

            for i in db(db.cms_page.parent_menu == cms_page.id).select(db.cms_page.id, db.cms_page.title, db.cms_page.parent_menu, db.cms_page.page_index, orderby=[db.cms_page.page_index]):
                sub_items += (T(i.title), False, URL('default','page/%s/%s' % (i.id, i.title.lower())), [])
            if sub_items:
                response.menu+=[ (T(cms_page.title), False, URL('default','page/%s/%s' % (cms_page.id, cms_page.title.lower())), [sub_items])]
            else: 
                response.menu+=[ (T(cms_page.title), False, URL('default','page/%s/%s' % (cms_page.id, cms_page.title.lower())))]
        elif cms_page.url:
            response.menu+=[ (T(cms_page.title), False, cms_page.url, []) ]

if "auth" in locals():
    auth.wikimenu()
