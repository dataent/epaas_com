

	
from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from subprocess import Popen, check_output, PIPE, STDOUT
import re, shlex, os, json, time, pymysql




@dataent.whitelist()
def create_site(site_name, mysql_password, admin_password, key):
	commands = ["bench new-site --mariadb-root-password {mysql_password} --admin-password {admin_password} {site_name}".format(site_name=site_name, 
		admin_password=admin_password, mysql_password=mysql_password)]
	commands.append("bench --site {site_name} install-app epaas".format(site_name=site_name))
	dataent.enqueue('bench_manager.clienttestapi.run_command',
		commands=commands,
		doctype="Bench Settings",
		key=key
	)
	all_sites = check_output("ls").strip('\n').split('\n')
	while site_name not in all_sites:
		time.sleep(2)
		print "waiting for site creation..."
		all_sites = check_output("ls").strip('\n').split('\n')
	doc = dataent.get_doc({'doctype': 'Site', 'site_name': site_name, 'app_list':'dataent', 'developer_flag':1})
	doc.insert()
	dataent.db.commit()
	
	
	
	

def run_command(commands, doctype, key, cwd='..', docname=' ', after_command=None):
	start_time = dataent.utils.time.time()
	console_dump = ''
	logged_command = ' && '.join(commands)
	logged_command += ' ' #to make sure passwords at the end of the commands are also hidden
	sensitive_data = ["--mariadb-root-password", "--admin-password", "--root-password"]
	for password in sensitive_data:
		logged_command = re.sub("{password} .*? ".format(password=password), '', logged_command, flags=re.DOTALL)
	doc = dataent.get_doc({'doctype': 'Bench Manager Command', 'key': key, 'source': doctype+': '+docname,
		 'command': logged_command, 'console': console_dump, 'status': 'Ongoing'})
	doc.insert()
	dataent.db.commit()
	dataent.publish_realtime(key, "Executing Command:\n{logged_command}\n\n".format(logged_command=logged_command), user=dataent.session.user)
	try:
		for command in commands:
			terminal = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd)
			for c in iter(lambda: terminal.stdout.read(1), ''):
				dataent.publish_realtime(key, c, user=dataent.session.user)
				console_dump += c
		if terminal.wait():
			_close_the_doc(start_time, key, console_dump, status='Failed', user=dataent.session.user)
		else:
			_close_the_doc(start_time, key, console_dump, status='Success', user=dataent.session.user)
	except:
		_close_the_doc(start_time, key, console_dump, status='Failed', user=dataent.session.user)
	finally:
		dataent.db.commit()
		# hack: dataent.db.commit() to make sure the log created is robust,
		# and the _refresh throws an error if the doc is deleted 
		dataent.enqueue('bench_manager.bench_manager.utils._refresh',
			doctype=doctype, docname=docname, commands=commands)