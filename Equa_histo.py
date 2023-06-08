"""

alexandre-laine
2023/06/08/11:11

"""

import numpy as np #Usuel
import matplotlib.pyplot as plt #Représentations graphiques

#Calcul la distribution des  données
def make_distrib(ni=[],nbr_bins=20,ni_max=20):
    p_ni,bin_ni=np.histogram(ni,bins=nbr_bins,range=(0,ni_max),density=True)
    bin_mid_ni=1/2*(np.sum((bin_ni[1:],bin_ni[:-1]),axis=0))
    return p_ni,bin_ni,bin_mid_ni

#Représente la distribution des données
def hist_distrib(p_ni=[],bin_mid_ni=[],bin_ni=[],nbr_bins=20,ni_max=20):    
    fig,ax=plt.subplots(figsize=(10,5))
    ax.bar(x=bin_mid_ni,height=p_ni,width=(ni_max/nbr_bins),color="red")
    ax.vlines(x=[x for x in bin_ni],ymin=0,ymax=p_ni.max()+0.2*p_ni.max(),color="black",linestyle="dashed",lw=1)
    ax.set_xticks(bin_mid_ni)
    ax.set_xticklabels([round(x) for x in np.linspace(0,ni_max-1,nbr_bins)])
    ax.set_xlim(0,ni_max)
    ax.set_xlabel("Taux de décharge (en Hz)")
    ax.set_ylabel("Probabilité d'occurence")
    ax.set_title("Distribution des taux de décharges")
    fig.savefig(f"/home/alexandre/Documents/Equalisation_histogramme/fig/histogramme_distribution_bin{nbr_bins}.png")
    plt.tight_layout()
    plt.show()

#Calcul la cumulation des probabilitées d'occurence
def make_cumul(p_ni=[]):
    P_ni=np.cumsum(p_ni)
    return P_ni

#Représente la cumulation des probabilitées d'occurence
def courbe_cumul(P_ni=[],bin_ni=[],nbr_bins=20,ni_max=20):
    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(bin_ni[:-1],P_ni)
    ax.set_xticks(bin_ni[:-1])
    ax.set_xticklabels([round(x,0) for x in np.linspace(0,ni_max-1,nbr_bins)])
    ax.set_xlim(bin_ni.min(),bin_ni[:-1].max())
    ax.set_xlabel("Taux de décharge (en Hz)")
    ax.set_ylim(-0.05,1.05)
    ax.set_ylabel("Probabilité cumulative d'occurence")
    ax.set_title("Courbe cumulative des probabilités")
    fig.savefig(f"/home/alexandre/Documents/Equalisation_histogramme/fig/courbe_cumulative_bin{nbr_bins}.png")
    plt.tight_layout()
    plt.show()

#Calcul l'interpolation des données à partir de la courbe de cumulation
def make_interp(ni=[],bin_ni=[],P_ni=[],nbr_bins_interp=5):
    ni_interp=np.interp(ni,bin_ni[:-1],P_ni)
    p_ni_interp,bin_ni_interp=np.histogram(ni_interp,bins=nbr_bins_interp,range=(0,1),density=True)
    bin_mid_ni_interp=1/2*(np.sum((bin_ni_interp[1:],bin_ni_interp[:-1]),axis=0))
    return p_ni_interp,bin_mid_ni_interp,bin_ni_interp

#Représente l'histogramme egalisé
def hist_interp(p_ni_interp=[],bin_ni_interp=[],bin_mid_ni_interp=[],nbr_bins_interp=10):
    fig,ax=plt.subplots(figsize=(10,5))
    ax.bar(x=bin_mid_ni_interp,height=p_ni_interp,width=1/(nbr_bins_interp),color="red")
    ax.vlines(x=[x for x in bin_ni_interp],ymin=0,ymax=p_ni_interp.max()+0.1*p_ni_interp.max(),color="black",linestyle="dashed",lw=1)
    ax.set_xticks(np.linspace(bin_mid_ni_interp[0],bin_mid_ni_interp[-1],nbr_bins_interp),)
    ax.set_xticklabels([round(x,2) for x in np.linspace(0,1,nbr_bins_interp)])
    ax.set_xlim(bin_ni_interp[0],bin_ni_interp[-1])
    ax.set_title("Histogramme Egalisé")
    ax.set_xlabel("Probabilité d'occurence")
    ax.set_ylabel("Densité d'occurence")
    fig.savefig(f"/home/alexandre/Documents/Equalisation_histogramme/fig/histogramme_egalise_bin{nbr_bins_interp}.png")
    plt.tight_layout()
    plt.show()

#Génère l'ensemble de l'analyse
def run_equa_histo(ni,nbr_bins=20,ni_max=20,nbr_bins_interp=10):
    p_ni,bin_ni,bin_mid_ni=make_distrib(ni=ni,nbr_bins=nbr_bins,ni_max=ni_max)
    hist_distrib(p_ni=p_ni,bin_mid_ni=bin_mid_ni,bin_ni=bin_ni,nbr_bins=nbr_bins,ni_max=ni_max)
    P_ni=make_cumul(p_ni=p_ni)
    courbe_cumul(P_ni=P_ni,bin_ni=bin_ni,nbr_bins=nbr_bins,ni_max=ni_max)
    p_ni_interp,bin_mid_ni_interp,bin_ni_interp=make_interp(ni=ni,bin_ni=bin_ni,P_ni=P_ni,nbr_bins_interp=nbr_bins_interp)
    hist_interp(p_ni_interp=p_ni_interp,bin_ni_interp=bin_ni_interp,bin_mid_ni_interp=bin_mid_ni_interp,nbr_bins_interp=nbr_bins_interp)