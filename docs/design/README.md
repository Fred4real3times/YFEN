# Direction visuelle YFEN

## Référence officielle

La référence visuelle et les règles UX actuelles sont définies dans [`brand-system.md`](brand-system.md). La promesse est :

**« Toutes vos entreprises, en un seul endroit. »**  
*All your businesses, in one place.*

Le [`yfen-brand-mockup.html`](yfen-brand-mockup.html) est la maquette interactive de référence. Elle illustre un portefeuille de plusieurs entreprises, filiales et unités opérationnelles dans un seul espace YFEN, à travers six écrans : Cockpit, Portefeuille, Imports, Actions, Analyse et Paramètres & accès.

La direction visuelle repose sur Deep Horizon Blue, Electric Teal, Warm Sand / Or africain, Alert Coral et Horizon Blue ; typographies Clash Display, Inter et JetBrains Mono. Le document `brand-system.md` fixe aussi les règles de concision, de hiérarchie et de charge cognitive.

## Captures de référence

Les six captures WebP dans [`../screenshots/`](../screenshots/) sont rendues directement à partir du nouveau mockup :
- `01-cockpit.webp`
- `02-portefeuille.webp`
- `03-imports.webp`
- `04-actions.webp`
- `05-analyse.webp`
- `06-parametres.webp`

Elles utilisent exclusivement des données de démonstration fictives. Elles représentent le mockup, pas une session authentifiée de l'application React connectée à l'API.

## Prototypes historiques

[`yfen-mockup.html`](yfen-mockup.html) est l'ancien prototype. Il est conservé pour l'historique, mais sa direction visuelle précédente (vert menthe, violet et Space Grotesk) ne doit plus servir de référence aux nouveaux composants.

## Règle de contribution

Avant d'ajouter un écran ou un composant :
1. Identifier la question utilisateur à laquelle il répond.
2. Vérifier qu'il réduit une décision ou une tâche, plutôt que d'ajouter du bruit.
3. Réutiliser les tokens et la typographie de `brand-system.md`.
4. Afficher la fraîcheur, la couverture et la provenance lorsque des chiffres sont concernés.
5. Conserver un portefeuille multi-entreprises unique avec des permissions par rôle et par entité.
6. Garder la même architecture fonctionnelle et les mêmes permissions sur mobile et desktop.
