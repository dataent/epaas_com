# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "epaas_com"
app_title = "EPAAS.com"
app_publisher = "Dataent"
app_description = "EPAAS.com website"
app_icon = "fa fa-globe"
app_color = "black"
app_email = "info@epaas.com"
app_url = "https://epaas.com"
app_version = "0.0.1"
hide_in_installer = True

website_context = {
	# "brand_html": "<img class='navbar-icon' src='/assets/dataent_theme/img/erp-icon.svg' />EPAAS",
	# "top_bar_items": [
	# 	{"label": "Pricing", "url": "/pricing", "right":1},
	# 	{"label": "Features", "url": "/features", "right":1},
	# 	{"label": "Docs", "url": "http://dataent.github.io/epaas", "right":1},
	# 	{"label": "Blog", "url": "https://dataent.io/blog", "right":1},
	# ],
	"hide_login": 1,
	"favicon": "/assets/dataent_theme/img/favicon.ico"
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/epaas_com/css/epaas_com.css"
# app_include_js = "/assets/epaas_com/js/epaas_com.js"

# include js, css files in header of web template
# web_include_css = "/assets/epaas_com/css/epaas_com.css"
web_include_js = "/assets/epaas_com/js/payment.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "epaas_com.install.before_install"
# after_install = "epaas_com.install.after_install"

# Desk Notifications
# ------------------
# See dataent.core.notifications.get_notification_config

# notification_config = "epaas_com.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "dataent.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "dataent.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"epaas_com.tasks.all"
# 	],
# 	"daily": [
# 		"epaas_com.tasks.daily"
# 	],
# 	"hourly": [
# 		"epaas_com.tasks.hourly"
# 	],
# 	"weekly": [
# 		"epaas_com.tasks.weekly"
# 	]
# 	"monthly": [
# 		"epaas_com.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "epaas_com.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"dataent.desk.doctype.event.event.get_events": "epaas_com.event.get_events"
# }

fixtures = ["Contact Us Settings"]
