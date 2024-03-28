#!/usr/bin/env python
# coding: utf-8

# ## import libraries

# In[1]:


import os
import time
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import pairwise_distances_argmin_min

import pm4py
from pm4py import read_xes
from pm4py.algo.evaluation import algorithm
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to, remove_transition



# In[2]:


import warnings
warnings.filterwarnings('ignore')

# Set the maximum number of rows to display
pd.set_option('display.max_rows', 1000)  # Change 1000 to your desired value


# ## read dataset

# In[3]:

def hello():
    print('hello')
def get_log_stats(log):
    # event log columns
    all_columns = log.columns
    print("\nEvent log have total {} columns and {} log activities".format(log.shape[1], log.shape[0]))
    print("======================================================")
    
    print("\nEvent Log have the follwing columns:")
    print("====================================")
    print(list(log.columns))
    
def read_log(xes_file_path):
    # Import the XES file as an event log
    event_log = read_xes(xes_file_path)
    return event_log


# ## split log

# In[4]:


def split_log(log, test_size=0.30, shuffle=False):
    train_log, test_log = train_test_split(log, test_size=test_size, random_state=42, shuffle=shuffle)
    return train_log, test_log


# ## train and evaluate Petri Net

# In[5]:


def train_evaluate_petri_net(training_log, testing_log):
    net, im, fm = pm4py.discover_petri_net_inductive(training_log, noise_threshold=0.2)

    q_o = algorithm.apply(test_log, net, im, fm)

    fitness = round(q_o['fitness']['average_trace_fitness'],3)
    prec = round(q_o['precision'],3)
    gen = round(q_o['generalization'],3)
    simp = round(q_o['simplicity'],3)
    
    # fitness = pm4py.fitness_token_based_replay(testing_log, net, im, fm)
    # prec = pm4py.precision_token_based_replay(testing_log, net, im, fm)
    # gen = generalization_evaluator.apply(testing_log, net, im, fm)
    # simp = simplicity_evaluator.apply(net)
    
    print("\n========================")
    print("Fitness: ", fitness)
    print("Precision: ", prec)
    print("Generalization: ", gen)
    print("Simplicity: ", simp)
    print("========================\n")

    return net, im, fm


# ## save and plot models

# In[6]:


def __remove_silent_transitions(net):
    silent_transitions = [transition for transition in net.transitions if transition.label is None]

    # for t in silent_transitions:
    #     # Remove arcs connected to the invisible transition
    #     for arc in list(net.arcs):
    #         if arc.target == t or arc.source == t:
    #             net.arcs.remove(arc)
    #     # Remove the transition itself
    #     net.transitions.remove(t)

    for trans in silent_transitions:
        in_arcs = trans.in_arcs
        for arc in in_arcs:
            place = arc.source
            place.out_arcs.remove(arc)
            net.arcs.remove(arc)
        out_arcs = trans.out_arcs
        for arc in out_arcs:
            place = arc.target
            place.in_arcs.remove(arc)
            net.arcs.remove(arc)
        net.transitions.remove(trans)

    return net

def plot_petri_net(net, im, fm, remove_silent=False, save_graph=False, graph_name="Petri_Net.png"):
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)

    net = __remove_silent_transitions(net) if remove_silent else net
        
    pn_visualizer.save(gviz, graph_name) if save_graph else None

def plot_bpmn(net, im, fm, save_graph=False, graph_name="BPMN.png"):
    bpmn_graph = pm4py.convert_to_bpmn(net, im, fm)

    gviz = bpmn_visualizer.apply(bpmn_graph)
    bpmn_visualizer.view(gviz)

    bpmn_visualizer.save(gviz, graph_name) if save_graph else None


# ## Create Session

# In[7]:


def log_preprocessing(event_log):
    event_log['time:timestamp'] = event_log['time:timestamp'].apply(lambda x : str(x))

    event_log['time:timestamp'] = event_log['time:timestamp'].apply(lambda x : x.split('.')[0])
    event_log['time:timestamp'] = event_log['time:timestamp'].apply(lambda x : x.split('+')[0])

    format_string = '%Y-%m-%d %H:%M:%S'
    event_log['time:timestamp'] = event_log['time:timestamp'].apply(lambda x : datetime.strptime(x, format_string))

    return event_log
    
def create_session(log, session_duration):
    log = log_preprocessing(log)
    
    customers = list(event_log['case:concept:name'].unique())
    session_df = pd.DataFrame(columns=['case:concept:name', 'lifecycle:transition','concept:name', 'time:timestamp',  'Session'])

    for customer in customers:
        customer_trace = event_log[event_log['case:concept:name'] == customer]
        customer_trace = customer_trace.sort_values('time:timestamp')
        customer_trace['Session'] = (customer_trace['time:timestamp'] - 
                                     customer_trace['time:timestamp'].shift(1)).gt(pd.Timedelta(minutes=session_duration)).cumsum() + 1
        session_df = pd.concat([session_df, customer_trace], ignore_index=True)

    return session_df


# ## Frequency Based Encoding

# In[8]:


def freq_encoding(session_log):
    # Perform one-hot encoding
    one_hot_encoded = pd.get_dummies(session_log['concept:name'], prefix='activity')
    
    # Replace frequency with 1 where frequency is not 0
    one_hot_encoded = one_hot_encoded.applymap(lambda x: 1 if x > 0 else 0)
    
    # Concatenate one-hot encoded columns with original DataFrame
    df_encoded = pd.concat([session_log[['case:concept:name', 'lifecycle:transition', 'Session']], one_hot_encoded], axis=1)
    
    # Group by customer_id and session
    # df_encoded['time:timestamp'] = df_encoded['time:timestamp'].astype(str)
    df_grouped = df_encoded.groupby(['case:concept:name', 'lifecycle:transition', 'Session']).sum().reset_index()

    return df_grouped


# ## Clustering

# In[9]:


def __clustering_preprocessing(endoded_log):
    # Filter columns
    activity_columns = [col for col in endoded_log.columns if col.startswith('activity_')]
    
    # Select only the columns that start with 'activity_'
    features = encoded_log[activity_columns]

    # Standardize features
    X = StandardScaler().fit_transform(features)

    # Convert the transformed ndarray back to a DataFrame
    # You need to retain the column names and index of your original DataFrame
    transformed_df = pd.DataFrame(X, columns=features.columns, index=features.index)

    return transformed_df
    

def elbow_clustering(encoded_log):

    features_log = __clustering_preprocessing(encoded_log)
    
    # Compute DBSCAN
    eps_values = np.linspace(0.1, 3.0, num=20)
    silhouette_scores = []
    
    for eps in eps_values:
        dbscan = DBSCAN(eps=eps)
        labels = dbscan.fit_predict(features_log)
        silhouette_scores.append(silhouette_score(features_log, labels))
    
    # Plotting Elbow Method
    plt.plot(eps_values, silhouette_scores, marker='o')
    plt.xlabel('Eps')
    plt.ylabel('Silhouette Score')
    plt.title('DBSCAN Elbow Method')
    plt.grid(True)
    plt.show()


def DBSACN_Clusteirng(encoded_log, epsilon_value=2, minimum_samples=12):

    features_log = __clustering_preprocessing(encoded_log)

    # Apply DBSCAN clustering
    dbscan_model = DBSCAN(eps=epsilon_value, min_samples=minimum_samples)  # Adjust eps and min_samples based on your data
    encoded_log['DBSCAN_Cluster'] = dbscan_model.fit_predict(features_log)

    labels = dbscan_model.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    
    print('\nEstimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)
    
    print("\n", encoded_log['DBSCAN_Cluster'].value_counts(), "\n")

    return encoded_log

def remove_noise_samples(encoded_log):
    # Assuming features_df is a DataFrame containing the feature vectors and DBSCAN_Cluster column
    # Reset the index to ensure proper alignment of indices
    # encoded_log = encoded_log.reset_index(drop=True)

    features_log = __clustering_preprocessing(encoded_log)
    features_log['DBSCAN_Cluster'] = encoded_log['DBSCAN_Cluster']
    
    # Find noise indices
    noise_indices = encoded_log[encoded_log['DBSCAN_Cluster'] == -1].index
    
    # Find the nearest cluster for each noise point
    nearest_cluster_indices, _ = pairwise_distances_argmin_min(
        features_log.iloc[noise_indices, :-1],  # Exclude the cluster label column
        features_log[features_log['DBSCAN_Cluster'] != -1].iloc[:, :-1]  # Exclude noise points
    )
    
    # Merge noise samples into the nearest cluster
    encoded_log.loc[noise_indices, 'DBSCAN_Cluster'] = encoded_log.loc[
        encoded_log['DBSCAN_Cluster'] != -1, 'DBSCAN_Cluster'
    ].iloc[nearest_cluster_indices].values
    
    # Check if there are still noise points
    remaining_noise_indices = encoded_log[encoded_log['DBSCAN_Cluster'] == -1].index
    if len(remaining_noise_indices) > 0:
        print(f"T\nhere are still {len(remaining_noise_indices)} noise points remaining.\n")
    else:
        print("\nAll noise points have been assigned to the nearest cluster.\n")

    print("\n", encoded_log['DBSCAN_Cluster'].value_counts(), "\n")
    return encoded_log


# ## Plotting

# In[10]:


def plot_heatmap(encoded_log):

    features_log = __clustering_preprocessing(encoded_log)
    features_log['DBSCAN_Cluster'] = encoded_log['DBSCAN_Cluster']
    features_df = features_log
    
    # Calculate mean of each feature within each cluster
    cluster_means = (features_df.groupby('DBSCAN_Cluster').mean()).T
    
    # Calculate correlation matrix
    correlation_matrix = cluster_means.corr()
    
    # Select top 10 most correlated columns for each cluster
    top_correlated_columns = {}
    for cluster_label in correlation_matrix.columns:
        top_correlated_columns[cluster_label] = correlation_matrix[cluster_label].nlargest(20).index.tolist()
    
    # Create a DataFrame containing only the top 10 most correlated columns for each cluster
    cluster_means_top_correlated = pd.DataFrame()
    for cluster_label, columns in top_correlated_columns.items():
        cluster_means_top_correlated[cluster_label] = cluster_means[cluster_label][columns]
    
    # Plot heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(cluster_means_top_correlated, annot=True, cmap="hot", fmt=".2f", facecolor='white')
    plt.title('Heatmap of Top 10 Most Correlated Columns with Each Feature')
    plt.xlabel('Cluster')
    plt.ylabel('Feature')
    plt.show()


# ## Abstract Model

# In[11]:


# Define a function to label the activities as 'start' and 'end'
def __label_activity(group):
    # print(group)
    if len(group) == 1:
        group.loc[group.index[0], 'Activity'] = 'start'
        new_activity = group.iloc[0].copy()  # Copy the first activity
        new_activity['Activity'] = 'end'
        return pd.concat([group, pd.DataFrame([new_activity])], ignore_index=True)
    else:
        group.loc[group.index[0], 'Activity_Status'] = 'start'
        group.loc[group.index[-1], 'Activity_Status'] = 'end'
        return group

def abstract_log_preprocessing(session_log, cluster_log, cluster_map):
    # Perform inner join
    merged_log = pd.merge(session_log, cluster_log, on=['case:concept:name', 'Session', 'lifecycle:transition'], how='inner')
    
    merged_log = merged_log[['case:concept:name', 'Session', 'lifecycle:transition', 'time:timestamp', 'concept:name', 'DBSCAN_Cluster']]
    
    merged_log['DBSCAN_Cluster'] = merged_log['DBSCAN_Cluster'].replace(cluster_map)
    merged_log.rename({'concept:name':'log_activity', 'DBSCAN_Cluster':'abstract_activity'}, axis=1, inplace=True)

    merged_log = merged_log.sort_values(by=['case:concept:name', 'Session', 'time:timestamp'])
    
    # Group the DataFrame by 'CustomerID' and 'Session', then apply the function
    new_df = merged_log.groupby(['case:concept:name', 'Session']).apply(__label_activity).reset_index(drop=True)
    
    # Select only the 'start' and 'end' activities
    merged_log = new_df[new_df['Activity_Status'].isin(['start', 'end'])]

    activity_log = merged_log[['case:concept:name', 'time:timestamp','log_activity', 'abstract_activity', 'Activity_Status']]
    activity_log.rename({'log_activity':'concept:name'}, axis=1, inplace=True)
    
    abstract_log = merged_log[['case:concept:name', 'time:timestamp','abstract_activity', 'Activity_Status']]
    abstract_log.rename({'abstract_activity':'concept:name'}, axis=1, inplace=True)

    return activity_log, abstract_log


# In[47]:


def add_invisible_transitions(net, im, fm, in_place, out_place):
    ip = [place for place in im][0]
    fp = [place for place in fm][0]

    transition = PetriNet.Transition("tau")
    net.transitions.add(transition)
    add_arc_from_to(transition, ip, net)
    add_arc_from_to(in_place, transition, net)
    
    transition = PetriNet.Transition("tau")
    net.transitions.add(transition)
    add_arc_from_to(fp, transition, net)
    add_arc_from_to(transition, out_place, net)


def merge_subprocesses(train_abstract_log, train_activity_log, test_activity_log):
    
    noise_threshold = 0.2
    
    print(f'Abstracted model is started to create at {datetime.fromtimestamp(time.time())}.')
    
    train_abstract_log = train_abstract_log[['case:concept:name','time:timestamp','concept:name']]
    a_net, a_im, a_fm = pm4py.discover_petri_net_inductive(train_abstract_log, noise_threshold)
        
    pm4py.write_pnml(a_net, a_im, a_fm, "_AbstractedModel.pnml")
    pm4py.save_vis_petri_net(a_net, a_im, a_fm, "_AbstractedModel.pdf")
    
    print(f'\nSubprocesses are started to merge at {datetime.fromtimestamp(time.time())}')
    
    low_level_activities = {t for t in a_net.transitions if t.label is not None}
    for i, a in enumerate(low_level_activities):
        print(f"Cluster {i}, High level activity: {a.label}  is merging at {datetime.fromtimestamp(time.time())}.")
        for arc in a.in_arcs:
            in_place = arc.source
        for arc in a.out_arcs:
            out_place = arc.target
        
        cluster_number = a.label[-1]
        sub_log = train_activity_log[train_activity_log['abstract_activity'] == a.label]
        train_activity_log_sub = sub_log[['case:concept:name','time:timestamp','concept:name', 'abstract_activity']]

        net, im, fm = pm4py.discover_petri_net_inductive(train_activity_log_sub, noise_threshold)
        add_invisible_transitions(net, im, fm, in_place, out_place)
        
        a_net.transitions.update(net.transitions)
        a_net.places.update(net.places)
        a_net.arcs.update(net.arcs)
        remove_transition(a_net, a)
        
    # pm4py.write_pnml(a_net, a_im, a_fm, os.path.join(abstracted_logs_folder, str(original_log_name+"_MergedModel.pnml")))
    # pm4py.save_vis_petri_net(a_net, a_im, a_fm, os.path.join(abstracted_logs_folder, str(original_log_name+"_MergedModel.pdf")))

    q_o = algorithm.apply(test_activity_log, a_net, a_im, a_fm)
    fitness = round(q_o['fitness']['average_trace_fitness'],3)
    q_o = algorithm.apply(train_activity_log, a_net, a_im, a_fm)
    prec = q_o['precision']
    gen = round(q_o['generalization'],3)
    simp = round(q_o['simplicity'],3)
    
    # fitness = pm4py.fitness_token_based_replay(testing_log, net, im, fm)
    # prec = pm4py.precision_token_based_replay(testing_log, net, im, fm)
    # gen = generalization_evaluator.apply(testing_log, net, im, fm)
    # simp = simplicity_evaluator.apply(net)
    
    print("\n========================")
    print("Fitness: ", fitness)
    print("Precision: ", prec)
    print("Generalization: ", gen)
    print("Simplicity: ", simp)
    print("========================\n")

    return a_net, a_im, a_fm
