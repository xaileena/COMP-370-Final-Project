import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import glob

def calculate_tfidf_per_topic():
    data_dir = 'paul_data/tf-idf'
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    
    topic_documents = []
    topic_names = []
    
    print(f"Found {len(csv_files)} files in {data_dir}")
    
    for file_path in csv_files:
        # Get topic name from filename
        topic_name = os.path.splitext(os.path.basename(file_path))[0]
        topic_names.append(topic_name)
        
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Ensure columns exist
            if 'title' not in df.columns or 'description' not in df.columns:
                print(f"Warning: Missing 'title' or 'description' columns in {file_path}. Skipping.")
                topic_documents.append("")
                continue
                
            # Fill NaNs
            df['title'] = df['title'].fillna('')
            df['description'] = df['description'].fillna('')
            
            # Combine title and description for all articles in this topic
            # Adding a space between title and description
            full_text = " ".join(df['title'] + " " + df['description'])
            
            topic_documents.append(full_text)
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            topic_documents.append("")

    # Initialize TF-IDF Vectorizer
    # Using 'english' stop words to remove common words like 'the', 'and', etc.
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Fit and transform the documents (topics)
    tfidf_matrix = vectorizer.fit_transform(topic_documents)
    feature_names = vectorizer.get_feature_names_out()
    
    results = {}
    
    print("\nTop 10 TF-IDF words per topic:\n")
    
    for i, topic in enumerate(topic_names):
        # Get the row for the current topic
        row = tfidf_matrix[i]
        
        # Convert to dense array to iterate
        dense_row = row.todense().tolist()[0]
        
        # Pair scores with words
        word_scores = [(feature_names[j], dense_row[j]) for j in range(len(feature_names))]
        
        # Sort by score descending
        sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
        
        # Get top 10
        top_10 = sorted_words[:10]
        
        results[topic] = top_10
        
        print(f"Topic: {topic}")
        for word, score in top_10:
            print(f"  {word}: {score:.4f}")
        print("-" * 30)

if __name__ == "__main__":
    calculate_tfidf_per_topic()

