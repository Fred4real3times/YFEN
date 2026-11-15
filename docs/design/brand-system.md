# YFEN — Brand system & UX principles

**Statut : référence visuelle et expérience cible.**  
Cette fiche formalise la nouvelle maquette de marque fournie en novembre 2026. Elle prévaut sur les choix visuels de l'ancien prototype `yfen-mockup.html`.

## 1. Promesse de marque

**Tagline principale : « Toutes vos entreprises, en un seul endroit. »**

**English : “All your businesses, in one place.”**

**Descripteur :** Le cockpit de pilotage de votre portefeuille d'entreprises.

YFEN — *Your Financial & Executive Navigator* — réunit dans un même espace les entreprises, filiales, établissements et activités qu'un dirigeant supervise. Il rassemble les rapports de gestion disponibles de ces différentes entités dans un portefeuille unique, fait ressortir ce qui mérite l'attention et aide les équipes à suivre les actions. YFEN ne remplace pas les logiciels opérationnels : il rend leurs informations lisibles, vérifiables et actionnables.

Le Y-Horizon représente la convergence de plusieurs entreprises et activités vers un point de décision commun. Le point radar cerclé d'or africain désigne le signal utile à capter, pas un élément décoratif.

### Portée de la promesse « toutes vos entreprises »

- « Toutes » désigne les entreprises, filiales et établissements rattachés au portefeuille d'un même espace YFEN et pour lesquels les données ont été transmises ou rendues accessibles.
- « En un seul endroit » désigne une interface, un portefeuille et des droits d'accès communs. Cela ne signifie pas que YFEN se connecte automatiquement à tous les logiciels, reçoit toutes les données en temps réel ou remplace les systèmes opérationnels.
- Chaque entreprise conserve son identité, ses données, ses sources, sa devise, ses périodes et son historique. La vue portefeuille ne transforme pas à elle seule une somme arithmétique en consolidation comptable.
- Le dirigeant voit le portefeuille complet selon ses droits ; les comptables et responsables de site ne voient que les entités et unités qui leur sont attribuées.

## 2. Principes produit non négociables

1. **Rien sans validation humaine.** Seuls les faits confirmés par un utilisateur autorisé alimentent les indicateurs publiés.
2. **Chaque chiffre a une source.** Un montant doit pouvoir remonter à sa période, son entité, son lot, son fichier, sa règle de transformation et son validateur.
3. **Sobriété radar.** L'interface reste calme. Les exceptions importantes attirent l'attention ; les jauges décoratives, les chiffres non sourcés et le bruit visuel sont exclus.
4. **Décision → action.** Une anomalie exploitable doit conduire à une action datée avec responsable, priorité et échéance.
5. **Précision et concision.** Le dirigeant doit comprendre la situation sans devoir analyser un tableau dense, interpréter un jargon comptable ou configurer des filtres complexes.
6. **Détails progressifs.** Le résumé est immédiat ; le détail, les graphiques, les sources et les lignes importées ne s'ouvrent qu'à la demande.

## 3. Palette officielle

| Nom | Code | Rôle |
| --- | --- | --- |
| Deep Horizon Blue | `#0A192F` | Fond principal : stabilité, confiance et profondeur. |
| Surface | `#112240` | Cartes et surfaces principales. |
| Surface 2 | `#0C1A33` | Surfaces secondaires et panneaux contextuels. |
| Electric Teal | `#00D4AA` | Action principale, validation et état positif confirmé. |
| Teal clair | `#3FE8C5` | Accent secondaire limité. |
| Warm Sand / Or africain | `#E6C288` | Valeur mise en avant, patrimoine et touche humaine. |
| Alert Coral | `#FF6B6B` | Exception, retard, rejet ou anomalie. |
| Horizon Blue | `#5487D9` | Information et visualisation de données. |
| Brume | `#8CA2C0` | Texte secondaire et éléments désactivés. |
| Brume profonde | `#5D7190` | Métadonnées secondaires. |

### Règles d'emploi

- Le fond Horizon domine ; les surfaces structurent les contenus sans multiplier les panneaux.
- Le Teal est réservé aux actions importantes et aux validations positives ; le Corail aux exceptions ; le Sand aux valeurs ou repères premium ; le bleu clair à l'information.
- Une couleur ne doit jamais être le seul moyen de transmettre un statut : ajouter libellé, icône ou texte.
- Pas de palette arc-en-ciel, de dégradés arbitraires, de rotation du logo ou d'ombres portées colorées.
- Les couleurs de séries analytiques doivent rester cohérentes d'un écran à l'autre et ne pas détourner les couleurs sémantiques des alertes.

## 4. Typographie

| Usage | Famille | Règle |
| --- | --- | --- |
| Titres et intitulés d'écrans | Clash Display, 400–700 | Identité forte, hiérarchie courte. |
| Interface, formulaires, descriptions | Inter, 400–700 | Lecture mobile et texte courant ; base indicative 13,5 px, interligne 1,6. |
| Montants, dates, références et preuves | JetBrains Mono, 400–600 | Chiffres alignés et auditables ; jamais en italique. |

Le frontend actuel n'est pas encore totalement aligné sur cette typographie : cette fiche définit la cible, pas un état d'implémentation.

## 5. Logo et composants

- Le monogramme Y-Horizon utilise deux branches teal convergeant vers un point central sombre cerclé de Sand, sur un carré Horizon aux coins adoucis.
- Respecter une zone de protection égale à la moitié de la tige du Y.
- Ne pas utiliser le monogramme sous 20 px ; employer le point radar seul à cette taille.
- Le wordmark est **YFEN.**, en Clash Display 700, avec le point en Sand.
- Les cartes et panneaux utilisent des coins arrondis cohérents (rayon de référence 20 px pour les cartes, 14 px pour les éléments secondaires).
- Les commandes sont explicites, les états visibles et les feuilles contextuelles servent à afficher le détail sans perdre l'écran d'origine.

## 6. Architecture de l'information — toutes les entreprises, un cockpit

| Écran | Question principale | Contenu prioritaire |
| --- | --- | --- |
| **Cockpit** | Que dois-je savoir et traiter maintenant ? | Situation du groupe, quelques indicateurs de tête, exceptions prioritaires, fraîcheur des données et actions urgentes. |
| **Portefeuille** | Quelle entité ou unité mérite mon attention ? | Entreprises et unités opérationnelles, état de mise à jour, indicateurs synthétiques et accès au détail. |
| **Imports** | Les données ont-elles été reçues et contrôlées ? | Quarantaine, aperçu, mapping, anomalies, revue et publication. |
| **Actions** | Qui fait quoi et pour quand ? | Responsable, priorité, échéance, statut et preuve/commentaire. |
| **Analyse** | Quelle évolution ou différence dois-je comprendre ? | Graphiques utiles, comparaisons pertinentes, agrégations et accès à la traçabilité. |
| **Paramètres & accès** | Qui peut voir et faire quoi ? | Membres, rôles, périmètres, préférences FR/EN, notifications et journal d'audit. |

Sur mobile, la navigation principale expose Cockpit, Portefeuille, Actions et Analyse, avec l'import comme action centrale. Paramètres reste accessible depuis l'en-tête. Sur desktop, la même architecture s'adapte en navigation latérale ; elle ne devient pas une autre application.

## 7. Règles de faible charge cognitive

- Le Cockpit est **orienté décision**, pas exploration de données. Il montre au plus quatre indicateurs principaux et trois exceptions prioritaires pour l'ensemble du portefeuille ; le reste est accessible via « Voir tout ».
- Chaque écran répond à une question principale et présente une action dominante.
- Les libellés sont courts, en français courant, sans jargon comptable non expliqué.
- Une variation est toujours accompagnée de sa période de comparaison ; une valeur est accompagnée de sa devise, de sa période et de sa fraîcheur.
- Les graphiques détaillés sont regroupés dans Analyse ; aucun graphique n'est affiché pour décorer.
- Les filtres et paramètres avancés sont masqués derrière une demande de détail ; les valeurs par défaut proviennent du profil du workspace et restent modifiables.
- Les alertes de premier niveau sont réservées aux exceptions qui demandent une décision ou une action. Les simples informations restent discrètes.
- Un écran vide propose une prochaine étape claire, pas une explication technique.
- Le dirigeant consulte et arbitre ; les comptables et gestionnaires de site portent la majorité des tâches d'import et de contrôle.

## 8. Langues, marché et devise

- Français par défaut et anglais sélectionnable dans l'interface dès la cible produit décrite par la maquette.
- Marché initial : Cameroun et zone CEMAC.
- La direction de marque décrit un cockpit initial mono-devise XAF. Tant qu'une politique de change documentée n'est pas implémentée, aucune somme ne mélange XAF, EUR, USD ou d'autres devises. Une donnée d'une autre devise reste explicitement séparée et identifiée.

## 9. Graphiques : règles d'usage

- La vue Cockpit privilégie les indicateurs synthétiques et les exceptions. La page Analyse porte les visualisations détaillées.
- Une visualisation doit répondre à une question : tendance temporelle, comparaison entre entités, répartition ou écart.
- Chaque graphique affiche un titre explicite, une période, une unité/devise et un état de couverture. Les valeurs exactes et les sources restent accessibles.
- Limiter les séries simultanées, éviter les légendes complexes et proposer un tableau ou une liste accessible en alternative.
- Ne pas tracer de données manquantes comme des zéros. Ne pas produire de tendance si les périodes ne sont pas comparables.
- Les graphiques de démonstration et les montants du mockup sont fictifs. Les exemples de marge brute, trésorerie ou « consolidé » ne sont pas des KPI disponibles tant que leurs sources, formules et contrôles ne sont pas implémentés.

## 10. Distinction entre maquette et produit

La maquette décrit la direction visuelle et les parcours cibles. Elle ne prouve ni connexion à l'API, ni exactitude de données réelles, ni disponibilité de toutes les fonctions. Tout KPI, graphique ou état de démonstration doit être remplacé par des données validées ou un état vide explicite avant livraison.

Le fichier `yfen-brand-mockup.html` et les captures de `../screenshots/` constituent la référence visuelle cible. L'ancien fichier `yfen-mockup.html` reste une archive de prototype et ne doit plus guider les nouveaux composants. Les captures du mockup présentent des données fictives et ne prouvent pas que le frontend React est déjà aligné ou connecté à l'API.
