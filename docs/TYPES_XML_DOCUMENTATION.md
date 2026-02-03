# 📄 TYPES.XML - Documentation Complète

## 📋 Vue d'ensemble

### Informations générales
- **Nom du fichier** : `types.xml`
- **Rôle** : Gestion des spawns et respawns de tous les items du jeu
- **Emplacement** : `mpmissions/[nom_mission]/db/types.xml`
- **Version DayZ** : 1.28 (Chernarus)
- **Priorité** : ⭐⭐⭐ CRITIQUE
- **Fréquence de modification** : TRÈS ÉLEVÉE (fichier le plus modifié)
- **Nombre d'items** : 1917 items dans la version vanilla Chernarus

### Impact sur le serveur
- ✅ Contrôle TOUS les spawns d'items (armes, vêtements, nourriture, outils, etc.)
- ✅ Détermine la rareté de chaque item
- ✅ Gère l'économie globale du serveur
- ✅ Affecte directement l'expérience de jeu

### Redémarrage requis
- ❌ Modifications prises en compte au **prochain restart** du serveur
- ⚠️ Pas de hot-reload possible

---

## 🏗️ Structure XML

### Structure racine
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<types>
    <type name="NomDeLItem">
        <!-- Configuration de l'item -->
    </type>
    <type name="AutreItem">
        <!-- Configuration de l'item -->
    </type>
    <!-- ... 1917 items au total ... -->
</types>
```

### Structure d'un élément `<type>`

```xml
<type name="AK74">
    <!-- SPAWN CONTROL -->
    <nominal>6</nominal>              <!-- Nombre cible sur la map -->
    <lifetime>28800</lifetime>        <!-- Durée de vie en secondes -->
    <restock>0</restock>              <!-- Temps avant respawn -->
    <min>4</min>                      <!-- Nombre minimum garanti -->
    
    <!-- QUANTITY (pour items stackables) -->
    <quantmin>30</quantmin>           <!-- Quantité minimum au spawn -->
    <quantmax>80</quantmax>           <!-- Quantité maximum au spawn -->
    
    <!-- ECONOMY -->
    <cost>100</cost>                  <!-- Coût économique (0-100) -->
    
    <!-- FLAGS -->
    <flags 
        count_in_cargo="0"            <!-- Compter dans les véhicules -->
        count_in_hoarder="0"          <!-- Compter dans les planques -->
        count_in_map="1"              <!-- Compter sur la map -->
        count_in_player="0"           <!-- Compter sur les joueurs -->
        crafted="0"                   <!-- Item craftable -->
        deloot="0"                    <!-- Peut être del par cleanup -->
    />
    
    <!-- CATEGORIZATION -->
    <category name="weapons"/>        <!-- Catégorie de l'item -->
    
    <!-- SPAWN LOCATIONS (multiples possibles) -->
    <usage name="Military"/>          <!-- Zone de spawn -->
    <usage name="Police"/>            <!-- Zone de spawn -->
    
    <!-- TIER SYSTEM (multiples possibles) -->
    <value name="Tier3"/>             <!-- Niveau de rareté -->
    <value name="Tier4"/>             <!-- Niveau de rareté -->
    
    <!-- TAGS (optionnels) -->
    <tag name="shelves"/>             <!-- Tag de spawn spécifique -->
</type>
```

---

## 📊 Balises détaillées

### 🔴 BALISES OBLIGATOIRES

#### `name` (attribut de `<type>`)
- **Type** : String (texte)
- **Obligatoire** : ✅ OUI
- **Description** : Nom technique de l'item (classname DayZ)
- **Format** : Sensible à la casse, pas d'espaces
- **Exemples** : 
  - ✅ `AK74`, `M4A1`, `PeachesCan`, `TShirt_White`
  - ❌ `AK 74`, `ak74` (si le nom exact est AK74)

---

#### `<nominal>`
- **Type** : Integer (nombre entier)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 10000+ (recommandé : 0-1000)
- **Description** : Nombre cible d'items de ce type sur toute la map
- **Règle métier** : `nominal` doit être ≥ `min`
- **Comportement** :
  - Si nominal = 0 → Item désactivé (ne spawn plus)
  - Si nominal = 1 → Item ultra rare (1 seul exemplaire)
  - Si nominal = 100 → 100 exemplaires répartis sur la map

**Exemples :**
```xml
<nominal>0</nominal>     <!-- Item désactivé -->
<nominal>1</nominal>     <!-- Item unique (ex: hélico) -->
<nominal>10</nominal>    <!-- Rare (ex: SVD) -->
<nominal>50</nominal>    <!-- Moyen (ex: AK74) -->
<nominal>200</nominal>   <!-- Commun (ex: Pommes) -->
```

---

#### `<lifetime>`
- **Type** : Integer (secondes)
- **Obligatoire** : ✅ OUI
- **Plage** : 1 à 86400 (1 seconde à 24h)
- **Description** : Durée de vie de l'item avant despawn automatique
- **Valeurs courantes** :
  - 3600 = 1 heure
  - 7200 = 2 heures
  - 14400 = 4 heures
  - 28800 = 8 heures
  - 86400 = 24 heures

**Exemples :**
```xml
<lifetime>3600</lifetime>    <!-- Nourriture périssable -->
<lifetime>14400</lifetime>   <!-- Attachements d'armes -->
<lifetime>28800</lifetime>   <!-- Armes -->
<lifetime>86400</lifetime>   <!-- Items rares/précieux -->
```

**⚠️ Attention :**
- Un lifetime trop court = items disparaissent trop vite
- Un lifetime trop long = saturation de la map

---

#### `<restock>`
- **Type** : Integer (secondes)
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 86400
- **Description** : Temps minimum avant qu'un nouvel item de ce type puisse spawn
- **Valeur spéciale** : 0 = respawn immédiat si sous le nominal

**Exemples :**
```xml
<restock>0</restock>       <!-- Respawn immédiat (nourriture, munitions) -->
<restock>1800</restock>    <!-- 30 minutes (armes communes) -->
<restock>3600</restock>    <!-- 1 heure (armes rares) -->
```

**Stratégie :**
- restock = 0 → Items courants qui doivent toujours être dispo
- restock élevé → Items rares avec respawn contrôlé

---

#### `<min>`
- **Type** : Integer
- **Obligatoire** : ✅ OUI
- **Plage** : 0 à 10000
- **Description** : Nombre MINIMUM garanti d'items de ce type sur la map
- **Règle métier** : `min` doit être ≤ `nominal`
- **Comportement** : Si le nombre d'items descend sous `min`, le système force un respawn

**Exemples :**
```xml
<nominal>10</nominal>
<min>5</min>      <!-- Au moins 5 exemplaires garantis -->
```

**Cas d'usage :**
```xml
<!-- Item complètement désactivé -->
<nominal>0</nominal>
<min>0</min>

<!-- Item ultra rare mais garanti -->
<nominal>3</nominal>
<min>2</min>

<!-- Item commun toujours disponible -->
<nominal>100</nominal>
<min>80</min>
```

---

### 🟡 BALISES OPTIONNELLES (mais courantes)

#### `<quantmin>` et `<quantmax>`
- **Type** : Integer
- **Obligatoire** : ❌ NON (mais très courant)
- **Plage** : -1 à 100
- **Description** : Quantité/charge de l'item au spawn
- **Valeur spéciale** : -1 = Non applicable (item non stackable)

**Application selon le type d'item :**

**Items stackables (munitions, bandages, etc.) :**
```xml
<quantmin>10</quantmin>
<quantmax>30</quantmax>
<!-- Spawn entre 10 et 30 munitions -->
```

**Armes (pourcentage de durabilité) :**
```xml
<quantmin>30</quantmin>
<quantmax>80</quantmax>
<!-- Spawn entre 30% et 80% de durabilité -->
```

**Items non concernés (vêtements, outils simples) :**
```xml
<quantmin>-1</quantmin>
<quantmax>-1</quantmax>
<!-- Pas de notion de quantité -->
```

**Conteneurs (nombre de slots utilisés) :**
```xml
<quantmin>0</quantmin>
<quantmax>50</quantmax>
<!-- Spawn avec 0 à 50% de slots remplis -->
```

---

#### `<cost>`
- **Type** : Integer
- **Obligatoire** : ❌ NON
- **Plage** : 0 à 100
- **Description** : "Coût" économique de l'item (impact sur l'économie globale)
- **Valeur par défaut** : 100 (si non spécifié)
- **Utilisation** : Système interne de DayZ, peu utilisé par les admins

**Exemples :**
```xml
<cost>10</cost>    <!-- Item commun, faible impact -->
<cost>100</cost>   <!-- Item précieux, fort impact -->
```

---

#### `<flags>` (attributs multiples)
- **Type** : Boolean (0 ou 1)
- **Obligatoire** : ❌ NON
- **Description** : Drapeaux de comportement de l'item

**Attributs disponibles :**

**`count_in_cargo`** (0 ou 1)
- 0 = Items dans les véhicules/containers ne comptent PAS dans le nominal
- 1 = Items dans les véhicules/containers comptent dans le nominal
- **Recommandé** : 0 (sinon risque de bloquer les spawns)

**`count_in_hoarder`** (0 ou 1)
- 0 = Items dans les bases/planques ne comptent PAS
- 1 = Items dans les bases/planques comptent
- **Recommandé** : 0 (pour éviter le hoarding)

**`count_in_map`** (0 ou 1)
- 0 = Items au sol ne comptent PAS
- 1 = Items au sol comptent dans le nominal
- **Recommandé** : 1 (toujours)

**`count_in_player`** (0 ou 1)
- 0 = Items sur les joueurs ne comptent PAS
- 1 = Items sur les joueurs comptent
- **Recommandé** : 0 (pour la fluidité)

**`crafted`** (0 ou 1)
- 0 = Item spawn naturellement
- 1 = Item obtenu UNIQUEMENT par craft
- **Usage** : Variantes craftées d'armes (spray paint)

**`deloot`** (0 ou 1)
- 0 = Item jamais supprimé par le cleanup
- 1 = Item peut être supprimé par le cleanup si conditions réunies
- **Usage** : Items temporaires, événements

**Configuration typique :**
```xml
<!-- Configuration standard (la plus courante) -->
<flags 
    count_in_cargo="0" 
    count_in_hoarder="0" 
    count_in_map="1" 
    count_in_player="0" 
    crafted="0" 
    deloot="0"
/>

<!-- Item craftable uniquement -->
<flags 
    count_in_cargo="0" 
    count_in_hoarder="0" 
    count_in_map="1" 
    count_in_player="0" 
    crafted="1" 
    deloot="0"
/>

<!-- Item d'event temporaire -->
<flags 
    count_in_cargo="0" 
    count_in_hoarder="0" 
    count_in_map="1" 
    count_in_player="0" 
    crafted="0" 
    deloot="1"
/>
```

---

#### `<category>`
- **Type** : Enum (liste fixe)
- **Obligatoire** : ❌ NON (mais recommandé)
- **Quantité** : 1 seule category par item
- **Description** : Catégorie fonctionnelle de l'item

**Valeurs autorisées :**
- `weapons` - Armes et accessoires
- `clothes` - Vêtements et équipement vestimentaire
- `food` - Nourriture et boissons
- `tools` - Outils et objets utilitaires
- `containers` - Sacs, caisses, conteneurs
- `explosives` - Explosifs et grenades

**Exemples :**
```xml
<category name="weapons"/>      <!-- AK74, M4A1, Mosin -->
<category name="clothes"/>      <!-- TShirt, Jeans, Boots -->
<category name="food"/>         <!-- Peaches, Rice, Water -->
<category name="tools"/>        <!-- Axe, Knife, Rope -->
<category name="containers"/>   <!-- Backpack, Barrel -->
<category name="explosives"/>   <!-- Grenade, Landmine -->
```

---

#### `<usage>` (peut être multiple)
- **Type** : Enum (liste fixe)
- **Obligatoire** : ❌ NON
- **Quantité** : 0 à plusieurs par item
- **Description** : Zones géographiques où l'item peut spawn

**Valeurs autorisées :**

**Zones urbaines :**
- `Town` - Villes moyennes
- `Village` - Petits villages
- `Coast` - Zones côtières

**Zones spécialisées :**
- `Military` - Bases militaires, checkpoints
- `Police` - Postes de police
- `Firefighter` - Casernes de pompiers
- `Medic` - Hôpitaux, cliniques
- `Office` - Bureaux
- `School` - Écoles

**Zones rurales :**
- `Farm` - Fermes
- `Hunting` - Zones de chasse
- `Industrial` - Zones industrielles

**Zones spéciales :**
- `Prison` - Prison
- `ContaminatedArea` - Zones toxiques
- `Historical` - Sites historiques
- `Lunapark` - Parc d'attractions
- `SeasonalEvent` - Événements saisonniers

**Exemples d'utilisation :**

```xml
<!-- Item militaire pur -->
<usage name="Military"/>

<!-- Item mixte (police + militaire) -->
<usage name="Military"/>
<usage name="Police"/>

<!-- Item civil répandu -->
<usage name="Town"/>
<usage name="Village"/>
<usage name="Farm"/>

<!-- Item de contamination -->
<usage name="ContaminatedArea"/>
```

**⚠️ Pas de `<usage>` = Item ne spawn PAS naturellement**
```xml
<!-- Cet item NE SPAWNERA PAS car pas de <usage> -->
<type name="ItemCrafté">
    <nominal>0</nominal>
    <!-- ... -->
    <flags crafted="1" />
    <!-- PAS de <usage> -->
</type>
```

---

#### `<value>` (peut être multiple)
- **Type** : Enum (liste fixe)
- **Obligatoire** : ❌ NON
- **Quantité** : 0 à plusieurs par item
- **Description** : Niveau de rareté / tier de l'item

**Valeurs autorisées :**
- `Tier1` - Très commun (côte, villages)
- `Tier2` - Commun (villes)
- `Tier3` - Rare (bases militaires secondaires)
- `Tier4` - Très rare (grandes bases militaires)

**Système de tiers DayZ :**
```
Tier1 (Côte/Villages)
  ↓
Tier2 (Villes moyennes)
  ↓
Tier3 (Bases secondaires)
  ↓
Tier4 (Grandes bases/NWAF)
```

**Exemples :**

```xml
<!-- Item côtier uniquement -->
<value name="Tier1"/>

<!-- Item des villes -->
<value name="Tier2"/>

<!-- Item militaire rare (Tier 3 ET 4) -->
<value name="Tier3"/>
<value name="Tier4"/>
```

**Item sans `<value>` :**
- Spawn dans TOUTES les zones correspondant aux `<usage>`
- Pas de restriction par tier

---

#### `<tag>` (peut être multiple)
- **Type** : Enum (liste fixe)
- **Obligatoire** : ❌ NON
- **Quantité** : 0 à plusieurs par item
- **Description** : Tags spécifiques de spawn (emplacements précis)

**Valeurs autorisées :**
- `shelves` - Étagères
- `floor` - Au sol
- `lootdispatch` - Distribution spéciale
- (Autres tags selon mods/extensions)

**Exemples :**
```xml
<!-- Item qui spawn sur les étagères -->
<tag name="shelves"/>

<!-- Item qui spawn au sol -->
<tag name="floor"/>
```

**Usage rare** : Principalement utilisé pour des configs avancées ou des mods.

---

## ⚠️ Règles métier et validations

### Règles de cohérence des valeurs

#### Règle 1 : `min` ≤ `nominal`
```xml
<!-- ✅ CORRECT -->
<nominal>10</nominal>
<min>5</min>

<!-- ❌ ERREUR -->
<nominal>5</nominal>
<min>10</min>  <!-- min > nominal = INVALIDE -->
```

---

#### Règle 2 : `quantmin` ≤ `quantmax`
```xml
<!-- ✅ CORRECT -->
<quantmin>10</quantmin>
<quantmax>30</quantmax>

<!-- ❌ ERREUR -->
<quantmin>50</quantmin>
<quantmax>20</quantmax>  <!-- quantmin > quantmax = INVALIDE -->
```

---

#### Règle 3 : `lifetime` > 0
```xml
<!-- ✅ CORRECT -->
<lifetime>3600</lifetime>

<!-- ❌ ERREUR -->
<lifetime>0</lifetime>  <!-- lifetime = 0 = INVALIDE -->
<lifetime>-100</lifetime>  <!-- lifetime négatif = INVALIDE -->
```

---

#### Règle 4 : `cost` entre 0 et 100
```xml
<!-- ✅ CORRECT -->
<cost>50</cost>

<!-- ❌ ERREUR -->
<cost>150</cost>  <!-- > 100 = INVALIDE -->
<cost>-10</cost>  <!-- négatif = INVALIDE -->
```

---

#### Règle 5 : Flags doivent être 0 ou 1
```xml
<!-- ✅ CORRECT -->
<flags count_in_cargo="0" count_in_map="1" />

<!-- ❌ ERREUR -->
<flags count_in_cargo="2" />  <!-- Valeur autre que 0/1 = INVALIDE -->
<flags count_in_cargo="true" />  <!-- Texte au lieu de nombre = INVALIDE -->
```

---

### Règles de cohérence logique

#### Règle 6 : Item désactivé correctement
```xml
<!-- ✅ CORRECT - Item totalement désactivé -->
<nominal>0</nominal>
<min>0</min>
<restock>0</restock>

<!-- ⚠️ INCOHÉRENT - Item avec nominal=0 mais min>0 -->
<nominal>0</nominal>
<min>5</min>  <!-- Impossible à atteindre -->
```

---

#### Règle 7 : Item craftable sans usage
```xml
<!-- ✅ CORRECT - Item craftable uniquement -->
<nominal>0</nominal>
<flags crafted="1" />
<!-- PAS de <usage> -->

<!-- ⚠️ INCOHÉRENT - Item craftable qui spawn quand même -->
<nominal>10</nominal>
<flags crafted="1" />
<usage name="Military"/>  <!-- Incohérent : spawn OU craft ? -->
```

---

#### Règle 8 : Catégorie cohérente avec usage
```xml
<!-- ✅ CORRECT -->
<category name="weapons"/>
<usage name="Military"/>

<!-- ⚠️ BIZARRE (mais techniquement valide) -->
<category name="weapons"/>
<usage name="Medic"/>  <!-- Arme à l'hôpital ? Étrange mais possible -->
```

---

## 💡 Exemples complets commentés

### Exemple 1 : Arme militaire rare (SVD)
```xml
<type name="SVD">
    <nominal>2</nominal>              <!-- Seulement 2 sur toute la map -->
    <lifetime>28800</lifetime>        <!-- 8h de durée de vie -->
    <restock>3600</restock>           <!-- 1h avant respawn possible -->
    <min>1</min>                      <!-- Au moins 1 garanti -->
    <quantmin>30</quantmin>           <!-- Durabilité 30-80% -->
    <quantmax>80</quantmax>
    <cost>100</cost>                  <!-- Coût élevé -->
    <flags 
        count_in_cargo="0" 
        count_in_hoarder="0" 
        count_in_map="1" 
        count_in_player="0" 
        crafted="0" 
        deloot="1"                    <!-- Peut être cleanup si besoin -->
    />
    <category name="weapons"/>
    <usage name="Military"/>          <!-- Spawn uniquement zones militaires -->
    <value name="Tier4"/>             <!-- Tier max uniquement (NWAF, Tisy) -->
</type>
```

**Résultat :** Arme ultra rare, spawn uniquement dans les grandes bases militaires.

---

### Exemple 2 : Nourriture commune (Peach)
```xml
<type name="PeachesCan">
    <nominal>80</nominal>             <!-- 80 exemplaires sur la map -->
    <lifetime>3600</lifetime>         <!-- 1h (nourriture périssable) -->
    <restock>0</restock>              <!-- Respawn immédiat -->
    <min>60</min>                     <!-- Au moins 60 garantis -->
    <quantmin>-1</quantmin>           <!-- Pas de quantité variable -->
    <quantmax>-1</quantmax>
    <cost>5</cost>                    <!-- Coût faible -->
    <flags 
        count_in_cargo="0" 
        count_in_hoarder="0" 
        count_in_map="1" 
        count_in_player="0" 
        crafted="0" 
        deloot="0"
    />
    <category name="food"/>
    <usage name="Town"/>              <!-- Spawn dans les villes -->
    <usage name="Village"/>           <!-- Et les villages -->
    <usage name="Farm"/>              <!-- Et les fermes -->
    <value name="Tier1"/>             <!-- Dispo dès la côte -->
    <value name="Tier2"/>
</type>
```

**Résultat :** Nourriture commune disponible partout.

---

### Exemple 3 : Item craftable uniquement (Arme peinte)
```xml
<type name="AK74_Black">
    <nominal>0</nominal>              <!-- Ne spawn PAS naturellement -->
    <lifetime>28800</lifetime>
    <restock>0</restock>
    <min>0</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags 
        count_in_cargo="0" 
        count_in_hoarder="0" 
        count_in_map="1" 
        count_in_player="0" 
        crafted="1"                   <!-- Craftable uniquement -->
        deloot="0"
    />
    <category name="weapons"/>
    <!-- PAS de <usage> ni <value> -->
</type>
```

**Résultat :** Obtenu uniquement en peignant un AK74 en noir.

---

### Exemple 4 : Item d'event temporaire (Hélico crash)
```xml
<type name="VSS">
    <nominal>1</nominal>              <!-- 1 seul sur la map -->
    <lifetime>7200</lifetime>         <!-- 2h -->
    <restock>7200</restock>           <!-- 2h avant respawn -->
    <min>0</min>                      <!-- Pas de minimum garanti -->
    <quantmin>50</quantmin>
    <quantmax>100</quantmax>
    <cost>100</cost>
    <flags 
        count_in_cargo="0" 
        count_in_hoarder="0" 
        count_in_map="1" 
        count_in_player="0" 
        crafted="0" 
        deloot="1"                    <!-- Cleanup si hélico despawn -->
    />
    <category name="weapons"/>
    <!-- Spawn géré par events.xml, pas de <usage> ici -->
</type>
```

**Résultat :** Arme d'hélico crash, spawn contrôlé par events.xml.

---

## 🎯 Cas d'usage et stratégies

### Stratégie 1 : Augmenter la rareté d'un item
```xml
<!-- AVANT (item commun) -->
<nominal>50</nominal>
<min>40</min>
<restock>0</restock>

<!-- APRÈS (item rare) -->
<nominal>10</nominal>    <!-- Diminuer -->
<min>5</min>             <!-- Diminuer proportionnellement -->
<restock>3600</restock>  <!-- Augmenter (ralentir respawn) -->
```

---

### Stratégie 2 : Désactiver complètement un item
```xml
<nominal>0</nominal>
<lifetime>28800</lifetime>
<restock>0</restock>
<min>0</min>
<quantmin>-1</quantmin>
<quantmax>-1</quantmax>
<cost>100</cost>
<flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
<category name="weapons"/>
<!-- Supprimer tous les <usage> et <value> -->
```

---

### Stratégie 3 : Créer un item ultra rare unique
```xml
<nominal>1</nominal>     <!-- 1 seul -->
<lifetime>86400</lifetime>  <!-- 24h -->
<restock>86400</restock>    <!-- 24h avant respawn -->
<min>1</min>             <!-- Toujours 1 présent -->
<usage name="Military"/>
<value name="Tier4"/>    <!-- Uniquement grandes bases -->
```

---

### Stratégie 4 : Item événementiel saisonnier
```xml
<nominal>20</nominal>
<lifetime>3600</lifetime>
<restock>0</restock>
<min>15</min>
<usage name="SeasonalEvent"/>  <!-- Zone d'événement -->
<flags deloot="1" />           <!-- Cleanup après event -->
```

---

## 🔍 Erreurs courantes et solutions

### Erreur 1 : Items qui ne spawnent pas
**Symptômes :** L'item n'apparaît jamais sur le serveur

**Causes possibles :**
1. `nominal = 0` → Item désactivé
2. Pas de `<usage>` → Aucune zone de spawn définie
3. `restock` trop élevé + item déjà looté → Attend le restock
4. `flags` mal configurés → Item compté ailleurs

**Solutions :**
```xml
<!-- Vérifier -->
<nominal>10</nominal>  <!-- > 0 -->
<usage name="Military"/>  <!-- Au moins 1 usage -->
<restock>1800</restock>  <!-- Pas trop élevé -->
```

---

### Erreur 2 : Trop d'items d'un type
**Symptômes :** L'item spawn en masse, map saturée

**Causes :**
1. `nominal` trop élevé
2. `restock = 0` avec `nominal` élevé = spawn constant
3. `flags count_in_cargo="1"` → Items stockés comptent pas, respawn sans cesse

**Solutions :**
```xml
<nominal>20</nominal>  <!-- Diminuer -->
<restock>1800</restock>  <!-- Augmenter (ralentir) -->
<flags count_in_cargo="0" />  <!-- Standard -->
```

---

### Erreur 3 : Items disparaissent trop vite
**Symptômes :** Items lootés despawnent rapidement

**Cause :** `lifetime` trop court

**Solution :**
```xml
<!-- AVANT -->
<lifetime>1800</lifetime>  <!-- 30 min = trop court -->

<!-- APRÈS -->
<lifetime>14400</lifetime>  <!-- 4h = mieux -->
```

---

### Erreur 4 : Déséquilibre économique
**Symptômes :** Certains items trop rares/communs par rapport à l'équilibre vanilla

**Solution :** Comparer avec les valeurs vanilla de référence

**Items clés de référence vanilla :**
- Munitions 5.56 : nominal=60
- AK74 : nominal=6
- M4A1 : nominal=3
- SVD : nominal=2
- Pommes : nominal=200

---

## 📈 Valeurs de référence vanilla

### Armes de poing
- Glock : nominal=15, lifetime=28800
- Deagle : nominal=3, lifetime=28800

### Fusils d'assaut
- AK74 : nominal=6, lifetime=28800
- M4A1 : nominal=3, lifetime=28800
- AUG : nominal=2, lifetime=28800

### Fusils de précision
- Mosin : nominal=20, lifetime=28800
- SVD : nominal=2, lifetime=28800

### Nourriture
- Peaches : nominal=80, lifetime=3600
- Rice : nominal=60, lifetime=3600
- Apple : nominal=200, lifetime=3600

### Munitions
- 7.62x39 : nominal=60, lifetime=14400
- 5.56 : nominal=60, lifetime=14400
- .308 : nominal=30, lifetime=14400

---

## 🛠️ Outils et workflow recommandés

### Workflow de modification

1. **Backup** : Toujours sauvegarder le fichier original
2. **Modifier** : Éditer avec un éditeur XML (Notepad++, VS Code)
3. **Valider** : Utiliser **Codex Validateur** pour vérifier la syntaxe
4. **Tester** : Uploader sur serveur de test
5. **Déployer** : Si OK, déployer en production
6. **Surveiller** : Observer les logs et le comportement in-game

### Commandes utiles (serveur)

**Forcer un cleanup :**
```
#exec server.cleanup
```

**Redémarrer l'économie :**
```
(nécessite restart du serveur)
```

---

## 📚 Ressources complémentaires

### Fichiers liés
- `cfgeconomycore.xml` - Configuration économie globale
- `events.xml` - Events dynamiques (hélico crash, etc.)
- `mapgroupproto.xml` - Groupes de positions de spawn
- `mapgrouppos.xml` - Positions précises sur la map

### Interactions avec d'autres fichiers
- Les `<usage>` font référence aux zones définies dans `mapgroupproto.xml`
- Les items d'events (hélico) sont configurés dans `events.xml` mais référencent `types.xml`
- Les tiers font référence à la géographie de la map

---

## ✅ Checklist de validation Codex

### Syntaxe XML
- [ ] Fichier commence par `<?xml version="1.0"?>`
- [ ] Balise racine `<types>` présente
- [ ] Toutes les balises sont fermées
- [ ] Pas de caractères spéciaux non échappés

### Structure des items
- [ ] Chaque `<type>` a un attribut `name` unique
- [ ] Toutes les balises obligatoires présentes (nominal, lifetime, restock, min)
- [ ] Pas de balises inconnues

### Valeurs numériques
- [ ] `min` ≤ `nominal`
- [ ] `quantmin` ≤ `quantmax`
- [ ] `lifetime` > 0
- [ ] `cost` entre 0 et 100
- [ ] Tous les flags sont 0 ou 1

### Énumérations
- [ ] `<category>` utilise une valeur autorisée
- [ ] `<usage>` utilise des valeurs autorisées
- [ ] `<value>` utilise des valeurs autorisées
- [ ] `<tag>` utilise des valeurs autorisées

### Cohérence logique
- [ ] Items désactivés (nominal=0) ont min=0
- [ ] Items craftables (crafted=1) n'ont généralement pas de <usage>
- [ ] Pas de configuration absurde (ex: lifetime=1, nominal=1000)

---

## 🎓 Pour aller plus loin

### Optimisation avancée
- Équilibrer `nominal` vs `min` pour éviter les pics/creux
- Ajuster `restock` selon le gameplay souhaité (survie hardcore vs casual)
- Utiliser `deloot=1` pour items d'events temporaires
- Combiner plusieurs `<usage>` pour items polyvalents

### Tests recommandés
- Observer les spawns sur 24h après modif
- Vérifier les logs serveur (warnings économie)
- Interroger les joueurs sur la rareté perçue
- Comparer avec les statistiques vanilla

---

**📝 Document créé par Codex - L'outil pour la communauté DayZ FR**
**Version : 1.0 - Basé sur DayZ 1.28 Chernarus**
**Dernière mise à jour : 2025**
