# -*- coding: utf-8 -*-
# Copyright 2026 SOPROMER
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'SOPROMER - Verrou Fond de Caisse POS',
    'version': '18.0.1.0.1',
    'category': 'Point of Sale',
    'summary': 'Verrouille le solde initial POS pour caissiers, override manager',
    'description': """
SOPROMER - Verrou Fond de Caisse POS
=====================================

Verrouille le champ "Solde initial" (cash_register_balance_start) sur les
sessions POS pour les caissiers (group_pos_user) afin d'eviter les erreurs
de saisie a l'ouverture (ex: oubli, sous-comptage).

Fonctionnalites
---------------
* Champ "Solde initial" en lecture seule pour les caissiers
* Champ editable uniquement pour les managers (group_pos_manager)
* Pre-remplissage automatique a la creation de session avec le solde de
  cloture reel (cash_register_balance_end_real) de la derniere session
  fermee du meme PdV
* Champ "Raison override" obligatoire si le manager modifie le solde propose
  (tracabilite : versement weekend, vol, ajustement, etc.)
* Affichage du solde auto-propose pour les managers a titre de reference

Cas d'usage business
--------------------
Reduit le risque d'erreurs recurrentes type POS/00204 (oubli) et POS/00541
(sous-comptage) en fermant la possibilite d'editer manuellement par les
caissiers, tout en laissant la souplesse aux managers en cas d'exception.
    """,
    'author': 'SOPROMER',
    'website': 'https://github.com/Lalaina710/sopromer_pos_balance_lock',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/pos_session_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
