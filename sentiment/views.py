from django.shortcuts import render,HttpResponse
from .scrap_comments import scrap_comments
from .clean_text import clean_text

import pandas as pd

import pickle

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


@csrf_exempt
def predict_sentiment(request):
    if request.method == 'POST':
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)
            videoID = data.get('videoID', '')
            comments= scrap_comments(videoID)
            comment_df = pd.DataFrame(comments, columns=['text'])

            # comment_df.info()
            

        # Load CountVectorizer and model from the pickle file
            with open('text_classifier.pkl', 'rb') as f:
                bow_counts, model1 = pickle.load(f)
            # Preprocess the input sentence
            # If you have a DataFrame df with comments in a 'text' column
            comment_df['processed_text'] = comment_df['text'].apply(clean_text)  # Preprocess the text column
            X_df = bow_counts.transform(comment_df['processed_text'])

            # Predict on the DataFrame
            predicted_labels_df = model1.predict(X_df)


            # Create a DataFrame with labels
            predicted_df = pd.DataFrame({
                'text': comment_df['text'],  # Assuming you want to include the original text
                'predicted_label': predicted_labels_df
            })

            # print("\nPredicted DataFrame:")
            # print(predicted_df)

            # Count occurrences of each class label
            label_counts = predicted_df['predicted_label'].value_counts()

            # Print the counts
            print("\nCount of each class label:")
            print(label_counts)
            # Store counts in variables
            positive_count = label_counts.get('positive', 0)
            negative_count = label_counts.get('negative', 0)
            neutral_count = label_counts.get('neutral', 0)


            # Print the counts
            print("\nCount of each class label:")
            print("Positive count:", positive_count)
            print("Negative count:", negative_count)
            print("Neutral count:", neutral_count)
            
            return JsonResponse({
                'status':True,
                'message': "Predicted successfully!",       
                'Positive':str(positive_count),
                'Negative':str(negative_count),
                'Neutral':str(neutral_count),
            })          
        except json.JSONDecodeError:           
            return JsonResponse({
                    'status':False,
                    'message': 'Invalid JSON data',                        
                })
    else:
        return JsonResponse({
                        'status':False,
                        'message': 'Only POST requests are allowed',                        
                    })
