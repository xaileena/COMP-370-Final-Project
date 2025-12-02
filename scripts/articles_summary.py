import pandas as pd

# Use on_bad_lines='skip' to ignore malformed rows
df = pd.read_csv('articles.csv', on_bad_lines='skip')

source_stats = df['source_name'].value_counts().reset_index()
source_stats.columns = ['source_name', 'article_count']

print(source_stats)
source_stats.to_csv('source_article_counts.csv', index=False)