# -*- coding: utf-8 -*-
# Copyright 2014-2018 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.models import expression as osv_expression
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval
from datetime import timedelta

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.multi
    def compute_fiscalyear_dates(self, date):
        """ Computes the start and end dates of the fiscalyear where the given 'date' belongs to
            @param date: a datetime object
            @returns: a dictionary with date_from and date_to
        """
        self = self[0]
        last_month = 12
        last_day = 31
        if (date.month < last_month or (date.month == last_month and date.day <= last_day)):
            date = date.replace(month=last_month, day=last_day)
        else:
            date = date.replace(month=last_month, day=last_day, year=date.year + 1)
        date_to = date
        date_from = date + timedelta(days=1)
        date_from = date_from.replace(year=date_from.year - 1)
        return {'date_from': date_from, 'date_to': date_to}

class AccountAccountType(models.Model):
    _inherit = 'account.account.type'

    include_initial_balance = fields.Boolean('Incluir Banalce inicial')
