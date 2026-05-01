/** @odoo-module **/
/*
 * Copyright 2026 SOPROMER
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
 *
 * Patch frontend POS OWL : grise l'input "Espèces à l'ouverture" dans la
 * popup "Contrôle à l'ouverture" pour les caissiers (group_pos_user) afin
 * d'aligner le comportement frontend avec le verrouillage backend déjà en
 * place sur pos.session.cash_register_balance_start.
 *
 * Critère d'autorisation : this.pos.user._role === "manager", pré-calculé
 * par Odoo natif côté backend (point_of_sale/models/res_users.py) en
 * fonction de l'appartenance au groupe point_of_sale.group_pos_manager.
 */

import { OpeningControlPopup } from "@point_of_sale/app/store/opening_control_popup/opening_control_popup";
import { patch } from "@web/core/utils/patch";

patch(OpeningControlPopup.prototype, {
    /**
     * Indique si l'utilisateur courant est manager POS.
     * Utilise le rôle pré-calculé natif Odoo (cf. res_users.py _load_pos_data).
     * Fallback : si pos.user manquant ou rôle absent, on log et on traite
     * comme caissier (verrouillé) — diagnostic via console pour les cas
     * où le user POS n'est pas correctement chargé en frontend.
     * @returns {boolean}
     */
    get isPosManager() {
        // _role est pose par pos_store.js mais peut etre undefined a l'init
        // du popup (timing). Fallback sur raw.role qui vient direct du
        // backend _load_pos_data (toujours defini).
        const user = this.pos?.user;
        const role = user?._role || user?.raw?.role;
        return role === "manager";
    },

    /**
     * Verrou frontend : input "Espèces à l'ouverture" en lecture seule pour
     * les caissiers. Les managers gardent l'édition libre (override avec
     * justification dans le champ backend cash_balance_override_reason).
     * @returns {boolean}
     */
    get isOpeningCashReadonly() {
        return !this.isPosManager;
    },
});
