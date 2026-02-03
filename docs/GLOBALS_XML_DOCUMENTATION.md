# 📄 GLOBALS.XML - Documentation Complète

## 📋 Vue d'ensemble

### Informations générales
- **Nom du fichier** : `globals.xml`
- **Rôle** : Configuration des variables globales du serveur (timers, limites, comportements)
- **Emplacement** : `mpmissions/[nom_mission]/db/globals.xml`
- **Version DayZ** : 1.28
- **Priorité** : ⭐⭐⭐ ÉLEVÉE (affecte performance et gameplay)
- **Fréquence de modification** : MOYENNE (ajustements selon besoins serveur)
- **Nombre de variables** : **31 variables** dans la version vanilla

### Impact sur le serveur
- ✅ Contrôle les **LIMITES** (animaux max, zombies max)
- ✅ Gère les **TIMERS** (cleanup, login, logout, respawn)
- ✅ Configure le **LOOT** (spawn initial, respawn, damage)
- ✅ Définit les **COMPORTEMENTS** (food decay, flag refresh, idle mode)
- ✅ Optimise les **PERFORMANCES** (spawn distance, avoidance)

### Redémarrage requis
- ✅ Modifications prises en compte au **prochain restart** du serveur
- ⚠️ Pas de hot-reload possible

---

## 🏗️ Structure XML

### Structure complète
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<variables>
    <var name="NomVariable" type="0" value="100"/>
    <var name="AutreVariable" type="1" value="0.5"/>
    <!-- ... 31 variables au total ... -->
</variables>
```

### Structure d'une variable
```xml
<var 
    name="AnimalMaxCount"    <!-- Nom de la variable -->
    type="0"                 <!-- Type : 0=entier, 1=décimal -->
    value="200"              <!-- Valeur -->
/>
```

---

## 📊 Les 2 types de variables

### Type 0 - Integer (Entier)
- **Description** : Nombre entier (pas de décimales)
- **Exemples** : 100, 3600, 1000
- **Usage** : Compteurs, timers en secondes, limites

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
```

---

### Type 1 - Float (Décimal)
- **Description** : Nombre décimal
- **Exemples** : 0.5, 0.82, 1.0
- **Usage** : Pourcentages, ratios

```xml
<var name="LootDamageMax" type="1" value="0.82"/>
```

---

## 🎯 Documentation des 31 variables

### 🐾 ANIMAUX

#### `AnimalMaxCount`
- **Type** : Integer (0)
- **Valeur vanilla** : `200`
- **Plage recommandée** : 0 à 500
- **Description** : Nombre MAXIMUM d'animaux simultanés sur le serveur
- **Impact** : 
  - Valeur basse = Moins d'animaux, moins de viande
  - Valeur haute = Plus d'animaux, plus de charge serveur

**Exemples :**
```xml
<!-- Serveur PvP (peu d'animaux) -->
<var name="AnimalMaxCount" type="0" value="50"/>

<!-- Serveur survie (beaucoup d'animaux) -->
<var name="AnimalMaxCount" type="0" value="400"/>

<!-- Vanilla -->
<var name="AnimalMaxCount" type="0" value="200"/>
```

**⚠️ Performance :**
- > 500 = Charge serveur élevée
- 0 = Désactive complètement les animaux

---

### 🧟 ZOMBIES

#### `ZombieMaxCount`
- **Type** : Integer (0)
- **Valeur vanilla** : `1000`
- **Plage recommandée** : 0 à 2000
- **Description** : Nombre MAXIMUM de zombies simultanés sur le serveur
- **Impact** :
  - Valeur basse = Moins de zombies, serveur PvP
  - Valeur haute = Horde mode, survie difficile

**Exemples :**
```xml
<!-- Serveur PvP pur (pas de zombies) -->
<var name="ZombieMaxCount" type="0" value="0"/>

<!-- Serveur équilibré -->
<var name="ZombieMaxCount" type="0" value="1000"/>

<!-- Horde mode -->
<var name="ZombieMaxCount" type="0" value="2000"/>
```

**⚠️ Performance :**
- > 1500 = Peut causer du lag sur serveurs faibles
- Lié aux configs dans `zombie_territories.xml` et `events.xml`

---

### 🧹 CLEANUP (Nettoyage automatique)

#### `CleanupLifetimeDefault`
- **Type** : Integer (0)
- **Valeur vanilla** : `45`
- **Unité** : Minutes
- **Description** : Durée de vie par défaut des objets au sol avant cleanup
- **Impact** : Items au sol despawnent après ce délai

**Exemples :**
```xml
<!-- Cleanup rapide (serveur performant) -->
<var name="CleanupLifetimeDefault" type="0" value="30"/>

<!-- Vanilla -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>

<!-- Cleanup lent (items persistent longtemps) -->
<var name="CleanupLifetimeDefault" type="0" value="90"/>
```

---

#### `CleanupLifetimeRuined`
- **Type** : Integer (0)
- **Valeur vanilla** : `330`
- **Unité** : Secondes
- **Description** : Durée de vie des items **RUINED** (état détruit) avant cleanup
- **Impact** : Items ruinés despawnent plus vite

```xml
<!-- Vanilla (5min 30s) -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>

<!-- Cleanup très rapide -->
<var name="CleanupLifetimeRuined" type="0" value="60"/>
```

**Note :** Items ruinés = inutilisables, donc cleanup rapide = bon pour performance

---

#### `CleanupLifetimeDeadPlayer`
- **Type** : Integer (0)
- **Valeur vanilla** : `3600`
- **Unité** : Secondes
- **Description** : Durée de vie des **CADAVRES DE JOUEURS** avant despawn
- **Impact** : Temps pour looter les morts

**Exemples :**
```xml
<!-- Despawn rapide (30 min) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="1800"/>

<!-- Vanilla (1 heure) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>

<!-- Despawn lent (2 heures - serveurs RP) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="7200"/>
```

**⚠️ Équilibre :**
- Trop court = Pas le temps de revenir looter son corps
- Trop long = Accumulation de cadavres (performance)

---

#### `CleanupLifetimeDeadInfected`
- **Type** : Integer (0)
- **Valeur vanilla** : `330`
- **Unité** : Secondes
- **Description** : Durée de vie des **CADAVRES DE ZOMBIES** avant despawn
- **Impact** : Combien de temps les zombies morts restent au sol

```xml
<!-- Vanilla (5min 30s) -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>

<!-- Cleanup très rapide (30s - performance) -->
<var name="CleanupLifetimeDeadInfected" type="0" value="30"/>
```

---

#### `CleanupLifetimeDeadAnimal`
- **Type** : Integer (0)
- **Valeur vanilla** : `1200`
- **Unité** : Secondes
- **Description** : Durée de vie des **CADAVRES D'ANIMAUX** avant despawn
- **Impact** : Temps pour dépecer les animaux

```xml
<!-- Vanilla (20 minutes) -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>

<!-- Despawn rapide (5 min) -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="300"/>
```

---

#### `CleanupLifetimeLimit`
- **Type** : Integer (0)
- **Valeur vanilla** : `50`
- **Unité** : Minutes
- **Description** : Durée de vie **LIMITE** pour certains objets spéciaux
- **Impact** : Limite supérieure de cleanup

```xml
<!-- Vanilla -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>
```

**Note :** Variable avancée, rarement modifiée

---

#### `CleanupAvoidance`
- **Type** : Integer (0)
- **Valeur vanilla** : `100`
- **Unité** : Mètres
- **Description** : Distance autour des joueurs où le cleanup est **ÉVITÉ**
- **Impact** : Items proches des joueurs ne sont pas cleanup

```xml
<!-- Vanilla -->
<var name="CleanupAvoidance" type="0" value="100"/>

<!-- Protection étendue (200m) -->
<var name="CleanupAvoidance" type="0" value="200"/>
```

**Logique :** Évite de despawn les items que le joueur vient de looter

---

### 🎁 LOOT SPAWN

#### `InitialSpawn`
- **Type** : Integer (0)
- **Valeur vanilla** : `100`
- **Unité** : Pourcentage
- **Description** : Pourcentage du loot qui spawn au **démarrage initial** du serveur
- **Impact** : Densité de loot au tout premier boot

```xml
<!-- Loot faible au démarrage (50%) -->
<var name="InitialSpawn" type="0" value="50"/>

<!-- Vanilla (100%) -->
<var name="InitialSpawn" type="0" value="100"/>
```

**Note :** Utilisé seulement au PREMIER boot (base vide)

---

#### `RestartSpawn`
- **Type** : Integer (0)
- **Valeur vanilla** : `0`
- **Unité** : Pourcentage
- **Description** : Pourcentage du loot qui respawn lors d'un **restart** (pas au boot initial)
- **Impact** : Boost de loot après restart

```xml
<!-- Vanilla (pas de boost) -->
<var name="RestartSpawn" type="0" value="0"/>

<!-- Boost 20% au restart -->
<var name="RestartSpawn" type="0" value="20"/>
```

**Usage :**
- 0 = Pas de boost (vanilla)
- > 0 = Boost de loot à chaque restart (peut encourager restart farming)

---

#### `SpawnInitial`
- **Type** : Integer (0)
- **Valeur vanilla** : `1200`
- **Unité** : Secondes
- **Description** : Durée du **spawn initial** au démarrage du serveur
- **Impact** : Temps pendant lequel le loot spawn massivement au boot

```xml
<!-- Vanilla (20 minutes) -->
<var name="SpawnInitial" type="0" value="1200"/>

<!-- Spawn initial rapide (10 min) -->
<var name="SpawnInitial" type="0" value="600"/>
```

**Logique :** Après ce timer, le respawn passe en mode normal (RespawnTypes)

---

#### `RespawnLimit`
- **Type** : Integer (0)
- **Valeur vanilla** : `20`
- **Description** : Nombre maximum d'items qui peuvent respawn **par cycle**
- **Impact** : Limite le flood de respawn

```xml
<!-- Vanilla -->
<var name="RespawnLimit" type="0" value="20"/>

<!-- Plus de respawn par cycle -->
<var name="RespawnLimit" type="0" value="40"/>
```

**Performance :** Valeur trop haute = pic de charge à chaque cycle

---

#### `RespawnAttempt`
- **Type** : Integer (0)
- **Valeur vanilla** : `2`
- **Description** : Nombre de **tentatives** de respawn par cycle
- **Impact** : Augmente les chances de respawn réussi

```xml
<!-- Vanilla -->
<var name="RespawnAttempt" type="0" value="2"/>

<!-- Plus agressif -->
<var name="RespawnAttempt" type="0" value="5"/>
```

---

#### `RespawnTypes`
- **Type** : Integer (0)
- **Valeur vanilla** : `12`
- **Description** : Nombre de **types d'items** différents traités par cycle de respawn
- **Impact** : Diversité du respawn

```xml
<!-- Vanilla -->
<var name="RespawnTypes" type="0" value="12"/>

<!-- Plus de diversité -->
<var name="RespawnTypes" type="0" value="20"/>
```

---

#### `LootSpawnAvoidance`
- **Type** : Integer (0)
- **Valeur vanilla** : `100`
- **Unité** : Mètres
- **Description** : Distance minimale de spawn du loot autour des joueurs
- **Impact** : Évite le spawn de loot sous le nez des joueurs

```xml
<!-- Vanilla -->
<var name="LootSpawnAvoidance" type="0" value="100"/>

<!-- Spawn plus près (risqué) -->
<var name="LootSpawnAvoidance" type="0" value="50"/>
```

---

#### `LootProxyPlacement`
- **Type** : Integer (0)
- **Valeur vanilla** : `1`
- **Description** : Active (1) ou désactive (0) le placement proxy du loot
- **Impact** : Mode de placement du loot

```xml
<!-- Vanilla (activé) -->
<var name="LootProxyPlacement" type="0" value="1"/>

<!-- Désactivé -->
<var name="LootProxyPlacement" type="0" value="0"/>
```

**Note :** Rarement modifié, affecte le système de spawn

---

#### `LootDamageMin`
- **Type** : Float (1)
- **Valeur vanilla** : `0.0`
- **Plage** : 0.0 à 1.0
- **Description** : Durabilité **MINIMALE** du loot au spawn (0.0 = 0%, 1.0 = 100%)
- **Impact** : État minimum des items spawnés

```xml
<!-- Vanilla (peut spawner complètement ruiné) -->
<var name="LootDamageMin" type="1" value="0.0"/>

<!-- Loot toujours au moins à 50% -->
<var name="LootDamageMin" type="1" value="0.5"/>
```

---

#### `LootDamageMax`
- **Type** : Float (1)
- **Valeur vanilla** : `0.82`
- **Plage** : 0.0 à 1.0
- **Description** : Durabilité **MAXIMALE** du loot au spawn
- **Impact** : État maximum des items spawnés

```xml
<!-- Vanilla (82% max) -->
<var name="LootDamageMax" type="1" value="0.82"/>

<!-- Loot neuf (100%) -->
<var name="LootDamageMax" type="1" value="1.0"/>

<!-- Loot toujours endommagé (max 50%) -->
<var name="LootDamageMax" type="1" value="0.5"/>
```

**Logique :**
- `LootDamageMin` à `LootDamageMax` = Plage aléatoire de durabilité
- Ex: min=0.5, max=0.82 → Items spawnent entre 50% et 82%

---

### 🚩 FLAGS (Drapeaux de territoire)

#### `FlagRefreshFrequency`
- **Type** : Integer (0)
- **Valeur vanilla** : `432000`
- **Unité** : Secondes
- **Description** : Fréquence à laquelle les drapeaux doivent être **rafraîchis** (baissés/montés)
- **Conversion** : 432000s = **5 jours**
- **Impact** : Combien de temps avant que le drapeau doive être interagi

```xml
<!-- Vanilla (5 jours) -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>

<!-- Plus fréquent (3 jours) -->
<var name="FlagRefreshFrequency" type="0" value="259200"/>

<!-- Moins fréquent (7 jours) -->
<var name="FlagRefreshFrequency" type="0" value="604800"/>
```

**Usage :** Si le drapeau n'est pas rafraîchi, la base commence à se dégrader

---

#### `FlagRefreshMaxDuration`
- **Type** : Integer (0)
- **Valeur vanilla** : `3456000`
- **Unité** : Secondes
- **Description** : Durée **MAXIMALE** avant despawn complet de la base inactive
- **Conversion** : 3456000s = **40 jours**
- **Impact** : Temps avant que la base soit supprimée si jamais rafraîchie

```xml
<!-- Vanilla (40 jours) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>

<!-- Plus court (20 jours - anti-hoarding) -->
<var name="FlagRefreshMaxDuration" type="0" value="1728000"/>

<!-- Plus long (60 jours) -->
<var name="FlagRefreshMaxDuration" type="0" value="5184000"/>
```

**Logique :** Évite les bases abandonnées qui occupent la map indéfiniment

---

### ⏱️ TIMERS (Connexion/Déconnexion)

#### `TimeLogin`
- **Type** : Integer (0)
- **Valeur vanilla** : `15`
- **Unité** : Secondes
- **Description** : Temps avant qu'un joueur puisse se **reconnecter** après déconnexion
- **Impact** : Anti combat-logging

```xml
<!-- Vanilla -->
<var name="TimeLogin" type="0" value="15"/>

<!-- Plus strict (30s) -->
<var name="TimeLogin" type="0" value="30"/>

<!-- Moins strict (5s) -->
<var name="TimeLogin" type="0" value="5"/>
```

**Usage :** Empêche les joueurs de se déconnecter en combat et se reconnecter ailleurs

---

#### `TimeLogout`
- **Type** : Integer (0)
- **Valeur vanilla** : `15`
- **Unité** : Secondes
- **Description** : Temps que le personnage reste dans le jeu après **déconnexion**
- **Impact** : Combat-logging protection

```xml
<!-- Vanilla -->
<var name="TimeLogout" type="0" value="15"/>

<!-- Plus strict (30s) -->
<var name="TimeLogout" type="0" value="30"/>
```

**Logique :** Le perso reste vulnérable 15s après alt+F4

---

#### `TimeHopping`
- **Type** : Integer (0)
- **Valeur vanilla** : `60`
- **Unité** : Secondes
- **Description** : Pénalité de temps pour **server hopping** (changer de serveur)
- **Impact** : Anti-loot farming multi-serveurs

```xml
<!-- Vanilla -->
<var name="TimeHopping" type="0" value="60"/>

<!-- Plus strict (5 min) -->
<var name="TimeHopping" type="0" value="300"/>

<!-- Moins strict (30s) -->
<var name="TimeHopping" type="0" value="30"/>
```

---

#### `TimePenalty`
- **Type** : Integer (0)
- **Valeur vanilla** : `20`
- **Unité** : Secondes
- **Description** : Pénalité de temps **générale** (diverses situations)
- **Impact** : Timer de sécurité

```xml
<!-- Vanilla -->
<var name="TimePenalty" type="0" value="20"/>
```

---

### 🌍 MONDE & ZONES

#### `ZoneSpawnDist`
- **Type** : Integer (0)
- **Valeur vanilla** : `300`
- **Unité** : Mètres
- **Description** : Distance **maximale** autour d'un joueur où les entités peuvent spawn
- **Impact** : Taille de la "bulle" de spawn autour des joueurs

```xml
<!-- Vanilla -->
<var name="ZoneSpawnDist" type="0" value="300"/>

<!-- Bulle plus grande (500m) -->
<var name="ZoneSpawnDist" type="0" value="500"/>

<!-- Bulle plus petite (150m - dense) -->
<var name="ZoneSpawnDist" type="0" value="150"/>
```

**Impact performance :**
- Plus grand = Plus d'entités actives = Plus de charge
- Plus petit = Zone de spawn réduite

---

### 🍖 NOURRITURE

#### `FoodDecay`
- **Type** : Integer (0)
- **Valeur vanilla** : `1`
- **Description** : Active (1) ou désactive (0) la **décomposition de la nourriture**
- **Impact** : La viande/nourriture se gâte ou non

```xml
<!-- Vanilla (décomposition activée) -->
<var name="FoodDecay" type="0" value="1"/>

<!-- Désactiver décomposition -->
<var name="FoodDecay" type="0" value="0"/>
```

**Usage :**
- 1 = Réaliste (viande pourrit)
- 0 = Casual (viande ne pourrit jamais)

---

### 💤 IDLE MODE (Mode inactif)

#### `IdleModeStartup`
- **Type** : Integer (0)
- **Valeur vanilla** : `1`
- **Description** : Active (1) ou désactive (0) le **mode idle au démarrage**
- **Impact** : Serveur démarre en mode économie d'énergie si personne connecté

```xml
<!-- Vanilla (activé) -->
<var name="IdleModeStartup" type="0" value="1"/>

<!-- Désactivé -->
<var name="IdleModeStartup" type="0" value="0"/>
```

---

#### `IdleModeCountdown`
- **Type** : Integer (0)
- **Valeur vanilla** : `60`
- **Unité** : Secondes
- **Description** : Temps avant activation du **mode idle** (si aucun joueur)
- **Impact** : Économie de ressources sur serveurs vides

```xml
<!-- Vanilla (1 minute) -->
<var name="IdleModeCountdown" type="0" value="60"/>

<!-- Plus rapide (30s) -->
<var name="IdleModeCountdown" type="0" value="30"/>
```

---

### 🌡️ ENVIRONNEMENT

#### `WorldWetTempUpdate`
- **Type** : Integer (0)
- **Valeur vanilla** : `1`
- **Description** : Active (1) ou désactive (0) les **mises à jour de température/humidité**
- **Impact** : Système météo/température actif ou non

```xml
<!-- Vanilla (activé) -->
<var name="WorldWetTempUpdate" type="0" value="1"/>

<!-- Désactivé (pas de température) -->
<var name="WorldWetTempUpdate" type="0" value="0"/>
```

**Usage :**
- 1 = Réaliste (hypothermie, surchauffe)
- 0 = Casual (pas de gestion température)

---

## 📋 Configurations par type de serveur

### 🎮 Serveur Vanilla Standard
```xml
<variables>
    <var name="AnimalMaxCount" type="0" value="200"/>
    <var name="ZombieMaxCount" type="0" value="1000"/>
    <var name="CleanupLifetimeDefault" type="0" value="45"/>
    <var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>
    <var name="LootDamageMin" type="1" value="0.0"/>
    <var name="LootDamageMax" type="1" value="0.82"/>
    <var name="FlagRefreshFrequency" type="0" value="432000"/>
    <var name="FoodDecay" type="0" value="1"/>
    <!-- ... toutes les autres vanilla ... -->
</variables>
```

---

### 🔫 Serveur PvP (sans zombies, peu d'animaux)
```xml
<variables>
    <var name="AnimalMaxCount" type="0" value="50"/>         <!-- Réduit -->
    <var name="ZombieMaxCount" type="0" value="0"/>          <!-- Désactivé -->
    <var name="CleanupLifetimeDefault" type="0" value="30"/>  <!-- Rapide -->
    <var name="CleanupLifetimeDeadPlayer" type="0" value="1800"/> <!-- 30min -->
    <var name="TimeLogout" type="0" value="30"/>             <!-- Anti-combat log -->
    <var name="TimeHopping" type="0" value="300"/>           <!-- 5min pénalité -->
    <var name="LootDamageMin" type="1" value="0.5"/>         <!-- Loot en meilleur état -->
    <var name="LootDamageMax" type="1" value="1.0"/>
    <!-- ... -->
</variables>
```

---

### 🏕️ Serveur RP/Base-Building
```xml
<variables>
    <var name="AnimalMaxCount" type="0" value="300"/>        <!-- Plus d'animaux -->
    <var name="ZombieMaxCount" type="0" value="500"/>        <!-- Zombies modérés -->
    <var name="CleanupLifetimeDefault" type="0" value="90"/>  <!-- Items persistent -->
    <var name="CleanupLifetimeDeadPlayer" type="0" value="7200"/> <!-- 2h -->
    <var name="FlagRefreshFrequency" type="0" value="604800"/>  <!-- 7 jours -->
    <var name="FlagRefreshMaxDuration" type="0" value="5184000"/> <!-- 60 jours -->
    <var name="TimeHopping" type="0" value="0"/>             <!-- Pas de pénalité -->
    <var name="FoodDecay" type="0" value="1"/>
    <!-- ... -->
</variables>
```

---

### 🧟 Serveur Hardcore Zombies
```xml
<variables>
    <var name="AnimalMaxCount" type="0" value="50"/>         <!-- Peu d'animaux -->
    <var name="ZombieMaxCount" type="0" value="2000"/>       <!-- HORDE -->
    <var name="CleanupLifetimeDefault" type="0" value="30"/>
    <var name="CleanupLifetimeDeadInfected" type="0" value="10"/> <!-- Cleanup zombies rapide -->
    <var name="LootDamageMin" type="1" value="0.0"/>         <!-- Loot endommagé -->
    <var name="LootDamageMax" type="1" value="0.5"/>
    <var name="RespawnLimit" type="0" value="10"/>           <!-- Moins de respawn -->
    <var name="FoodDecay" type="0" value="1"/>
    <!-- ... -->
</variables>
```

---

### ⚡ Serveur Performance Optimisé
```xml
<variables>
    <var name="AnimalMaxCount" type="0" value="100"/>        <!-- Réduit -->
    <var name="ZombieMaxCount" type="0" value="500"/>        <!-- Réduit -->
    <var name="CleanupLifetimeDefault" type="0" value="20"/> <!-- Cleanup agressif -->
    <var name="CleanupLifetimeDeadInfected" type="0" value="30"/>
    <var name="CleanupLifetimeDeadAnimal" type="0" value="300"/>
    <var name="RespawnLimit" type="0" value="15"/>           <!-- Respawn modéré -->
    <var name="ZoneSpawnDist" type="0" value="200"/>         <!-- Bulle réduite -->
    <!-- ... -->
</variables>
```

---

## ⚠️ Règles de validation

### Règle 1 : Types corrects (0 ou 1)
```xml
<!-- ✅ CORRECT -->
<var name="ZombieMaxCount" type="0" value="1000"/>  <!-- Integer -->
<var name="LootDamageMax" type="1" value="0.82"/>   <!-- Float -->

<!-- ❌ ERREUR -->
<var name="ZombieMaxCount" type="1" value="1000"/>  <!-- Type incorrect -->
<var name="LootDamageMax" type="0" value="0.82"/>   <!-- Type incorrect -->
```

---

### Règle 2 : Valeurs dans plages logiques
```xml
<!-- ⚠️ ABSURDE -->
<var name="AnimalMaxCount" type="0" value="-100"/>  <!-- Négatif -->
<var name="LootDamageMax" type="1" value="5.0"/>    <!-- > 1.0 -->

<!-- ✅ CORRECT -->
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="LootDamageMax" type="1" value="0.82"/>
```

---

### Règle 3 : LootDamageMin ≤ LootDamageMax
```xml
<!-- ❌ ERREUR -->
<var name="LootDamageMin" type="1" value="0.9"/>
<var name="LootDamageMax" type="1" value="0.5"/>  <!-- Min > Max -->

<!-- ✅ CORRECT -->
<var name="LootDamageMin" type="1" value="0.0"/>
<var name="LootDamageMax" type="1" value="0.82"/>
```

---

### Règle 4 : Cohérence timers
```xml
<!-- ⚠️ INCOHÉRENT -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 jours -->
<var name="FlagRefreshMaxDuration" type="0" value="86400"/>     <!-- 1 jour -->
<!-- MaxDuration < Frequency = impossible -->

<!-- ✅ CORRECT -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 jours -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>   <!-- 40 jours -->
```

---

## 🎯 Impact des variables clés

### Tableau récapitulatif

| Variable | Impact Low | Impact High | Performance |
|----------|------------|-------------|-------------|
| **AnimalMaxCount** | Peu d'animaux | Beaucoup d'animaux | ⬆️ Charge si > 400 |
| **ZombieMaxCount** | PvP | Horde mode | ⬆️⬆️ Charge si > 1500 |
| **CleanupLifetimeDefault** | Map propre | Items persistent | ⬇️ Perf si > 90 |
| **LootDamageMax** | Loot endommagé | Loot neuf | Neutre |
| **TimeLogout** | Risque combat-log | Protection forte | Neutre |
| **ZoneSpawnDist** | Zone dense | Zone étendue | ⬆️ Charge si > 500 |

---

## 💡 Cas d'usage et stratégies

### Stratégie 1 : Optimisation performance
```xml
<!-- Réduire les limites -->
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZombieMaxCount" type="0" value="500"/>

<!-- Cleanup agressif -->
<var name="CleanupLifetimeDefault" type="0" value="20"/>
<var name="CleanupLifetimeDeadInfected" type="0" value="30"/>

<!-- Zone réduite -->
<var name="ZoneSpawnDist" type="0" value="200"/>
```

**Résultat :** Serveur plus fluide, moins de charge

---

### Stratégie 2 : Serveur débutant-friendly
```xml
<!-- Loot en bon état -->
<var name="LootDamageMin" type="1" value="0.5"/>
<var name="LootDamageMax" type="1" value="1.0"/>

<!-- Zombies modérés -->
<var name="ZombieMaxCount" type="0" value="500"/>

<!-- Pas de décomposition nourriture -->
<var name="FoodDecay" type="0" value="0"/>

<!-- Items persistent longtemps -->
<var name="CleanupLifetimeDefault" type="0" value="90"/>
```

**Résultat :** Gameplay plus accessible

---

### Stratégie 3 : Anti-combat logging
```xml
<!-- Timers stricts -->
<var name="TimeLogin" type="0" value="30"/>
<var name="TimeLogout" type="0" value="60"/>
<var name="TimeHopping" type="0" value="600"/>  <!-- 10 min -->
```

**Résultat :** Moins de ghosting et combat-logging

---

## 🔍 Erreurs courantes et solutions

### Erreur 1 : Serveur lag avec beaucoup de joueurs
**Cause :** Trop d'entités actives

**Solution :**
```xml
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZombieMaxCount" type="0" value="500"/>
<var name="CleanupLifetimeDefault" type="0" value="30"/>
```

---

### Erreur 2 : Loot ne respawn pas assez
**Cause :** Limites trop basses

**Solution :**
```xml
<var name="RespawnLimit" type="0" value="30"/>
<var name="RespawnAttempt" type="0" value="5"/>
<var name="RespawnTypes" type="0" value="20"/>
```

---

### Erreur 3 : Bases despawnent trop vite
**Cause :** Timers drapeaux trop courts

**Solution :**
```xml
<var name="FlagRefreshFrequency" type="0" value="604800"/>    <!-- 7 jours -->
<var name="FlagRefreshMaxDuration" type="0" value="5184000"/> <!-- 60 jours -->
```

---

## ✅ Checklist de validation Codex

### Syntaxe XML
- [ ] Fichier commence par `<?xml version="1.0"?>`
- [ ] Balise racine `<variables>` présente
- [ ] 31 variables présentes
- [ ] Toutes les balises auto-fermantes (`/>`)

### Types
- [ ] Variables integer ont `type="0"`
- [ ] Variables float ont `type="1"`
- [ ] LootDamageMin et LootDamageMax ont `type="1"`

### Valeurs
- [ ] Pas de valeurs négatives (sauf si logique)
- [ ] LootDamageMin entre 0.0 et 1.0
- [ ] LootDamageMax entre 0.0 et 1.0
- [ ] LootDamageMin ≤ LootDamageMax

### Cohérence
- [ ] FlagRefreshMaxDuration > FlagRefreshFrequency
- [ ] AnimalMaxCount et ZombieMaxCount raisonnables (< 5000)
- [ ] Timers cleanup cohérents

---

## 📊 Conversions utiles

### Temps
- 60s = 1 minute
- 3600s = 1 heure
- 86400s = 1 jour
- 604800s = 7 jours
- 432000s = 5 jours
- 3456000s = 40 jours

### Durabilité
- 0.0 = 0% (ruiné)
- 0.5 = 50% (endommagé)
- 0.82 = 82% (vanilla max)
- 1.0 = 100% (neuf)

---

**📝 Document créé par CodeX - L'outil pour la communauté DayZ FR**
**Version : 1.0 - Basé sur DayZ 1.28**
**Dernière mise à jour : 2025**
