import pandas as pd
import os

# Function to combine CSV files, each representing a different genre, into a single DataFrame
def combine_csv_files_multiple_genres(directory):
    dataframes = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            new_genre = filename.replace('_songs.csv', '')  # Extract genre name from filename
            
            df = pd.read_csv(os.path.join(directory, filename))
            
            df['new_genre'] = new_genre  # Add a column for the new genre
            
            dataframes.append(df)
    
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    return combined_df

data = combine_csv_files_multiple_genres('scenarios_csv/')

# Function to count classifications per song based on high-probability predictions
def count_classifications_per_song(data):
    filtered_data = data[data['prob'] > 0.9]
    
    classification_counts = filtered_data.groupby('filename')['new_genre'].count().reset_index()
    classification_counts.columns = ['filename', 'num_classifications']
    
    return classification_counts

# Function to get the highest probability subgenre classification for each song
def highest_prob_per_song(data):
    max_prob = data.groupby('filename').apply(lambda df: df.loc[df['prob'].idxmax()])
    return max_prob[['filename', 'label', 'new_genre', 'prob']]

classification_counts = count_classifications_per_song(data)
max_prob_per_song = highest_prob_per_song(data)

print("Number of reclassifications for each song:")
print(classification_counts)

print("\nSubgenre with the highest probability for each song:")
print(max_prob_per_song)

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

# Plot the distribution of classifications per song
def plot_classifications_per_song(classification_counts):
    plt.figure(figsize=(10, 6))
    sns.histplot(classification_counts['num_classifications'], bins=range(1, classification_counts['num_classifications'].max() + 1), kde=False)
    plt.title('Number of Classifications per Song')
    plt.xlabel('Number of Classifications')
    plt.ylabel('Number of Songs')
    plt.show()

# Plot the probability distribution for the new genre classifications
def plot_probabilities_distribution(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['prob'], bins=10, kde=True)
    plt.title('Distribution of Probabilities for New Genres')
    plt.xlabel('Probability')
    plt.ylabel('Frequency')
    plt.show()

# Plot the number of reclassified songs per original genre
def plot_reclassified_per_original_genre(data):
    reclassified = data[data['prob'] > 0.9]
    plt.figure(figsize=(10, 6))
    sns.countplot(data=reclassified, x='label', palette='Set3')
    plt.title('Number of Reclassified Songs per Original Genre')
    plt.xlabel('Original Genre')
    plt.ylabel('Number of Reclassified Songs')
    plt.xticks(rotation=45)
    plt.show()

plot_classifications_per_song(classification_counts)
plot_probabilities_distribution(data)
plot_reclassified_per_original_genre(data)

# Count the number of unique reclassified songs per original genre
def count_reclassified_songs_per_genre(data):
    filtered_data = data[data['prob'] > 0.9]
    
    unique_reclassifications = filtered_data.drop_duplicates(subset=['filename'])
    
    reclassified_counts = unique_reclassifications.groupby('label')['filename'].count().reset_index()
    reclassified_counts.columns = ['original_genre', 'num_reclassified_songs']
    
    return reclassified_counts

# Plot the reclassified song count per original genre
def plot_reclassified_songs_per_genre(reclassified_counts):
    plt.figure(figsize=(10, 6))
    
    sns.barplot(data=reclassified_counts, x='original_genre', y='num_reclassified_songs', palette='Set3')
    
    plt.title('Number of Reclassified Songs per Original Genre')
    plt.xlabel('Original Genre')
    plt.ylabel('Number of Reclassified Songs')
    
    plt.xticks(rotation=45)
    
    plt.show()

reclassified_counts = count_reclassified_songs_per_genre(data)
plot_reclassified_songs_per_genre(reclassified_counts)

# Count the number of reclassified songs per new genre
def count_reclassified_songs_per_new_genre(data):
    filtered_data = data[data['prob'] > 0.9]
    
    new_genre_counts = filtered_data.groupby('new_genre')['filename'].nunique().reset_index()
    new_genre_counts.columns = ['new_genre', 'num_reclassified_songs']
    
    return new_genre_counts

# Plot the reclassified song count per new genre
def plot_reclassified_songs_per_new_genre(new_genre_counts):
    plt.figure(figsize=(10, 6))
    
    sns.barplot(data=new_genre_counts, x='new_genre', y='num_reclassified_songs', palette='Set2')
    
    plt.title('Number of Reclassified Songs per New Subgenre')
    plt.xlabel('New Subgenre')
    plt.ylabel('Number of Reclassified Songs')
    
    plt.xticks(rotation=90)
    
    plt.show()

new_genre_counts = count_reclassified_songs_per_new_genre(data)
plot_reclassified_songs_per_new_genre(new_genre_counts)

# Count songs in genres starting with a specific prefix
def count_songs_in_genres_starting_with(data, genre_prefix):
    filtered_data = data[data['prob'] > 0.9]
    
    genre_filtered = filtered_data[filtered_data['new_genre'].str.startswith(genre_prefix)]
    
    num_songs = genre_filtered['filename'].nunique()
    
    return num_songs

num_jazz_songs = count_songs_in_genres_starting_with(data, "jazz")
print(f'Number of songs in subgenres starting with "jazz": {num_jazz_songs}')

# Plot the number of songs in subgenres starting with a specified prefix
def plot_songs_in_genres_starting_with(data, genre_prefix):
    filtered_data = data[data['prob'] > 0.9]
    
    genre_filtered = filtered_data[filtered_data['new_genre'].str.startswith(genre_prefix)]
    
    genre_counts = genre_filtered.groupby('new_genre')['filename'].nunique().reset_index()
    genre_counts.columns = ['new_genre', 'num_songs']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=genre_counts, x='new_genre', y='num_songs', palette='Set1')
    
    plt.title(f'Number of Songs in Subgenres Starting with "{genre_prefix}"')
    plt.xlabel('New Subgenre')
    plt.ylabel('Number of Songs')
    
    plt.xticks(rotation=45)
    
    plt.show()

plot_songs_in_genres_starting_with(data, "jazz")

# Count songs for each genre prefix provided
def count_songs_by_genre_prefix(data, genres):
    filtered_data = data[data['prob'] > 0.9]
    
    genre_summary = []

    for genre in genres:
        genre_filtered = filtered_data[filtered_data['new_genre'].str.startswith(genre)]
        num_songs = genre_filtered['filename'].nunique()
        genre_summary.append({'genre': genre, 'num_songs': num_songs})

    genre_summary_df = pd.DataFrame(genre_summary)
    
    return genre_summary_df

# Plot songs by genre prefix
def plot_songs_by_genre_prefix(genre_summary_df):
    plt.figure(figsize=(10, 6))
    
    sns.barplot(data=genre_summary_df, x='genre', y='num_songs', palette='Set2')
    
    plt.title('Number of Songs Reclassified in Subgenres Starting with Original Genre Name')
    plt.xlabel('Original Genre')
    plt.ylabel('Number of Reclassified Songs')
    
    plt.show()

genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

genre_summary_df = count_songs_by_genre_prefix(data, genres)

plot_songs_by_genre_prefix(genre_summary_df)
