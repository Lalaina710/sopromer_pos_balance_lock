# -*- coding: utf-8 -*-
# Copyright 2026 SOPROMER
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    cash_balance_override_reason = fields.Char(
        string="Raison de l'override fond de caisse",
        help="Raison obligatoire si le manager modifie le solde d'ouverture "
             "automatiquement propose (ex: versement weekend, vol, "
             "ajustement exceptionnel).",
        tracking=True,
    )
    cash_balance_auto_proposed = fields.Float(
        string="Solde auto propose (J-1)",
        compute='_compute_cash_balance_auto_proposed',
        store=False,
        help="Solde calcule automatiquement depuis la derniere session "
             "fermee du meme point de vente. Sert de reference visuelle "
             "pour le manager afin de detecter une eventuelle modification "
             "manuelle du solde d'ouverture.",
    )
    is_pos_manager = fields.Boolean(
        string="Est manager POS",
        compute='_compute_is_pos_manager',
        store=False,
        help="True si l'utilisateur courant appartient au groupe "
             "point_of_sale.group_pos_manager. Champ technique utilise "
             "dans la vue pour gerer le readonly du solde d'ouverture "
             "(remplace l'appel user_has_groups invalide en attribut XML).",
    )

    @api.depends_context('uid')
    def _compute_is_pos_manager(self):
        """Indique si l'utilisateur courant est manager POS.
        Utilise pour griser cash_register_balance_start dans la vue."""
        is_mgr = self.env.user.has_group('point_of_sale.group_pos_manager')
        for rec in self:
            rec.is_pos_manager = is_mgr

    @api.depends('config_id', 'state')
    def _compute_cash_balance_auto_proposed(self):
        """Recupere la balance_end_real de la derniere session fermee
        du meme PdV. Utilise par les managers en reference visuelle."""
        for session in self:
            domain = [
                ('config_id', '=', session.config_id.id),
                ('state', '=', 'closed'),
            ]
            if session.id:
                domain.append(('id', '!=', session.id))
            previous = self.env['pos.session'].search(
                domain, order='stop_at desc', limit=1,
            )
            session.cash_balance_auto_proposed = (
                previous.cash_register_balance_end_real if previous else 0.0
            )

    @api.model_create_multi
    def create(self, vals_list):
        """Pre-remplir cash_register_balance_start avec le solde de cloture
        reel de la derniere session fermee du PdV (J-1).

        Si la valeur est deja fournie explicitement (cas manager qui force
        une valeur autre), on respecte la saisie.
        """
        for vals in vals_list:
            if not vals.get('cash_register_balance_start'):
                config_id = vals.get('config_id')
                if config_id:
                    previous = self.search([
                        ('config_id', '=', config_id),
                        ('state', '=', 'closed'),
                    ], order='stop_at desc', limit=1)
                    if previous:
                        vals['cash_register_balance_start'] = (
                            previous.cash_register_balance_end_real
                        )
        return super().create(vals_list)
