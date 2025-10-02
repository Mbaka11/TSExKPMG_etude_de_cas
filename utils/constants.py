# -*- coding: utf-8 -*-
"""
overview.py — Constantes globales pour l'étude de cas TSE (KPMG)
Toutes les valeurs et libellés sont en français.

Notes :
- Les taux (croissance, actualisation) sont exprimés en fractions (ex.: 0.02 = 2%).
- Heures supplémentaires : le complément de rémunération est de 0.5× le salaire de base
  par heure supplémentaire (car le 1.5× inclut déjà 1.0×).
- L'horizon d'analyse est de 5 ans conformément à l'énoncé.
"""

VUEDENSEMBLE = {
    # Croissance annuelle
    "taux_croissance_couts": 0.02,      # 2 %
    "taux_croissance_revenus": 0.15,    # 15 %

    # Main-d'œuvre
    "heures_moyennes_par_mois": 130,    # heures/mois
    "facteur_majoration_heures_sup": 0.5,  # +0.5× du salaire de base par h. sup (=> 1.5× au total)

    # Actualisation / horizon
    "taux_actualisation": 0.04,         # 4 % (VAN)
    "duree_analyse_ans": 5,             # années
}
