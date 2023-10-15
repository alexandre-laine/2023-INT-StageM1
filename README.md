# 2023-INT-Stage-M1
_Repository de mon stage de M1 réalisé au sein de l'équipe NeOpTo de l'institut de Neurosciences de la TImone (INT) sous la direction de [Laurent U. Perrinet](https://github.com/laurentperrinet)_

## Organisation :
Ces dossiers regroupent la contribution que j'ai pu apporter durant mon stage sur le travail réalisé par Hugo Ladret concernant le décoding d'activités enregistrées au sein du cortex visuel primaire d'un chat lors de la présentation de différents stimulus. \
Mon objectif a été d'ajouter une phase de transformations non-linéaires afin de modifier le support du "décodeur" et ainsi d'améliorer ses performances. Cette phase se composait tout d'abord d'une égalisation d'histogramme et du passage au sein d'une fonction d'erreur inverse.

Les fichiers principaux sont :
- le [notebook principal](M1_stage_2023_AL.ipynb) reprenant tout le déroulé du décoding.
- le [poster](Poster_LAINE_Alexandre_NeuroMarseille_Day_2023.pdf) présenté lors de la journée NeuroMarseille 2023.

## Résumé du stage :
- Semaine 1 : décoding de Berens appliqué aux données d'[Hugo Ladret](https://github.com/hugoladret)

_biblio :_ \
Berens, P., Ecker, A. S., Cotton, R. J., Ma, W. J., Bethge, M., & Tolias, A. S. (2012). A Fast and Simple Population Code for Orientation in Primate V1. Journal of Neuroscience, 32(31), 10618‑10626. https://doi.org/10.1523/JNEUROSCI.1335-12.2012 \
Ladret, H. J., Cortes, N., Ikan, L., Chavane, F., Casanova, C., & Perrinet, L. U. (2023). Cortical recurrence supports resilience to sensory variance in the primary visual cortex. Communications Biology, 6(1), 667. https://doi.org/10.1038/s42003-023-05042-3

- Semaine 2 et 3 : peut-on améliorer la performance du décoding ?

_biblio :_ \
Bishop, C. M. (2006). Pattern recognition and machine learning. Springer. \
Cristóbal, G., Perrinet, L., & Keil, M. S. (Éds.). (2015). Biologically Inspired Computer Vision : Fundamentals and Applications (1ʳᵉ éd.). Wiley. https://doi.org/10.1002/9783527680863

- Semaine 4 : utilisation du décoding pour différencier l'activité évoquée et non-évoquée !


## Autre :
Il est aussi possible de retrouver le travail réalisé dans la continuité du stage :
- L'[analyse](Analyse_stage_AL.ipynb) des scores de décoding obtenue.
- D'[autres transformations](Autres_transformations_AL.ipynb) ainsi que leurs influences.
- L'ensemble des [figures](figs) obtenues au cours et après mon stage.

## Nota bene
Les données brutes d'Hugo sont accessibles [ici](https://figshare.com/articles/dataset/Data_for_Ladret_et_al_2023_Cortical_recurrence_supports_resilience_to_sensory_variance_in_the_primary_visual_cortex_/23366588), et le code des phases de préprocessing et postprocessing sont accessible sur cet autre [repository](https://github.com/hugoladret/variance-processing-V1).  Les données produites au cours de mon stage sont en partie accessible mais pas en totalité, si besoin, n'hésitez pas à contacter Laurent, Hugo ou moi-même.

## TODOs

* utiliser `os.path.join` partout où on peut -> ok
* ajouter le lien pour télécharger les données (et le repo ?) d'hugo -> ok
* nbdiff-web in `pip install nbdime` 
