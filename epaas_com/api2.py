from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.integrations.utils import get_checkout_url

# TODO:
# 1. send email to particpant and us
# 2. who is coming page
# 3. final design

@dataent.whitelist(allow_guest=True)
def make_payment(full_name, email, company, workshop=0, conf=0, currency='inr'):
	if currency=='inr':
		conf_rate = 600
		workshop_rate = 2000
	else:
		conf_rate = 10
		workshop_rate = 50

	amount = int(workshop or 0) * workshop_rate + int(conf or 0) * conf_rate

	if not amount:
		dataent.msgprint('Please set no of tickets')
		return

	participant = dataent.get_doc({
		'doctype': 'Conference Participant',
		'full_name': full_name,
		'email_id': email,
		'company_name': company,
		'workshop': workshop,
		'conference': conf,
		'amount': amount
	}).insert(ignore_permissions=True)

	#get controller for respecctive payment gateway
	if currency == "inr":
		payment_gateway = "Razorpay"
	else:
		payment_gateway = "PayPal"

	return get_checkout_url(**{
		"amount": amount,
		"title": 'EPAAS Conference Tickets',
		"description": '{0} passes for conference, {1} passes for workshop'.format(int(conf or 0), int(workshop or 0)),
		"reference_doctype":  participant.doctype,
		"reference_docname": participant.name,
		"payer_email": email,
		"payer_name": full_name,
		"order_id": participant.name,
		"currency": currency,
		"payment_gateway": payment_gateway
	})
	
@dataent.whitelist()
def create_site(site_name):
	verify_whitelisted_call()
	commands = ["bench new-site --mariadb-root-password Bear515515 --admin-password Bear515515 {site_name}.buildbrand.xyz".format(site_name=site_name)]
	if install_epaas == "true":
		with open('apps.txt', 'r') as f:
		    app_list = f.read()
		if 'epaas' not in app_list:
			commands.append("bench get-app epaas")
		commands.append("bench --site {site_name}.buildbrand.xyz install-app epaas".format(site_name=site_name))
	dataent.enqueue('bench_manager.bench_manager.utils.run_command',
		commands=commands,
		doctype="Bench Settings",
		
	)
	all_sites = check_output("ls").strip('\n').split('\n')
	while site_name not in all_sites:
		time.sleep(2)
		print "waiting for site creation..."
		all_sites = check_output("ls").strip('\n').split('\n')
	doc = dataent.get_doc({'doctype': 'Site', 'site_name': site_name, 'app_list':'dataent', 'developer_flag':1})
	doc.insert()
	dataent.db.commit()
		

@dataent.whitelist(allow_guest=True)
def signup(full_name, email, subdomain, plan=None, distribution="epaas", res=None):
	status = _signup(full_name, email, subdomain, plan=plan,
		distribution=distribution, reseller=res)

	if status == 'success':
		location = dataent.redirect_to_message(_('Verify your Email'),
			"""<div><p>You will receive an email at <strong>{}</strong>,
			asking you to verify this account request.<p><br>
			<p>It may take a few minutes before you receive this email.
			If you don't find it, please check your SPAM folder.</p>
			</div>""".format(email), indicator_color='blue')

	elif status=='retry':
		return {}

	else:
		# something went wrong
		location = dataent.redirect_to_message(_('Something went wrong'),
			'Please try again or drop an email to support@epaas.com',
			indicator_color='red')

	return {
		'location': location
	}

@dataent.whitelist(allow_guest=True)
def check_subdomain_availability(subdomain):
	signup_domain = dataent.db.get_single_value('Central Settings', 'signup_domain') or dataent.local.conf.domain
	try:
		return validate_subdomain(subdomain)
	except dataent.DuplicateEntryError:
		dataent.local.message_log = []
		return '{0}.{1}'.format(subdomain, signup_domain)