from django.shortcuts import render
from .scrap_comments import scrap_comments
from .clean_text import clean_text

import pandas as pd

import pickle

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import UserActivity

from django.contrib.auth.models import User

# @login_required
@csrf_exempt
def predict_sentiment(request):
    if request.method == 'POST':
        try:
            
            # Get the JSON data from the request body
            data = json.loads(request.body)
            videoID = data.get('videoID', '')
            apiKey = data.get('apiKey', '')
            numberofcomments = data.get('numberofcomments', '')
            username = data.get('username', '')
            model_choice = data.get('model', '') 

            user= User.objects.get(username=username)

            comments= scrap_comments(videoID,apiKey,numberofcomments)

            single_array = []
            for inner_list in comments:
                for comment in inner_list:
                    single_array.append(comment)
            comment_df = pd.DataFrame(comments, columns=['text'])

            # comment_df.info()
            

            # Preprocess the input sentence
            comment_df['processed_text'] = comment_df['text'].apply(clean_text)  # Preprocess the text column

            if model_choice == 'model1':
                with open('svm_classifier.pkl', 'rb') as f:
                    tf_idf_vect, model = pickle.load(f)
                X_df = tf_idf_vect.transform(comment_df['processed_text'])
                predicted_labels_df = model.predict(X_df)
                predicted_labels_df = predicted_labels_df.tolist()
            elif model_choice == 'model2':
                with open('naive_bayes_classifier.pkl', 'rb') as f:
                    model = pickle.load(f)
                predicted_labels_df = model.predict(comment_df['processed_text'])

            # Load tfidf vectorizer and model from the pickle file
            # with open('svm_classifier.pkl', 'rb') as f:
                # tf_idf_vect, model1 = pickle.load(f)
            # If you have a DataFrame df with comments in a 'text' column
            # X_df = tf_idf_vect.transform(comment_df['processed_text'])

            # Predict on the DataFrame
            # predicted_labels_df = model1.predict(X_df)  


            # Load nb_classifier model from the pickle file 
            # with open('naive_bayes_classifier.pkl', 'rb') as f:
            #     model2 = pickle.load(f)
            # predicted_labels_df = model2.predict(comment_df['processed_text'])  
            


            # Create a DataFrame with labels
            predicted_df = pd.DataFrame({
                'text': comment_df['text'], 
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
            print("Neutral count:", neutral_count)
            print("Negative count:", negative_count)
            # user=User()
            # print(user.username)
            userActivity =UserActivity(user=user, videoid= videoID,positive_count=positive_count,negative_count=negative_count,neutral_count=neutral_count,model_choice=model_choice)

            userActivity.save()
            
            return JsonResponse({
                'status':True,
                'message': "Predicted successfully!",       
                'Positive':str(positive_count),
                'Negative':str(negative_count),
                'Neutral':str(neutral_count),
                'model_used':model_choice,
                'comments': single_array,
                'predicted_labels': predicted_labels_df
            })          
        except json.JSONDecodeError:           
            return JsonResponse({
                    'status':False,
                    'message': 'Invalid JSON data',                        
                },status=400)
    else:
        return JsonResponse({
                        'status':False,
                        'message': 'Only POST requests are allowed',                        
                    },status=400)


@csrf_exempt

def get_history(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')

        user = User.objects.get(username=username)
        response = []

        userActivity = UserActivity.objects.filter(user=user)
        if len(userActivity) < 1:
            return JsonResponse({'response': response}, status=200)

        for userAct in userActivity:
            response.append({
                "videoid": userAct.videoid,
                "positive": userAct.positive_count,
                "negative": userAct.negative_count,
                "neutral": userAct.neutral_count,
                "model_choice": userAct.model_choice
            })

        return JsonResponse({'response': response})
    from django.shortcuts import render


from django.http import HttpResponse
from django.conf import settings
import os


@csrf_exempt

def get_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_name = data.get('image_name', '')
        # Construct the path to the image
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        try:
            # Open the image file
            with open(image_path, 'rb') as f:
                # Return the image as a response
                return HttpResponse(f.read(), content_type='image/jpeg')  # Adjust content_type as per your image type
        except IOError:
            # Handle file not found error
            return HttpResponse(status=404)

