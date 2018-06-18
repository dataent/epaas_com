from __future__ import unicode_literals
import dataent
from central.utils import get_signup_domain

def get_context(context):
	return {
		'signup_domain': get_signup_domain() or 'epaas.com'
	}
