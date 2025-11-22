import pandas as pd
import numpy as np

# Load the CSV file, skipping problematic lines
df = pd.read_csv('articles.csv', on_bad_lines='skip')

# Get available indices (excluding 444-514, adjusting for 0-based indexing: 443-513)
available_indices = list(range(0, 443)) + list(range(514, len(df)))

# Calculate sampling interval
n_samples = 66
sampling_interval = len(available_indices) // n_samples

# Perform systematic sampling
start_index = np.random.randint(0, sampling_interval)
sampled_indices = available_indices[start_index::sampling_interval][:n_samples]

# Get the sampled articles
sampled_articles = df.iloc[sampled_indices]

# Save to a new CSV
sampled_articles.to_csv('sampled_articles_66.csv', index=False)

print(f"Selected {len(sampled_articles)} articles using systematic sampling")
print(f"Sample saved to 'sampled_articles_66.csv'")