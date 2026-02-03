# 📄 MESSAGES.XML - Documentation Complète

## 📋 Vue d'ensemble

### Informations générales
- **Nom du fichier** : `messages.xml`
- **Rôle** : Configuration des messages automatiques affichés aux joueurs
- **Emplacement** : `mpmissions/[nom_mission]/db/messages.xml`
- **Version DayZ** : 1.28
- **Priorité** : ⭐ FAIBLE (cosmétique, pas critique)
- **Fréquence de modification** : ÉLEVÉE (messages événements, annonces)
- **État vanilla** : Fichier VIDE (exemples en commentaires)

### Impact sur le serveur
- ✅ Affiche des **MESSAGES automatiques** aux joueurs
- ✅ Gère les **ANNONCES** (restarts, règles, liens)
- ✅ Configure les **MESSAGES DE BIENVENUE**
- ✅ Programme des **SHUTDOWNS** automatiques
- ❌ N'affecte PAS le gameplay (purement informatif)

### Redémarrage requis
- ❌ **Pas de restart nécessaire** pour les modifications
- ✅ **Hot-reload** : Messages mis à jour en direct (selon version serveur)

---

## 🏗️ Structure XML

### Structure de base
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<messages>
    <message>
        <!-- Configuration du message -->
    </message>
    <message>
        <!-- Autre message -->
    </message>
</messages>
```

### Structure complète d'un message
```xml
<message>
    <!-- TIMERS (optionnels) -->
    <delay>10</delay>              <!-- Délai avant affichage (minutes) -->
    <repeat>15</repeat>            <!-- Répétition toutes les X minutes -->
    <deadline>600</deadline>       <!-- Compte à rebours (minutes) -->
    
    <!-- TRIGGERS (optionnels) -->
    <onconnect>1</onconnect>       <!-- Affiché à la connexion -->
    <shutdown>1</shutdown>         <!-- Shutdown serveur après deadline -->
    
    <!-- CONTENU (obligatoire) -->
    <text>Votre message ici</text>
</message>
```

---

## 📊 Balises détaillées

### 🔴 BALISE OBLIGATOIRE

#### `<text>`
- **Type** : String (texte)
- **Obligatoire** : ✅ OUI
- **Description** : Le message à afficher aux joueurs
- **Placeholders disponibles** :
  - `#name` → Nom du serveur
  - `#tmin` → Temps restant en minutes (avec deadline)
  - `#tsec` → Temps restant en secondes (avec deadline)

**Exemples :**
```xml
<!-- Message simple -->
<text>Bienvenue sur notre serveur !</text>

<!-- Avec placeholder serveur -->
<text>Vous jouez sur #name</text>

<!-- Avec compte à rebours -->
<text>#name redémarrera dans #tmin minutes</text>
<text>Shutdown dans #tsec secondes !</text>
```

**⚠️ Encodage :**
- UTF-8 pour caractères spéciaux (é, à, ç, etc.)
- Échapper les caractères XML si nécessaire (`&amp;`, `&lt;`, `&gt;`)

---

### 🟡 BALISES OPTIONNELLES (Timers)

#### `<delay>`
- **Type** : Integer (minutes)
- **Obligatoire** : ❌ NON
- **Description** : Délai AVANT le premier affichage du message
- **Usage** : Attendre X minutes après le démarrage du serveur ou la connexion du joueur

**Exemples :**
```xml
<!-- Afficher 10 minutes après connexion -->
<message>
    <delay>10</delay>
    <onconnect>1</onconnect>
    <text>N'oubliez pas de rejoindre notre Discord !</text>
</message>

<!-- Afficher 5 minutes après démarrage serveur -->
<message>
    <delay>5</delay>
    <text>Serveur stable, bon jeu à tous !</text>
</message>
```

**Logique :**
- Avec `<onconnect>1</onconnect>` → Délai après connexion joueur
- Sans onconnect → Délai après démarrage serveur

---

#### `<repeat>`
- **Type** : Integer (minutes)
- **Obligatoire** : ❌ NON
- **Description** : Répète le message toutes les X minutes
- **Usage** : Messages récurrents (règles, liens, astuces)

**Exemples :**
```xml
<!-- Message toutes les 30 minutes -->
<message>
    <repeat>30</repeat>
    <text>Consultez les règles : www.monserveur.com/regles</text>
</message>

<!-- Message toutes les heures -->
<message>
    <repeat>60</repeat>
    <text>Pensez à boire de l'eau et à manger !</text>
</message>
```

**⚠️ Sans repeat :**
- Le message s'affiche UNE SEULE FOIS

---

#### `<deadline>`
- **Type** : Integer (minutes)
- **Obligatoire** : ❌ NON
- **Description** : Compte à rebours jusqu'à un événement (souvent restart/shutdown)
- **Usage** : Avertir les joueurs d'un restart programmé

**Comportement :**
- Le message s'affiche avec un **compte à rebours décroissant**
- Utilise les placeholders `#tmin` et `#tsec`
- Répété automatiquement jusqu'à atteindre 0

**Exemples :**
```xml
<!-- Shutdown dans 10 heures (600 minutes) -->
<message>
    <deadline>600</deadline>
    <shutdown>1</shutdown>
    <text>#name redémarrera dans #tmin minutes</text>
</message>

<!-- Événement dans 2 heures (sans shutdown) -->
<message>
    <deadline>120</deadline>
    <text>Événement PvP dans #tmin minutes !</text>
</message>
```

**Fréquence d'affichage :**
- Plus le deadline approche, plus le message est fréquent
- Ex: 1h avant = toutes les 10min, 10min avant = toutes les 2min, 1min avant = toutes les 10s

---

### 🟡 BALISES OPTIONNELLES (Triggers)

#### `<onconnect>`
- **Type** : Boolean (0 ou 1)
- **Obligatoire** : ❌ NON
- **Valeur par défaut** : 0
- **Description** : Déclenche le message à la **connexion du joueur**
- **Usage** : Messages de bienvenue, règles initiales

**Exemples :**
```xml
<!-- Message immédiat à la connexion -->
<message>
    <onconnect>1</onconnect>
    <text>Bienvenue sur #name !</text>
</message>

<!-- Message 5 min après connexion -->
<message>
    <delay>5</delay>
    <onconnect>1</onconnect>
    <text>Pensez à lire les règles sur notre Discord</text>
</message>

<!-- Message à la connexion puis répété -->
<message>
    <onconnect>1</onconnect>
    <repeat>30</repeat>
    <text>Serveur modé - Liste des mods : www.exemple.com</text>
</message>
```

**Logique :**
- `onconnect="1"` → Déclenché par connexion joueur
- `onconnect="0"` ou absent → Déclenché par timer serveur

---

#### `<shutdown>`
- **Type** : Boolean (0 ou 1)
- **Obligatoire** : ❌ NON
- **Valeur par défaut** : 0
- **Description** : **ARRÊTE LE SERVEUR** quand le deadline atteint 0
- **Usage** : Restarts automatiques programmés

**⚠️ ATTENTION : Cette balise SHUTDOWN le serveur !**

**Exemples :**
```xml
<!-- Shutdown automatique dans 12h -->
<message>
    <deadline>720</deadline>
    <shutdown>1</shutdown>
    <text>#name redémarrera dans #tmin minutes pour maintenance</text>
</message>

<!-- Countdown sans shutdown (juste info) -->
<message>
    <deadline>120</deadline>
    <text>Événement dans #tmin minutes !</text>
    <!-- PAS de <shutdown> = serveur continue -->
</message>
```

**Fonctionnement :**
- Quand deadline atteint 0 ET `shutdown="1"` → Serveur s'arrête
- Sans `shutdown` → Juste un compte à rebours informatif

---

## 💡 Exemples complets commentés

### Exemple 1 : Message de bienvenue simple
```xml
<message>
    <onconnect>1</onconnect>
    <text>Bienvenue sur #name ! Bon jeu !</text>
</message>
```
**Résultat :** Message immédiat à chaque connexion

---

### Exemple 2 : Règles affichées après 2 minutes
```xml
<message>
    <delay>2</delay>
    <onconnect>1</onconnect>
    <text>📜 Règles du serveur : Pas de KOS en zone safe, respect des bases, teamplay encouragé</text>
</message>
```
**Résultat :** Message 2 minutes après connexion, UNE SEULE FOIS

---

### Exemple 3 : Rappel Discord toutes les 30 minutes
```xml
<message>
    <repeat>30</repeat>
    <text>💬 Rejoignez notre Discord : discord.gg/ABCD1234</text>
</message>
```
**Résultat :** Message répété toutes les 30 minutes à TOUS les joueurs

---

### Exemple 4 : Message de bienvenue + rappel périodique
```xml
<message>
    <delay>5</delay>
    <repeat>60</repeat>
    <onconnect>1</onconnect>
    <text>🌐 Site web : www.monserveur.com | Discord : discord.gg/XYZ</text>
</message>
```
**Résultat :** 
- À la connexion : message après 5 minutes
- Puis répété toutes les 60 minutes

---

### Exemple 5 : Restart automatique programmé
```xml
<message>
    <deadline>720</deadline>
    <shutdown>1</shutdown>
    <text>⚠️ #name redémarrera dans #tmin minutes pour maintenance !</text>
</message>
```
**Résultat :**
- Compte à rebours de 12 heures (720 min)
- Affichage répété avec temps restant
- **SHUTDOWN automatique** à la fin

---

### Exemple 6 : Événement programmé (sans shutdown)
```xml
<message>
    <deadline>120</deadline>
    <text>🎮 ÉVÉNEMENT PvP dans #tmin minutes au NEAF !</text>
</message>
```
**Résultat :**
- Compte à rebours de 2 heures
- Pas de shutdown (juste info)

---

### Exemple 7 : Conseils de survie répétés
```xml
<message>
    <repeat>45</repeat>
    <text>💡 Astuce : Purifiez l'eau avant de la boire avec des pastilles de chlore !</text>
</message>

<message>
    <repeat>45</repeat>
    <text>💡 Astuce : La viande crue peut vous rendre malade, cuisinez-la avant !</text>
</message>
```
**Résultat :** Rotation d'astuces toutes les 45 minutes

---

### Exemple 8 : Multi-messages pour nouveaux joueurs
```xml
<!-- Message immédiat -->
<message>
    <onconnect>1</onconnect>
    <text>👋 Bienvenue sur #name !</text>
</message>

<!-- Message après 2 min -->
<message>
    <delay>2</delay>
    <onconnect>1</onconnect>
    <text>📜 Lis les règles avec /rules</text>
</message>

<!-- Message après 10 min -->
<message>
    <delay>10</delay>
    <onconnect>1</onconnect>
    <text>💬 Besoin d'aide ? Rejoins notre Discord !</text>
</message>
```
**Résultat :** Séquence de bienvenue étalée dans le temps

---

## 🎯 Configurations par type de serveur

### 🎮 Serveur Vanilla Minimal
```xml
<messages>
    <!-- Bienvenue -->
    <message>
        <onconnect>1</onconnect>
        <text>Bienvenue sur #name !</text>
    </message>
    
    <!-- Restart automatique tous les jours -->
    <message>
        <deadline>1440</deadline>
        <shutdown>1</shutdown>
        <text>#name redémarrera dans #tmin minutes</text>
    </message>
</messages>
```

---

### 🏕️ Serveur RP avec règles
```xml
<messages>
    <!-- Bienvenue -->
    <message>
        <onconnect>1</onconnect>
        <text>🎭 Bienvenue sur #name - Serveur RP</text>
    </message>
    
    <!-- Règles après 2 min -->
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>📜 RÈGLES : Pas de KOS, RP obligatoire, micro recommandé</text>
    </message>
    
    <!-- Discord répété -->
    <message>
        <repeat>30</repeat>
        <text>💬 Discord : discord.gg/MONSERVEUR</text>
    </message>
    
    <!-- Restart 2x par jour -->
    <message>
        <deadline>720</deadline>
        <shutdown>1</shutdown>
        <text>⚠️ Restart dans #tmin minutes</text>
    </message>
</messages>
```

---

### 🔫 Serveur PvP compétitif
```xml
<messages>
    <!-- Bienvenue agressive -->
    <message>
        <onconnect>1</onconnect>
        <text>⚔️ Bienvenue sur #name - PvP Full Loot</text>
    </message>
    
    <!-- Règles PvP -->
    <message>
        <delay>1</delay>
        <onconnect>1</onconnect>
        <text>🔥 Zone safe : Trader uniquement | KOS autorisé partout ailleurs</text>
    </message>
    
    <!-- Stats serveur -->
    <message>
        <repeat>20</repeat>
        <text>📊 Stats : www.monserveur.com/stats</text>
    </message>
    
    <!-- Événements -->
    <message>
        <repeat>60</repeat>
        <text>🎯 Événement Airdrop toutes les 3h !</text>
    </message>
</messages>
```

---

### 🌍 Serveur communautaire actif
```xml
<messages>
    <!-- Bienvenue -->
    <message>
        <onconnect>1</onconnect>
        <text>👋 Bienvenue sur #name</text>
    </message>
    
    <!-- Discord -->
    <message>
        <delay>3</delay>
        <onconnect>1</onconnect>
        <text>💬 Discord obligatoire : discord.gg/EXAMPLE</text>
    </message>
    
    <!-- Site web -->
    <message>
        <repeat>45</repeat>
        <text>🌐 Site : www.monserveur.com | Boutique : shop.monserveur.com</text>
    </message>
    
    <!-- Donations -->
    <message>
        <repeat>90</repeat>
        <text>❤️ Soutenez le serveur : www.monserveur.com/donate</text>
    </message>
    
    <!-- Règles -->
    <message>
        <repeat>60</repeat>
        <text>📜 Règles complètes : www.monserveur.com/rules</text>
    </message>
    
    <!-- Restart programmé -->
    <message>
        <deadline>360</deadline>
        <shutdown>1</shutdown>
        <text>🔄 Restart automatique dans #tmin minutes</text>
    </message>
</messages>
```

---

## ⚠️ Règles de validation

### Règle 1 : Balise <text> obligatoire
```xml
<!-- ❌ ERREUR - Pas de texte -->
<message>
    <repeat>30</repeat>
</message>

<!-- ✅ CORRECT -->
<message>
    <repeat>30</repeat>
    <text>Message ici</text>
</message>
```

---

### Règle 2 : Valeurs numériques positives
```xml
<!-- ❌ ERREUR -->
<message>
    <delay>-10</delay>
    <text>Test</text>
</message>

<!-- ✅ CORRECT -->
<message>
    <delay>10</delay>
    <text>Test</text>
</message>
```

---

### Règle 3 : onconnect et shutdown sont 0 ou 1
```xml
<!-- ❌ ERREUR -->
<message>
    <onconnect>yes</onconnect>
    <shutdown>true</shutdown>
    <text>Test</text>
</message>

<!-- ✅ CORRECT -->
<message>
    <onconnect>1</onconnect>
    <shutdown>1</shutdown>
    <text>Test</text>
</message>
```

---

### Règle 4 : deadline nécessite shutdown explicite
```xml
<!-- ⚠️ AMBIGU - Shutdown ou pas ? -->
<message>
    <deadline>720</deadline>
    <text>#name restart dans #tmin min</text>
</message>

<!-- ✅ CLAIR - Shutdown explicite -->
<message>
    <deadline>720</deadline>
    <shutdown>1</shutdown>
    <text>Restart dans #tmin min</text>
</message>

<!-- ✅ CLAIR - Juste info, pas de shutdown -->
<message>
    <deadline>120</deadline>
    <text>Événement dans #tmin min</text>
</message>
```

---

## 🎨 Bonnes pratiques

### ✅ Faire :

1. **Encodage UTF-8** pour les accents
```xml
<text>Bienvenue sur notre serveur français !</text>
```

2. **Messages courts et clairs** (< 100 caractères)
```xml
<text>Rejoignez notre Discord : discord.gg/ABC123</text>
```

3. **Espacement des messages répétés** (> 15 minutes)
```xml
<repeat>30</repeat>  <!-- Bon -->
```

4. **Séquence de bienvenue progressive**
```xml
<!-- Immédiat -->
<message><onconnect>1</onconnect><text>Bienvenue !</text></message>
<!-- Après 2 min -->
<message><delay>2</delay><onconnect>1</onconnect><text>Règles...</text></message>
<!-- Après 10 min -->
<message><delay>10</delay><onconnect>1</onconnect><text>Discord...</text></message>
```

5. **Prévoir des restarts automatiques**
```xml
<message>
    <deadline>1440</deadline>  <!-- 24h -->
    <shutdown>1</shutdown>
    <text>Restart quotidien dans #tmin min</text>
</message>
```

---

### ❌ Éviter :

1. **Spam de messages** (< 10 minutes)
```xml
<!-- ❌ SPAM -->
<repeat>5</repeat>
```

2. **Messages trop longs** (> 200 caractères)
```xml
<!-- ❌ TROP LONG -->
<text>Bienvenue sur notre serveur qui est le meilleur serveur DayZ de France avec plein de mods géniaux et une communauté super active venez nous rejoindre sur Discord...</text>
```

3. **Trop de messages simultanés**
```xml
<!-- ❌ Overload - 10+ messages répétés -->
```

4. **Placeholders sans deadline**
```xml
<!-- ❌ ERREUR - #tmin sans deadline -->
<message>
    <text>Restart dans #tmin minutes</text>
</message>
```

---

## 🔍 Erreurs courantes et solutions

### Erreur 1 : Messages n'apparaissent pas
**Causes possibles :**
- Syntaxe XML invalide
- Fichier mal encodé (pas UTF-8)
- Balises mal fermées

**Solution :**
- Valider la syntaxe XML
- Sauvegarder en UTF-8
- Vérifier toutes les balises `<message>...</message>`

---

### Erreur 2 : Serveur ne shutdown pas
**Cause :** `<shutdown>1</shutdown>` manquant

**Solution :**
```xml
<message>
    <deadline>720</deadline>
    <shutdown>1</shutdown>  <!-- ⬅️ NÉCESSAIRE -->
    <text>Restart dans #tmin min</text>
</message>
```

---

### Erreur 3 : Messages spamment les joueurs
**Cause :** `<repeat>` trop court

**Solution :**
```xml
<!-- ❌ AVANT (spam) -->
<repeat>2</repeat>

<!-- ✅ APRÈS (raisonnable) -->
<repeat>30</repeat>
```

---

### Erreur 4 : Accents cassés
**Cause :** Encodage incorrect

**Solution :**
- Sauvegarder le fichier en **UTF-8**
- Vérifier `encoding="UTF-8"` dans la première ligne

---

## 📊 Placeholders disponibles

| Placeholder | Description | Exemple |
|-------------|-------------|---------|
| `#name` | Nom du serveur | "Mon Serveur DayZ" |
| `#tmin` | Temps en minutes (avec deadline) | "120" |
| `#tsec` | Temps en secondes (avec deadline) | "45" |

**Exemples d'utilisation :**
```xml
<text>Bienvenue sur #name !</text>
<!-- Affiche : Bienvenue sur Mon Serveur DayZ ! -->

<text>#name restart dans #tmin minutes</text>
<!-- Affiche : Mon Serveur DayZ restart dans 120 minutes -->

<text>Shutdown dans #tsec secondes !</text>
<!-- Affiche : Shutdown dans 45 secondes ! -->
```

---

## ✅ Checklist de validation Codex

### Syntaxe XML
- [ ] Fichier commence par `<?xml version="1.0" encoding="UTF-8"?>`
- [ ] Balise racine `<messages>` présente
- [ ] Toutes les balises `<message>` fermées
- [ ] Commentaires entre `<!-- -->` si présents

### Structure des messages
- [ ] Chaque `<message>` contient au moins `<text>`
- [ ] Balises optionnelles correctement placées
- [ ] Pas de balises inconnues

### Valeurs
- [ ] `delay`, `repeat`, `deadline` sont des entiers positifs
- [ ] `onconnect` et `shutdown` sont 0 ou 1
- [ ] Placeholders `#name`, `#tmin`, `#tsec` correctement utilisés

### Cohérence
- [ ] `deadline` utilisé avec ou sans `shutdown` selon besoin
- [ ] Messages répétés espacés (> 15 minutes recommandé)
- [ ] Pas trop de messages (< 10 recommandé)

---

## 📝 Template de base prêt à l'emploi

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<messages>
    
    <!-- MESSAGE DE BIENVENUE -->
    <message>
        <onconnect>1</onconnect>
        <text>👋 Bienvenue sur #name !</text>
    </message>
    
    <!-- RÈGLES (2 min après connexion) -->
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>📜 Règles : www.votresite.com/regles</text>
    </message>
    
    <!-- DISCORD (répété toutes les 30 min) -->
    <message>
        <repeat>30</repeat>
        <text>💬 Discord : discord.gg/VOTRECODE</text>
    </message>
    
    <!-- RESTART AUTOMATIQUE (toutes les 24h) -->
    <message>
        <deadline>1440</deadline>
        <shutdown>1</shutdown>
        <text>⚠️ #name redémarrera dans #tmin minutes</text>
    </message>
    
</messages>
```

---

**📝 Document créé par CodeX - L'outil pour la communauté DayZ FR**
**Version : 1.0 - Basé sur DayZ 1.28**
**Dernière mise à jour : 2025**
