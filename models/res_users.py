# -*- coding: utf-8 -*-
# Copyright 2026 SOPROMER
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _load_pos_data(self, data):
        """Force role='manager' pour les administrateurs systeme.

        Sans ce patch, un Administrator sans group_pos_manager explicite
        est considere comme 'cashier' cote POS frontend, ce qui:
          - cache le bouton Cash In (sopromer_pos_cash_print v6+)
          - verrouille le solde d'ouverture (sopromer_pos_balance_lock)
          - applique les restrictions natives (price control, etc.)

        Politique SOPROMER : un admin doit toujours pouvoir intervenir
        (ouverture, Cash In, override prix). On marque donc tous les users
        ayant base.group_system comme manager POS.
        """
        res = super()._load_pos_data(data)
        if res.get('data'):
            user_id = res['data'][0].get('id')
            if user_id and self.browse(user_id).has_group('base.group_system'):
                res['data'][0]['role'] = 'manager'
        return res
