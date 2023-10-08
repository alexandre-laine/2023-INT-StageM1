#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 14:44:11 2019

@author: hugo
"""

import params as prm
import utils 
import utils_single_neuron as sn_utils 
import utils_decoding as dec_utils
import numpy as np 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_val_predict
import os 
import matplotlib.pyplot as plt 
from tqdm import tqdm 

from sklearn.model_selection import ParameterGrid
from joblib import Parallel, delayed
from scipy.stats import permutation_test
from scipy import stats

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42



def make_theta_decoding_all() :    
    print('First run to get the data')
    
    # DECODING  ------------------------------------
    print('Doing the decoding on all the neurons with K-fold = %s' % prm.n_splits)
    if not os.path.exists('./data/%s/decoding_theta_all_kfold.npy' % prm.postprocess_name):
        kfold_scores = np.zeros((len(prm.B_thetas), len(prm.timesteps), prm.n_splits)) 
        for ibt, bt in enumerate(prm.B_thetas) :
            print('Running for btheta = %s' % (bt*180/np.pi))
            # Data
            if not os.path.exists('./data/%s/decoding_theta_bt%s_data.npy' % (prm.postprocess_name, ibt)):
                data, labels, le = dec_utils.par_load_data(timesteps = prm.timesteps, target_clusters = prm.cluster_list,
                                                        target_btheta = bt, target_theta = None, data_type = 'one_bt',
                                                        disable_tqdm = False
                                                        )
                np.save('./data/%s/decoding_theta_bt%s_data.npy' % (prm.postprocess_name, ibt), [data, labels, le])
            else : 
                data, labels, le = np.load('./data/%s/decoding_theta_bt%s_data.npy' % (prm.postprocess_name, ibt), allow_pickle = True)

            # Classifying
            logreg = LogisticRegression(**prm.opts_LR)

            for ibin in tqdm(range(data.shape[0]), desc = 'Decoding') :
                scores = cross_val_score(logreg, data[ibin,:,:], labels, 
                                        cv = prm.n_splits, 
                                        scoring = 'balanced_accuracy')
                kfold_scores[ibt, ibin, :] = scores

        np.save('./data/%s/decoding_theta_all_kfold.npy'% prm.postprocess_name, kfold_scores)
    else :
        kfold_scores = np.load('./data/%s/decoding_theta_all_kfold.npy'% prm.postprocess_name)
    
    
    # PLOTTING  ------------------------------------
    fig, ax = plt.subplots(figsize = (9,6))
    plot_bthetas = [7,  0]
    for ibt in plot_bthetas :
        kfold_means = np.asarray([x.mean() for x in kfold_scores[ibt]])
        kfold_stderr = np.asarray([x.std() for x in kfold_scores[ibt]])
        
        ax.plot(prm.timesteps + prm.win_size, kfold_means, color = prm.colors[ibt])
        ax.fill_between(prm.timesteps + prm.win_size,
                    kfold_means + kfold_stderr, kfold_means - kfold_stderr,
                    facecolor = prm.colors[ibt], edgecolor = None, alpha = .7,
                    label = r'B$_\theta$ = %.1f°' % (prm.B_thetas[ibt] * 180/np.pi))
        mod_t = prm.timesteps + prm.win_size
        print('Btheta %.2f - max at time %.2fs = %.2f' % (prm.B_thetas[ibt], mod_t[np.argmax(kfold_means)],
                                                np.max(kfold_means)))
        
    ax.hlines(.95, 0., .3, color = 'k', linewidth = 4)
    ax.axhline(1/12, c = 'gray', linestyle = '--')

    ax.set_xlabel('PST (ms)', fontsize = 18)
    ax.set_ylabel('Classification accuracy', fontsize = 18)
    ax.tick_params(axis='both', which='major', labelsize=14)
    labs = np.round(ax.get_xticks().tolist(),1)
    ax.set_xticklabels((labs*1000).astype(np.int16))
    yticks = np.linspace(0, 1., 6)
    ax.set_yticks(yticks)
    ax.set_yticklabels(np.round(yticks,1))
    ax.set_xlim(prm.timesteps[0]+prm.win_size, prm.timesteps[-1]+prm.win_size)
    ax.set_ylim(0, 1.)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc = (.025, .65), frameon = False, fontsize = 14, markerscale = 2, ncol = 1)
    leg = ax.get_legend()
    leg.legendHandles[0].set_color(prm.colors[7])
    leg.legendHandles[0].set_alpha(1)
    leg.legendHandles[1].set_color(prm.colors[0])
    leg.legendHandles[1].set_alpha(1)
    
    fig.tight_layout()
    fig.savefig('./figs/decoding_theta_all_timesteps.pdf', bbox_inches='tight', dpi=200, transparent=True)
    plt.show(block = prm.block_plot)
    plt.close()

def statistic(x, y, axis):
            return np.mean(x, axis=axis) - np.mean(y, axis=axis)
# --------------------------------------------------------------
# Decoding of orientation for the two groups
# --------------------------------------------------------------
def make_theta_decoding_groups(params, data, labels, le):
    loop_n_bootstrap = params['n_bootstraps']
    loop_n_subgroups = params['n_subgroups']
    loop_seed = params['loop_seeds']
    
    # DECODING --------------------------------------------------
    #print('LOOP : %s n bootstrap ; %s n subgroups ; %s seed' % (loop_n_bootstrap, loop_n_subgroups, loop_seed))
    bootstrapped_results = np.zeros((2, loop_n_bootstrap, len(prm.timesteps))) # we only report the mean per kfold
    mean_overlapped = 0
    for ibootstrap in range(loop_n_bootstrap):
        # Randomly pick subgroups in each population
        np.random.seed(loop_seed+ibootstrap)
        picked_res = np.random.choice(prm.tuned_lst, size = loop_n_subgroups, replace = True)
        picked_vul = np.random.choice(prm.untuned_lst, size = loop_n_subgroups, replace = True)
        
        idxs_res = [list(prm.cluster_list).index(x) for x in picked_res]
        idxs_vul = [list(prm.cluster_list).index(x) for x in picked_vul]
            
        # Fetch the main data, do logreg, and so on
        data_res = data[:, :, idxs_res]
        data_vul = data[:, :, idxs_vul]

        # Classifying
        logreg = LogisticRegression(**prm.opts_LR)
        
        for ibin in range(15,data.shape[0]) :
            scores_res = cross_val_score(logreg, data_res[ibin,:,:], labels, 
                                        cv = prm.n_splits, 
                                        scoring = 'balanced_accuracy')
            scores_vul = cross_val_score(logreg, data_vul[ibin,:,:], labels,
                                        cv = prm.n_splits,
                                        scoring='balanced_accuracy')
            bootstrapped_results[0, ibootstrap, ibin] = np.mean(scores_res)
            bootstrapped_results[1, ibootstrap, ibin] = np.mean(scores_vul)
    
    # Statistical tests
    pvals_array = np.ones_like(prm.timesteps)
    for i in range(15,data.shape[0]) :
        p, val = stats.wilcoxon(bootstrapped_results[0,:, i], bootstrapped_results[1,:, i],
                                alternative = 'two-sided')
        pvals_array[i] = p
        
            
    signif_total = 0
    for i, pval in enumerate(pvals_array[:-1]) :
        if pval <0.05 : # don't care about  pre-stim
            signif_total+=1
            

        
    if signif_total < 40 :
        # PLOTTING --------------------------------------------------------
        fig, ax = plt.subplots(figsize = (8,5))
        
        # Untuned bootstrapping
        bootstrap_mean = bootstrapped_results[1,:,:].mean(axis = 0)
        bootstrap_std = bootstrapped_results[1,:,:].std(axis = 0)
        
        ax.plot(prm.timesteps + prm.win_size, bootstrap_mean, color = prm.col_untuned)
        ax.fill_between(prm.timesteps + prm.win_size,
                    bootstrap_mean + bootstrap_std, bootstrap_mean - bootstrap_std,
                    facecolor = prm.col_untuned, edgecolor = None, alpha = .7,
                    label = prm.name_untuned)
        
        # Tuned bootstrapping
        bootstrap_mean = bootstrapped_results[0,:,:].mean(axis = 0)
        bootstrap_std = bootstrapped_results[0,:,:].std(axis = 0)
        
        ax.plot(prm.timesteps + prm.win_size, bootstrap_mean, color = prm.col_tuned)
        ax.fill_between(prm.timesteps + prm.win_size,
                    bootstrap_mean + bootstrap_std, bootstrap_mean - bootstrap_std,
                    facecolor = prm.col_tuned, edgecolor = None, alpha = .7,
                    label = prm.name_tuned)
        
        for i, pval in enumerate(pvals_array[:-1]) :
            if pval <0.05 : # don't care about  pre-stim
                ax.axvspan(prm.timesteps[i]+prm.win_size, prm.timesteps[i+1]+prm.win_size, alpha = .3,
                        facecolor = 'gray', edgecolor = 'None',
                        zorder = -20)
        
        ax.hlines(.95, 0., .3, color = 'k', linewidth = 4)
        ax.axhline(1/12, c = 'gray', linestyle = '--')
        
        ax.set_xlabel('PST (ms)', fontsize = 18)
        ax.set_ylabel('Classification accuracy', fontsize = 18)
        ax.tick_params(axis='both', which='major', labelsize=14)
        labs = np.round(ax.get_xticks().tolist(),1)
        ax.set_xticklabels((labs*1000).astype(np.int16))
        yticks = np.linspace(0, 1., 6)
        ax.set_yticks(yticks)
        ax.set_yticklabels(np.round(yticks,1))
        ax.set_xlim(prm.timesteps[0]+prm.win_size, prm.timesteps[-1]+prm.win_size)
        ax.set_ylim(0, 1.)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(loc = (.025, .75), frameon = False, fontsize = 14, markerscale = .2)
        fig.tight_layout()
        fig.savefig('./figs/LOOP_theta_npop%s_nseed%s_bootstrap%s.pdf' % ( loop_n_subgroups, loop_seed, loop_n_bootstrap),
                    bbox_inches='tight', dpi=50, transparent=True)
        plt.close()
        
    
    return [loop_seed, signif_total]
        
        
        
make_theta_decoding_all() # run one time to get the data on the disk

data, labels, le = np.load('./data/%s/decoding_theta_bt7_data.npy' % (prm.postprocess_name), allow_pickle = True)
    
paramgrid = {'n_bootstraps' : [5],
            'n_subgroups' : [100],
            'loop_seeds' : [43, 44, 45, 46,50, 61, 81,93, 94, 192, 193, 220, 221, 223,
                            298, 317, 465, 468, 502, 880, 1024, 2060, 2518, 4026, 4048,
                            4197, 30732, 19963418, 19966725, 19963419, 19969074, 19967568],
}

results = Parallel(n_jobs = -1)(delayed(make_theta_decoding_groups)(params, data, labels, le) for params in tqdm(ParameterGrid(paramgrid)))
print(sorted(results, key=lambda x: x[1], reverse=False)[:100])
print('Highest overlaping', max([x[1] for x in results]))