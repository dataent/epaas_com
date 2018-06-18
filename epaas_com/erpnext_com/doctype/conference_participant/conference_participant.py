# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataent.model.document import Document

class ConferenceParticipant(Document):
	def on_payment_authorized(self, status_changed_to=None):
		self.paid = 1
		self.save(ignore_permissions=True)
