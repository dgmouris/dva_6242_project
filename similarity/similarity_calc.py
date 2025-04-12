import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def clean_data(df, situation):
    """
    Clean the dataset filtered to the situation that the closest similarity POIUs are being
    calculated for
    
    Args:
        df (pd.DataFrame): raw shot data dataframe
        situation (string): situation on the ice to be used (5on5, 5on4, etc.)
    Returns:
        cleaned_df (pd.DataFrame): Final shot data dataframe to be used with clustering algorithm
    """
    df = df[df.situation == situation].copy()
    
    offense_cols = [
        'shooting_poiu_id', 'xGoal', 'goal','shotDistance',
        'shotWasOnGoal'
    ]

    defense_cols = [
        'defending_poiu_id', 'xGoal', 'goal', 'shotDistance',
        'shotWasOnGoal',
    ]

    df_encoded = pd.get_dummies(df, columns=['shotType'])

    offensive_stats = (
        df_encoded[offense_cols + [col for col in df_encoded.columns if col.startswith('shotType_')]]
        .groupby(['shooting_poiu_id'])
        .agg(['mean', 'sum']) 
    )

    defensive_stats = (
        df_encoded[defense_cols + [col for col in df_encoded.columns if col.startswith('shotType_')]]
        .groupby(['defending_poiu_id'])
        .agg(['mean', 'sum'])
    )

    offensive_stats.columns = [f"{col[0]}_{col[1]}" for col in offensive_stats.columns]
    offensive_stats['num_shots'] = df.groupby('shooting_poiu_id').size()
    offensive_stats.reset_index(inplace=True)

    defensive_stats.columns = [f"{col[0]}_{col[1]}" for col in defensive_stats.columns]
    defensive_stats['num_shots'] = df.groupby('defending_poiu_id').size()
    defensive_stats.reset_index(inplace=True)

    offensive_stats.rename(columns={"shooting_poiu_id": "poiu_id"}, inplace=True)
    defensive_stats.rename(columns={"defending_poiu_id": "poiu_id"}, inplace=True)

    offensive_stats = offensive_stats.drop(columns=["shotDistance_sum"])
    defensive_stats = defensive_stats.drop(columns=["shotDistance_sum"])

    merged_df = pd.merge(
        offensive_stats, defensive_stats, 
        on = "poiu_id",
        how="outer", suffixes=('_offense', '_defense'))
    merged_df.fillna(0, inplace=True)

    merged_df["corsi"] = merged_df["num_shots_offense"] - merged_df["num_shots_defense"]

    cleaned_df = merged_df.copy()

    return cleaned_df

def calculate_neighbors(cleaned_df):
    """
    Create the dataframe for finding the 5 most similar POIUs for a given situation

    Args:
        cleaned_df (pd.DataFrame): dataframe prepared for clustering 
    Returns:
        neighbors_df (pd.DataFrame): dataframe where each row is a POIU and columns give the 5 most similar POIUs and similarity scores 
    """

    cols = list(cleaned_df.columns)
    feature_cols = [col for col in cols if col not in ["poiu_id"]]

    poiu_ids = cleaned_df['poiu_id']

    X = cleaned_df[feature_cols]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=.9) #Explains 90% of the variance
    X_reduced = pca.fit_transform(X_scaled)

    knn = NearestNeighbors(n_neighbors=6, metric='cosine') #Use 6 because this includes the unit being compared to itself
    knn.fit(X_reduced)
    distances, indices = knn.kneighbors(X_reduced)

    poiu_similarity_dict = {}

    for i in range(len(poiu_ids)):
        neighbors = []
        for j in range(1,6): 
            neighbor_index = indices[i][j]
            neighbor_id = poiu_ids.iloc[neighbor_index]
            similarity = 1 - distances[i][j]
            similarity_pct = round(similarity * 100, 2)
            neighbors.append({'poiu_id': neighbor_id, 'similarity_pct': similarity_pct})
        
        poiu_similarity_dict[poiu_ids.iloc[i]] = neighbors

    rows = []

    for main_id, neighbors in poiu_similarity_dict.items():
        row = {'poiu_id': main_id}
        for idx, neighbor in enumerate(neighbors, start=1):
            row[f'neighbor_{idx}'] = neighbor['poiu_id']
            row[f'similarity_{idx}'] = neighbor['similarity_pct']
        rows.append(row)

    neighbors_df = pd.DataFrame(rows)

    kmeans = KMeans(n_clusters=25, random_state=5)
    cluster_labels = kmeans.fit_predict(X_reduced)

    sil_score = silhouette_score(X_scaled, cluster_labels, metric="cosine")
    print(f"silhouette Score: {round(sil_score, 3)}")

    knn = NearestNeighbors(n_neighbors=6, metric="cosine")
    knn.fit(X_scaled)
    _, indices = knn.kneighbors(X_scaled)

    prec_k = precision_at_k(indices, cluster_labels, k=5)
    print(f"Precision@K Score: {round(prec_k, 3)}")

    return neighbors_df

def precision_at_k(knn_indices, cluster_labels, k=5):
    """
    Function to calculate the precision of knn label predictions for the k nearest neighbors

    Args:
        knn_indices (np.array, Integer): array of indices for the most similar POIUs
        cluster_labels (np.array, Integer): array of cluster labels determined by KMeans
        k (Integer): value of neighbors to test on
    """
    precision_scores = []
    for i, neighbors in enumerate(knn_indices):
        true_label = cluster_labels[i]
        retrieved_labels = [cluster_labels[j] for j in neighbors[1:k+1]]  
        relevant_count = sum(1 for label in retrieved_labels if label == true_label)
        precision_scores.append(relevant_count / k)
    return sum(precision_scores) / len(precision_scores)

def main():
    shot_data = pd.read_csv("shot_data_with_poiu.csv")

    print("Calculating Similarity for 5on5 situation POIUs")
    cleaned_data = clean_data(shot_data, "5on5")
    even_df = calculate_neighbors(cleaned_data)

    print("Calculating Similarity for Powerplay POIUs")
    cleaned_data = clean_data(shot_data, "5on4")
    pp_df = calculate_neighbors(cleaned_data)

    print("Calculating Similarity for Penalty Kill POIUs")
    cleaned_data = clean_data(shot_data, "4on5")
    pk_df = calculate_neighbors(cleaned_data)

    even_df.to_csv('similar_poius_5on5_2023.csv', index=False)
    pp_df.to_csv('similar_poius_powerplay_2023.csv', index=False)
    pk_df.to_csv('similar_poius_penalty_kill_2023.csv', index=False)

if __name__ ==  "__main__":
    main()


