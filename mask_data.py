import pandas as pd
import re

def mask_pii(text):
    if not isinstance(text, str):
        return text
    
    # 1. Mask Emails
    text = re.sub(r'\S+@\S+\.\S+', '[EMAIL_MASKED]', text)
    
    # 2. Mask Phone Numbers (Common formats)
    text = re.sub(r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', '[PHONE_MASKED]', text)
    
    return text

# 3. Load your ranked comments
df = pd.read_csv('my_ranked_comments.csv')

print("Masking PII and IDs...")

# 4. Mask the text content
df['Text'] = df['Text'].apply(mask_pii)

# 5. Anonymize the Comment ID (Replace IDs with 1, 2, 3...)
df['Comment ID'] = range(1, len(df) + 1)

# 6. Save the "Safe" version for GitHub
df.to_csv('my_ranked_comments_PUBLIC.csv', index=False)

print("Success! Created 'my_ranked_comments_PUBLIC.csv'.")
print("You can now safely share this file.")
