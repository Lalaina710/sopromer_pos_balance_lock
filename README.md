# SOPROMER - Verrou Fond de Caisse POS

Module Odoo 18 verrouillant le champ **Solde initial** (`cash_register_balance_start`) des sessions POS pour les caissiers, avec override manager justifié.

## Contexte

Mis en place suite aux erreurs récurrentes constatées sur les sessions POS SOPROMER :
- **POS/00204** : oubli de saisie (1 409 400 Ar manquants)
- **POS/00541** : sous-comptage (8 976 Ar)

Le pré-remplissage automatique avec le solde de clôture J-1 ferme une source d'erreur humaine.

## Comportement

| Acteur | Solde initial | Solde auto proposé | Raison override |
|--------|--------------|--------------------|-----------------| 
| Caissier (`group_pos_user`) | **Lecture seule** | Caché | Caché |
| Manager (`group_pos_manager`) | Editable | Visible (référence) | Visible si valeur modifiée |

### Pré-remplissage automatique
À la création d'une nouvelle session POS, le `cash_register_balance_start` est rempli automatiquement avec le `cash_register_balance_end_real` de la dernière session fermée du même point de vente. Si aucune session précédente fermée, valeur par défaut 0.

### Override manager
Si un manager modifie manuellement le solde initial (cas exceptionnels : versement weekend, vol, ajustement), le champ **Raison override** apparaît automatiquement et invite à justifier la modification (traçable via `mail.thread` grâce à `tracking=True`).

## Installation

```bash
# Sur serveur SOPROMER 45 (test)
cd /opt/odoo18/custom_addons/dev/
git clone https://github.com/Lalaina710/sopromer_pos_balance_lock.git
sudo chown -R odoo:odoo sopromer_pos_balance_lock
docker exec odoo-dev /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d "SOPROMER-rest260426" -i sopromer_pos_balance_lock --stop-after-init --no-http
docker restart odoo-dev
```

## Tests à valider

1. Connexion caissier → ouverture session → "Solde initial" doit être grisé
2. Connexion manager → "Solde initial" éditable + "Solde auto proposé" visible
3. Nouvelle session → balance_start pré-rempli avec balance_end_real session J-1
4. Manager modifie balance_start → "Raison override" devient visible

## Caractéristiques techniques

- **Version** : 18.0.1.0.0
- **Catégorie** : Point of Sale
- **License** : LGPL-3
- **Dépendances** : `point_of_sale` (autonome)
- **Modèles modifiés** : `pos.session` (héritage `_inherit`)
- **Frontend POS** : aucun impact (modification backend uniquement)

## Auteur

SOPROMER — Distribution produits mer, Madagascar.
