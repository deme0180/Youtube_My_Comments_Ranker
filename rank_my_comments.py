import pandas as pd
from googleapiclient.discovery import build
import time

# 1. Paste your API Key from the previous project here
API_KEY = #"KeyGoesHere"

def get_comment_likes(comment_ids, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    all_stats = []
    
    # The API allows checking 50 IDs at a time (much faster than 1 by 1)
    for i in range(0, len(comment_ids), 50):
        batch = comment_ids[i:i+50]
        print(f"Fetching likes for batch {i//50 + 1}...")
        
        request = youtube.comments().list(
            part="snippet",
            id=",".join(batch)
        )
        response = request.execute()
        
        for item in response['items']:
            all_stats.append({
                'Comment ID': item['id'],
                'Likes': item['snippet']['likeCount'],
                'Text': item['snippet']['textDisplay']
            })
        
        # Small sleep to be nice to the API quota
        time.sleep(0.5)
        
    return pd.DataFrame(all_stats)

if __name__ == "__main__":
    # 2. Load your merged history
    df_history = pd.read_csv('my_full_history.csv')
    
    # 3. Clean up the IDs (remove any empty ones)
    ids_to_check = df_history['Comment ID'].dropna().tolist()
    
    print(f"Starting lookup for {len(ids_to_check)} comments...")
    
    # 4. Run the lookup
    df_ranked = get_comment_likes(ids_to_check, API_KEY)
    
    # 5. Sort by Likes (Highest first)
    df_ranked = df_ranked.sort_values(by='Likes', ascending=False)
    
    # 6. Save the final result
    df_ranked.to_csv('my_ranked_comments.csv', index=False)
    
    print("\n--- DONE! ---")
    print(f"Top Comment: {df_ranked.iloc[0]['Text']} with {df_ranked.iloc[0]['Likes']} likes!")
    print("Full results saved to 'my_ranked_comments.csv'.")
