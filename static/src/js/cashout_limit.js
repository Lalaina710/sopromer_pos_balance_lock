/** @odoo-module **/
/*
 * Copyright 2026 SOPROMER
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
 *
 * Patch CashMovePopup : bloque les Cash Out dont le montant dépasse le
 * solde caisse courant de la session.
 *
 * Formule solde courant (calculée côté backend) :
 *   solde = cash_register_balance_start
 *           + sum(cash payments encaissés cette session)
 *           + sum(cash ins déjà effectués)
 *           - sum(cash outs déjà effectués)
 *
 * Règle de sécurité DURE : aucun manager override possible.
 * Cash In : jamais bloqué.
 */

import { CashMovePopup } from "@point_of_sale/app/navbar/cash_move_popup/cash_move_popup";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { parseFloat } from "@web/views/fields/parsers";

patch(CashMovePopup.prototype, {
    /**
     * Surcharge confirm() pour injecter le contrôle Cash Out.
     *
     * Séquence :
     *  1. Si type !== 'out' → déléguer à super() sans contrôle
     *  2. Si montant invalide ou nul → déléguer à super() (il gérera l'erreur)
     *  3. Appel backend get_current_cash_balance pour solde temps réel
     *  4. Montant > solde → AlertDialog + retour (bloqué)
     *  5. Montant ≤ solde → super() normal
     */
    async confirm() {
        // Seulement pour les Cash Out
        if (this.state.type !== "out") {
            return super.confirm();
        }

        // Montant non saisi ou invalide : laisser super() gérer
        const amount = parseFloat(this.state.amount);
        if (!amount || amount <= 0) {
            return super.confirm();
        }

        // Récupérer solde courant depuis backend (temps réel, inclut
        // les cash moves déjà validés dans la session courante)
        let currentBalance;
        try {
            currentBalance = await this.pos.data.call(
                "pos.session",
                "get_current_cash_balance",
                [[this.pos.session.id]],
                {}
            );
        } catch (err) {
            // En cas d'erreur réseau : bloquer par précaution (sécurité dure)
            this.dialog.add(AlertDialog, {
                title: _t("Erreur vérification solde"),
                body: _t(
                    "Impossible de vérifier le solde caisse courant. " +
                    "Veuillez réessayer ou contacter un responsable technique."
                ),
            });
            return;
        }

        // Contrôle : montant retiré > solde disponible
        if (amount > currentBalance) {
            const formattedAmount = this.env.utils.formatCurrency(amount);
            const formattedBalance = this.env.utils.formatCurrency(currentBalance);
            this.dialog.add(AlertDialog, {
                title: _t("Cash Out refusé"),
                body: _t(
                    "Montant retiré (%s) dépasse le solde caisse courant (%s).",
                    formattedAmount,
                    formattedBalance
                ),
            });
            return;
        }

        // Solde suffisant : procéder normalement
        return super.confirm();
    },
});
