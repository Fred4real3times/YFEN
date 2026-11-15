# Architecture technique YFEN

## Décision

**Monolithe modulaire Django + traitements différés**, exposé par API REST, avec un frontend React/TypeScript PWA. Pas de microservices au MVP. Les frontières métier sont matérialisées par des applications Django afin de conserver un faible coût d'exploitation et de pouvoir extraire un service plus tard si la charge le justifie.

## Vue de déploiement

```text
Android / Chrome mobile / navigateur desktop
                 |
        React + TypeScript + Vite
        PWA shell / IndexedDB futur
                 | HTTPS / JSON + multipart
                 v
       Django + Django REST Framework
  Auth | Workspace | Portfolio | Imports | KPI
      Actions | Alertes | Audit | Exports
          |             |             |
          v             v             v
      PostgreSQL      Redis       Stockage fichiers
      données métier  jobs futurs  quarantaine privée
          |             |
          +------ Celery (P1 / parsing lourd) ------+
                                      |
                            adaptateur LLM (P1)
                   contexte structuré, pas de SQL libre
```

## Modules Django

| Application | Responsabilité |
| --- | --- |
| `identity` | Identité, mot de passe, email unique et token d’accès. |
| `tenancy` | Workspaces, memberships, entités juridiques et unités opérationnelles. |
| `sources` | Lots de fichiers, faits métriques, provenance et anomalies de validation. |
| `actions` | Actions, responsable, priorité, statut, commentaires et preuves. |
| `alerts` | Alertes générées par des règles déterministes. |
| `audit` | Événements d’audit append-only au niveau modèle. |
| `api` | Auth, permissions tenant, sérialisation, endpoints, agrégats et exports. |

## Flux d’import P0 implémenté

1. L’utilisateur choisit le workspace, l’entité, la famille de rapport, la période et la devise.
2. L’API vérifie le rôle, la limite de taille (10 Mo), l’extension, la signature XLSX/PDF et les premiers octets du CSV.
3. Le fichier original est stocké dans le répertoire privé de quarantaine ; son SHA-256 est conservé et un doublon dans le workspace est rejeté.
4. L’aperçu CSV/XLSX présente les colonnes et dix lignes maximum. Pour un PDF, l’extraction textuelle est une aide de lecture ; elle ne crée pas de faits.
5. L’utilisateur choisit explicitement la colonne du montant et, en option, la colonne de date.
6. Les lignes sont analysées en `MetricFact.REVIEW`. Les lignes non conformes produisent des `ValidationIssue`.
7. Une confirmation explicite fait passer les faits de `REVIEW` à `VALIDATED` et le lot à `VALIDATED` dans une transaction. Seuls les faits validés sont exposés dans le cockpit.

### Familles de métriques agrégées

- `SALES` → `reported_revenue`
- `CASH` → `reported_collections`
- `BANK` → `reported_cash_balance`
- `EXPENSES` → `reported_expenses`
- `RECEIVABLES` → `reported_receivables`
- `PAYABLES` → `reported_payables`

La somme est effectuée par le backend avec `Decimal`. Dans la vue portefeuille, les faits ne sont agrégés qu’à métrique, période, devise et unité identiques ; les devises et périodes différentes restent séparées. Dans une vue entité, le filtre cible une seule entité. Le total portefeuille est un total arithmétique des données rapportées : aucune élimination des opérations intragroupe ni consolidation comptable n’est réalisée. Les taux de change ne sont pas appliqués automatiquement.

## Contrôle multi-tenant

Chaque endpoint métier reçoit un `workspace_id` puis résout un membership actif côté serveur. Les queryset sont filtrés par workspace ; les relations (entité, responsable) sont revalidées contre le même workspace dans les serializers. Un UUID difficile à deviner n'est jamais considéré comme une autorisation.

Rôles initiaux : `OWNER`, `ADMIN`, `ACCOUNTANT`, `MANAGER`, `VIEWER`. Le frontend masque certains contrôles selon le rôle, mais la permission décisive demeure dans l'API.

## Frontend

- React 19 + TypeScript, Vite 8.
- Navigation mobile et desktop dans un seul projet responsive.
- Le token d’accès est gardé dans `sessionStorage`, non dans `localStorage`.
- Le service worker ne met en cache que le shell statique et ne met jamais en cache `/api/` ou des réponses financières.
- Les montants affichés sont formatés dans le navigateur ; les sommes financières et agrégats restent calculés par le backend. Les agrégats portefeuille sont des totaux arithmétiques explicitement signalés comme non retraités intragroupe.
- Le menu Assistant IA est volontairement verrouillé P1.

## Dépendances structurantes

| Couche | Technologie | Usage |
| --- | --- | --- |
| API | Django 6.1.3 + DRF 3.18.3 | Auth, ORM, permissions, REST et admin. |
| Base | PostgreSQL 17 (Docker) | Données métier et transactions. SQLite est disponible en mode développement local. |
| Fichiers | Django Storage privé | Fichiers sources conservés hors des réponses publiques. |
| Tableurs | openpyxl | Lecture XLSX en mode lecture seule et `data_only`. |
| PDF | pdfplumber | Extraction textuelle assistée, sans OCR. |
| Jobs futurs | Celery + Redis | Parsing lourd, briefs et notifications asynchrones après le P0. |
| Frontend | React 19.3.0, TypeScript 5.9, Vite 8.3 ; Recharts retenu pour les visualisations (à intégrer) | PWA responsive, mobile-first, expérience exécutive concise. |

## Limites d’architecture à traiter avant pilote payant

- Générer, relire et committer les migrations initiales ; le scaffold actuel permet un bootstrap de développement mais ne doit pas lancer `makemigrations` en production.
- Déplacer le parsing des fichiers vers un worker isolé avec quotas CPU/mémoire, et ajouter scan antivirus/quarantaine opérationnelle.
- Activer MFA, rotation/expiration des tokens et sessions révocables par appareil.
- Configurer un stockage objet S3 privé chiffré, des liens temporaires, la politique de rétention et la restauration.
- Ajouter observabilité, alertes d’exploitation et tests de charge p95.


## Onboarding et configuration du template adaptatif

Le formulaire d’inscription envoie les données d’accès et le profil du workspace à `POST /api/v1/auth/register/`. Lorsque le bloc `workspace` est présent, la création utilisateur, workspace, membership OWNER, profil et événement d’audit est atomique.

`WorkspaceProfile` stocke les réponses structurées :
- `industry`, `operating_model`, `entity_count_band` ;
- `source_systems` et `selected_modules` sous forme de listes JSON contrôlées par des choix serveur ;
- `other_requirements` pour le contexte facultatif ;
- `template_version` pour versionner la configuration initiale des templates.

Les choix de modules utilisent les codes de familles de rapports déjà supportés par le pipeline P0 (`SALES`, `CASH`, `BANK`, `EXPENSES`, `RECEIVABLES`, `PAYABLES`). Le frontend les priorise dans le sélecteur d’import, sans rendre les autres familles indisponibles. Le profil ne remplace pas le mapping de colonnes : chaque fichier externe passe toujours par preview, mapping, validation et confirmation humaine.

Les anciens comptes sans workspace passent par le même composant de questions au moment de créer leur premier workspace. Les valeurs structurées sont validées côté API ; le texte libre n’est jamais exécuté ni interprété comme règle métier.


## Architecture d'expérience — précision, concision et faible charge cognitive

La direction de marque et d'expérience est définie dans [`docs/design/brand-system.md`](design/brand-system.md). Elle constitue une contrainte de conception, pas une simple couche cosmétique.

### Contrat d'expérience

- **Une seule application, des espaces adaptés au rôle.** Aucun produit ou frontend distinct pour le dirigeant et les opérateurs.
- **Owner : cockpit exécutif par défaut.** La première vue répond à « que dois-je savoir et traiter maintenant ? » ; elle privilégie la situation globale, quatre indicateurs de tête au maximum, trois exceptions prioritaires au maximum, la fraîcheur des données et les actions à arbitrer.
- **Accountant / Manager : espace opérationnel.** Leur entrée privilégie les imports à préparer, les anomalies à corriger, les lots en attente et les actions affectées. Les fonctions visibles dépendent des permissions et du périmètre attribué.
- **Détails progressifs.** Un chiffre ouvre son explication ; l'explication ouvre les sources ; les lignes détaillées et les filtres avancés ne sont pas exposés par défaut.
- **Une question et une action principale par écran.** Le Cockpit ne devient pas un outil BI. Les analyses graphiques approfondies restent dans l'écran Analyse.
- **Vocabulaire dirigeant.** Libellés courts, dates explicites, termes métier usuels ; les termes comptables spécialisés sont expliqués au moment où ils apparaissent.
- **Pas de fausse précision.** Une donnée partielle, ancienne ou non comparable est signalée au même niveau que la valeur. Une donnée absente n'est jamais remplacée par zéro ou par une estimation.
- **Defaults adaptatifs.** `WorkspaceProfile` peut prioriser les types de rapports, les filtres et les parcours pertinents, mais ne doit ni masquer définitivement les autres fonctions ni créer des KPI sans données suffisantes.

### Architecture de navigation cible

Les six espaces fonctionnels sont Cockpit, Portefeuille, Imports, Actions, Analyse, Paramètres & accès. Sur mobile, Cockpit, Portefeuille, Actions et Analyse constituent les onglets visibles ; l'import est l'action centrale ; les paramètres sont accessibles depuis l'en-tête. Sur desktop, la même hiérarchie s'adapte en navigation latérale. Ce découpage reprend la maquette de marque : six écrans, un cockpit.

### Périmètres d'accès et séparation des tâches

- Un `WorkspaceMembership` doit pouvoir porter des accès explicites à une ou plusieurs entités/unités opérationnelles. Les filtres de périmètre sont appliqués dans les querysets et services backend, jamais uniquement dans React.
- Le dirigeant OWNER conserve une vue portefeuille globale et les capacités d'arbitrage prévues par ses permissions.
- Le comptable travaille sur les entités qui lui sont attribuées, contrôle les données et traite la file de revue.
- Le gestionnaire de site importe et suit les informations de son périmètre ; il ne voit pas automatiquement les autres entités ni les agrégats globaux.
- **Maker–checker cible :** le préparateur soumet un lot ; une personne autorisée et distincte le vérifie et le publie. L'auto-approbation est interdite, sauf mécanisme d'urgence audité explicitement défini.
- État actuel à ne pas masquer : les permissions par unité et l'approbation indépendante ne sont pas encore complètement implémentées. Les endpoints actuels de confirmation d'import reposent sur le rôle générique d'écriture. Ces contrôles doivent être réalisés côté API avant un pilote multi-utilisateur.

## Moteur analytique, KPI et génération des graphiques

### Calculs financiers

Le backend reste l'unique source de vérité des calculs. Le moteur analytique doit évoluer depuis `apps/api/metrics.py` et `apps/api/data_services.py`, sans déplacer les formules financières vers React ou vers un LLM.

- Utiliser `Decimal` pour les montants, agrégations, variations et ratios financiers ; ne pas utiliser `float` pour la logique financière.
- Maintenir un registre de KPI versionné : identifiant, libellé utilisateur, définition, formule, champs sources, unité, devise, période, règles de signe, prérequis, version de formule et tests de référence.
- Un ratio n'est publié que si toutes ses composantes et les périodes nécessaires sont disponibles et comparables. Une base nulle ou une période non comparable produit « N/A / non calculable », jamais une valeur inventée.
- Les KPI distinguent les valeurs rapportées des valeurs rapprochées ou consolidées. Le libellé doit refléter le niveau réel de contrôle.
- Les agrégations de portefeuille regroupent uniquement les faits de même métrique, unité, période et devise. Aucune conversion automatique ; aucune élimination intragroupe au MVP.
- Chaque réponse KPI conserve sa provenance : lots, fichiers, lignes/champs, règle appliquée, date de collecte, date de validation et personne ayant validé.
- La fraîcheur et la couverture des données sont des attributs de premier niveau. Une valeur partielle ne peut pas être présentée comme complète.

### Contrat API pour la visualisation

L'API fournit des séries prêtes à afficher, pas des formules à exécuter dans le navigateur. Chaque série contient au minimum : clé et libellé de métrique, période, devise, unité, points temporels ou catégories, couverture, fraîcheur et références de provenance.

Les valeurs financières exactes restent sérialisées dans un format décimal sans perte (chaînes décimales). Si la bibliothèque graphique exige une coordonnée numérique, le backend peut fournir une représentation de tracé bornée et documentée ; elle ne devient jamais la valeur comptable officielle. Les infobulles et les cartes affichent la valeur exacte formatée par le serveur ou à partir de sa représentation décimale, sans recalcul financier dans le navigateur.

### Rendu des graphiques

- **Choix cible : Recharts**, bibliothèque déclarative React qui rend les graphiques en SVG et propose des comportements responsives. La dépendance n'est pas encore installée dans le frontend au moment de cette mise à jour.
- Graphique en ligne pour une évolution temporelle ; barres pour comparer des entités/périodes ; donut uniquement pour une répartition simple et utile.
- Les graphiques détaillés se trouvent dans Analyse, pas dans le Cockpit exécutif par défaut.
- Chaque visualisation doit avoir une question/titre, une période, une unité/devise et un statut de couverture. Pas de graphique si les données sont insuffisantes ou non comparables.
- Limiter les séries et les légendes ; conserver un tableau ou une liste accessible ; respecter les couleurs sémantiques du brand system, sans palette arc-en-ciel.
- Les interactions de graphique servent à ouvrir le détail et la provenance ; elles ne déclenchent aucune modification des données sources.

### État réel vs cible

| Capacité | État au moment de cette mise à jour |
| --- | --- |
| Agrégation des faits validés | Socle implémenté dans `build_cockpit`, avec `Decimal` et séparation par devise/période/unité. |
| Registre complet de formules et ratios | À concevoir et tester ; le socle actuel n'est pas un moteur financier complet. |
| API de séries chronologiques / comparatives | À développer ; le cockpit actuel renvoie principalement des agrégats par groupe. |
| Bibliothèque Recharts et graphiques connectés | Décision d'architecture ; non installée/non intégrée à ce commit. |
| Alignement complet du frontend sur le brand system | À réaliser ; le CSS existant ne reprend pas encore toutes les couleurs et typographies de la nouvelle maquette. |

## Rôle de l'intelligence artificielle

L'IA intervient après le moteur de calcul, comme couche d'explication et d'assistance :

1. Les services métier déterminent les KPI, alertes, périodes comparables et données sources accessibles.
2. Le contexte envoyé au LLM contient uniquement les agrégats autorisés, leurs définitions, leurs limites et leurs références.
3. Le LLM rédige une synthèse courte, explique les écarts, répond aux questions et peut proposer une action.
4. Les chiffres restitués sont liés aux résultats structurés reçus ; le LLM ne recalcule pas les montants, ne crée pas de KPI, n'invente pas de causes et n'accède jamais au SQL libre.
5. Toute action créée à partir d'une suggestion exige un aperçu et une confirmation humaine.

L'assistant doit savoir répondre « données insuffisantes », « période non comparable » ou « source trop ancienne ». Sa réponse est concise, orientée décision et accompagnée des références qui permettent d'ouvrir la preuve.
