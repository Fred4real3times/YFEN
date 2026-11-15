# Direction visuelle YFEN

## Référence officielle

La référence visuelle et les règles UX actuelles sont définies dans [`brand-system.md`](brand-system.md). Cette spécification est issue de la nouvelle maquette de marque fournie en novembre 2026 et doit guider les prochains changements du frontend React.

**Tagline :** « Toute votre entreprise. Une seule fenêtre. »

Elle fixe la palette Horizon / Electric Teal / Or africain / Corail, les typographies Clash Display / Inter / JetBrains Mono, la navigation en six espaces et les règles de faible charge cognitive pour les dirigeants.

## Prototypes et captures historiques

- [`yfen-mockup.html`](yfen-mockup.html) est l'ancien prototype interactif. Il reste conservé pour référence de parcours et d'historique, mais sa direction visuelle précédente (vert menthe, violet et Space Grotesk) ne doit plus servir de référence pour les nouveaux composants.
- Les captures PNG dans [`../screenshots/`](../screenshots/) documentent ce prototype historique ; elles ne représentent pas encore le frontend aligné sur le nouveau brand system ni une session connectée à l'API.
- Les données, sociétés, montants, marges, trésorerie et noms de personnes visibles dans les prototypes sont fictifs. Ils ne doivent jamais servir de données métier ou d'exemples de KPI prétendument implémentés.

## Règle de contribution

Avant d'ajouter un écran ou un composant :
1. Identifier la question utilisateur à laquelle il répond.
2. Vérifier qu'il réduit une décision ou une tâche, plutôt que d'ajouter du bruit.
3. Réutiliser les tokens et la typographie de `brand-system.md`.
4. Afficher la fraîcheur, la couverture et la provenance lorsque des chiffres sont concernés.
5. Garder la même navigation et les mêmes permissions sur mobile et desktop.
