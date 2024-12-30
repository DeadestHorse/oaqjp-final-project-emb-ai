import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, json=input_json, headers=header)
        status_code = response.status_code

        emotions = {}

        if status_code == 200:
            formatted_response = json.loads(response.text)
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            emotions['dominant_emotion'] = dominant_emotion[0]
        elif status_code == 400:
            emotions = {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        else:
            emotions['error'] = f"Unexpected status code: {status_code}"

        return emotions
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}