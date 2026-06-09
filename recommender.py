import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FragranceRecommender:
    def __init__(self, data_path="dataset/perfume_data.csv"):
        self.df = pd.read_csv(data_path)
        self.prepare_engine()
        
    def prepare_engine(self):
        # Create a rich metadata soup string
        self.df['metadata_soup'] = (
            self.df['Fragrance_Family'] + " " +
            self.df['Top_Notes'] + " " +
            self.df['Middle_Notes'] + " " +
            self.df['Base_Notes'] + " " +
            self.df['Occasion'] + " " +
            self.df['Gender']
        )
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['metadata_soup'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_recommendations(self, perfume_id, top_n=5):
        idx_list = self.df.index[self.df['Perfume_ID'] == int(perfume_id)].tolist()
        if not idx_list:
            return pd.DataFrame()
        idx = idx_list[0]
        
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        
        perfume_indices = [i[0] for i in sim_scores]
        return self.df.iloc[perfume_indices]

    def recommend_by_preferences(self, gender, occasion, favorite_note, top_n=5):
        # Dynamic filter or structural fallback matching
        mask = (self.df['Gender'] == gender) | (self.df['Gender'] == 'Unisex')
        filtered_df = self.df[mask]
        
        if filtered_df.empty:
            filtered_df = self.df
            
        note_mask = filtered_df['metadata_soup'].str.contains(favorite_note, case=False, na=False)
        matched = filtered_df[note_mask]
        
        if len(matched) >= top_n:
            return matched.head(top_n)
            
        return pd.concat([matched, filtered_df]).drop_duplicates().head(top_n)
