# Étude de cas — Accueil Coupe du Monde 2026 (TSE)

**Notebook Python + README du projet**

## 🎯 Résumé exécutif

* **Reco** : **Agrandir le TO Field pour 2026** (VAN 5 ans supérieure & chemin réglementaire plus court).
* **Option long terme** : **Nouveau stade** peut devenir préférable **≥ 32–33 ans**, surtout avec **cofinancement** ciblé (≈ **27 %** des coûts **t=0** met les options à **égalité à 30 ans**).
* **Pourquoi** : l’**Année 0** du nouveau stade (ex. foncier ~**343 M$** + permis + préparation, jeu de données fourni) **écrase** la VAN à court terme ; les revenus plus élevés se matérialisent sur un **horizon long**.
* **Conditions de succès** : cofinancement sécurisé, permis clés, design freeze, lots long-lead, intégrations techno (billetterie QR/NFC, capteurs foules).

---

## 📦 Contenus & données

* **Sources fournies**

  * PDF : `Septembre 2025 R2 - FIFA World Cup - FR.pdf` (énoncé, parties prenantes & régulation, tendances techno)
  * Excel : `Toronto Sports Entertainment_Sept 2025_FR.xlsx`

    * Feuille *Main d’œuvre* (3 lignes d’instructions, en-têtes à la ligne 4)
    * Feuille *Coûts de construction* (structure identique)
    * Feuille *Revenus* (structure identique)
    * Feuille *Overview* (paramètres généraux — réimplémentés dans `constants.py`)

---

## 🗂️ Arborescence recommandée

```
.
├─ data/
│  ├─ Septembre 2025 R2 - FIFA World Cup - FR.pdf
│  └─ Toronto Sports Entertainment_Sept 2025_FR.xlsx
├─ notebooks/
│  └─ etude_cas_TSE.ipynb
├─ src/
│  ├─ constants.py
│  ├─ io_loader.py            # lecture Excel (skip 3 lignes, drop 1ère colonne)
│  ├─ transforms.py           # calculs CF, VAN, projections, agrégations
│  ├─ viz.py                  # fonctions de graphiques (matplotlib)
│  └─ formatters.py           # formatage nombres (espaces, 2 décimales)
├─ outputs/
│  ├─ figures/                # .png exportés pour PPT
│  └─ tables/                 # .csv intermédiaires (optionnel)
├─ slides/
│  └─ Presentation_Cas_B.pptx
└─ README.md
```

---

## ⚙️ Environnement & installation

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -U pip
pip install jupyter pandas numpy openpyxl matplotlib
jupyter lab                           # ou jupyter notebook
```

> **Version Python** conseillée : 3.10+.

---

## 🔧 Paramètres (constants.py)

```python
# src/constants.py
VUEDENSEMBLE = {
    # Croissance
    "taux_croissance_couts": 0.02,     # 2 %
    "taux_croissance_revenus": 0.15,   # 15 %

    # Main d'œuvre
    "heures_moy_par_mois": 130,
    "facteur_heure_sup": 1.5,          # 1,5 × salaire horaire

    # Actualisation / horizon
    "taux_actualisation": 0.04,        # 4 % (VAN, flux nominaux)
    "duree_analyse_ans": 5,            # horizon baseline
}
```

> **Convention** : tous les **flux sont nominaux**, donc **taux nominal**.

---

## 🧠 Méthodologie (vue rapide)

1. **Nettoyage/lecture** des feuilles Excel : ignorer 3 lignes d’instructions, prendre toutes les colonnes utiles, **supprimer la 1ʳᵉ colonne vide**.
2. **Main d’œuvre** : salaire annuel = (salaire horaire × heures_moy × 12) + (heures_sup × salaire horaire × **facteur_heure_sup** × 12).
3. **Projections 5 ans** : appliquer **gc** (= 2 %) aux coûts et **gr** (= 15 %) aux revenus.
4. **Construction** :

   * **Année 0** = **coûts uniques** (foncier, permis/inspection, préparation)
   * **Années 1→N** = coûts **annuels** + **12× mensuels** (avec croissance)
5. **Revenus** : somme des postes (billetterie, sponsoring, concessions, marchandise) avec **gr**.
6. **Cash-flows** : CF₀ = – coûts uniques t=0 ; CFₜ = revenusₜ − (coûts main d’œuvreₜ + coûts construction récurrentsₜ).
7. **VAN** : ( \mathrm{VAN} = \sum_{t=0}^{T} \frac{CF_t}{(1+r)^t} ).
8. **Sensibilités** : horizons (10/20/30/40), **cofinancement** des coûts uniques **t=0** du nouveau stade, **taux r**.

---

## 🧪 Étapes du notebook (structure “étape X : markdown + code”)

* **Étape 1 — Overview → `constants.py`** : paramètres généraux (**VUEDENSEMBLE**)
* **Étape 2 — Main d’œuvre** : calcul salaires + projections 5 ans
* **Étape 3 — Formatage** : affichage lisible (espaces, 2 décimales)
* **Étape 4 — Agrégats main d’œuvre par projet** : totaux salariaux & **nombre de travailleurs**
* **Étape 5 — Coûts de construction (tableau brut)** : simple aperçu (vérif colonnes)

  * **5.1** : projection 5 ans (uniques t=0, annuels, mensuels×12)
  * **5.2** : **Total** par projet + **% part des coûts initiaux** (insight)
* **Étape 6 — Revenus** :

  * **6.0** : lecture & aperçu
  * **6.1** : projections 5 ans
  * **6.2** : **revenu total** par projet + **revenu par travailleur**
  * **6.5/6.6** : **mix revenus** (camemberts / 100 %)
* **Étape 7 — VAN (5 ans)** : CF année 0 → 5 + VAN par projet
* **Étape 8 — What-if** :

  * **8.1** : VAN **sans achat du terrain** (t=0)
  * **8.2** : variations de croissance revenus/couts (si utile)
  * **8.3** : valeur résiduelle (VR) — scénario
* **Étape 9 — Sensibilités** :

  * **9.1** : VAN vs **horizon** (10/20/30/40) & **points morts** (~17–18 ans / ~23–24 ans) & **croisement** (~32–33 ans)
  * **9.2** : **Heatmap ΔVAN** (Nouveau − Agrandir) vs **cofinancement × horizon** → **~27 % @ 30 ans = égalité**
  * **9.3** : VAN vs **r** (option)

---

## 📊 Graphiques clés (export pour PPT)

* **CF annuels (0→5 ans)** par option
* **VAN 5 ans** (barres) — labels numériques
* **Année 0 décomposée** (empilé : foncier, permis, préparation)
* **Mix des revenus** (2 camemberts ou 100 % empilé)
* **VAN vs horizon** (10/20/30/40) — 2 courbes
* **ΔVAN heatmap** (`cofinancement × horizon`) — point d’égalité **~27 % @ 30 ans**

> Export recommandé : `outputs/figures/*.png` (utilisables dans PowerPoint).

---

## 📌 Résultats & messages à retenir

* **5 ans** : **Agrandir > Nouveau** (Année 0 du nouveau **très** pénalisante).
* **Points morts** : **Agrandir ~17–18 ans**, **Nouveau ~23–24 ans**.
* **Croisement** : **~32–33 ans** (Nouveau ≥ Agrandir).
* **Cofinancement t=0 (Nouveau)** : **≈ 27 %** → **égalité à 30 ans** ; à **20 ans**, même **50 %** ne suffit pas ; à **40 ans**, le **Nouveau** domine **même sans cofinancement**.
* **Mix revenus** : agrandissement **plus dépendant du sponsoring** ; nouveau **plus diversifié**.
* **Reco** : **livrer 2026** via **agrandissement** ; **préparer le nouveau stade** (LT) si **cofinancement** & **permis** sont sécurisés.

---

## 🧾 Excel “vitrine” (conforme aux consignes)

Même si la modélisation est en Python, fournir un Excel minimal :

* **Onglet `Résultats`** : VAN 5/10/20/30/40 ans par option, ΔVAN(30 ans) vs % cofinancement (table courte), points morts & croisement.
* **Onglet `Hypothèses`** : r=4 %, gc=2 %, gr=15 %, heures & heures sup., hypothèses de projection.

> Les grands tableaux détaillés peuvent rester dans le notebook.

---

## 🧱 Hypothèses & hors périmètre

* Flux **nominals** ; r **nominal** 4 %.
* Pas de taxes, pas de financement/dette, pas d’amortissement, pas d’effets macro ni subventions **dans la base** (adressés en scénarios).
* Valeurs issues **exclusivement** du fichier Excel fourni.

---

## 👥 Parties prenantes & réglementaire (résumé d’exécution)

* **À gérer de près** : Ville de Toronto (permis, mobilité), **FIFA** (accessibilité, sûreté).
* **Cofinancement** : PPP, naming, subventions — **appliqué aux coûts uniques t=0** du **Nouveau stade**.
* **KPIs** : % cofinancement, % permis, flottant planning (j), écart CAPEX, pré-ventes/loges (%), readiness IT/5G (%).

---

## 🛣️ Feuille de route (exécutif)

* **2025–2026 (Agrandissement)** : pré-consultations & permis (2–4 mois), conception (overlap 4–6), appels d’offres (2–3), travaux (~7), tests (1–2) → **livraison 2026**.
* **2025–2030 (Nouveau stade)** : financement/foncier (6–12), études & permis (6–12, parallèle), conception (9–12), appels d’offres (6–9), **construction (24–36)**, commissioning (3–6) → **~2030**.

---

## ✅ Check-list qualité (avant envoi)

* Même **unité** partout (M$ si besoin), **espaces** pour milliers, **2 décimales** max.
* **Labels** numériques sur barres & points clés.
* Rappel discret : **r = 4 %** (flux nominaux).
* Slide finale : **Reco + conditions de succès + prochaines étapes**.

---
