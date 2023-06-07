# 2023-INT-StageM1
_Repository des notebooks et des autres éléments de mon stage de M1._

## Semaine 1: Décoding de Berens appliqué aux données d'Hugo
_cf._ https://github.com/alexandre-laine/ADAM_obv1replication

Berens, P., Ecker, A. S., Cotton, R. J., Ma, W. J., Bethge, M., & Tolias, A. S. (2012). A Fast and Simple Population Code for Orientation in Primate V1. Journal of Neuroscience, 32(31), 10618‑10626. https://doi.org/10.1523/JNEUROSCI.1335-12.2012

Ladret, H. J., Cortes, N., Ikan, L., & Perrinet, L. U. (s. d.). 1 Resilience to sensory variance in the primary visual 2 cortex.

## Semaine 2: Peut-on améliorer la performance du decoding?

Q: introduction d'une Egalisation d'histogramme dans le decoding?

### étude de l'égalisation d'histogramme 

* _Déroulement à suivre :_
1) Génération de donnée selon une loi de Poisson (scipy.stats.poisson)
2) Réalisation de l'histogramme de probabilité (np.histogram $\rightarrow$ plt.plot)
3) Représentation de la courbe des densités de probabilités (np.cumsum)
4) Interpolation...
5) Passage des données générées dans l'interpolation
6) Observation de la répartition des donnés après l'interpolation

_biblio :_ https://arxiv.org/pdf/1701.06859.pdf

*  Notebook $\rightarrow$ **Egalisation d'histogramme** : [Equa_histo.ipynb](./Equa_histo.ipynb)

## Semaine 3: decoding d'autres datasets?

* https://github.com/CONECT-INT/2022_CENTURI-SummerSchool/tree/main/dev
* 
