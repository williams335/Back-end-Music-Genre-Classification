
import librosa
import numpy as np
import os
import urllib.request
import json
from pathlib import Path
def getmetadata(filename):
    
    y, sr = librosa.load(filename)
    #fetching tempo

    onset_env = librosa.onset.onset_strength(y, sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    #fetching beats

    y_harmonic, y_percussive = librosa.effects.hpss(y)
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)

    #chroma_stft

    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

    #rmse

    rmse = librosa.feature.rms(y=y)

    #fetching spectral centroid

    spec_centroid = librosa.feature.spectral_centroid(y, sr=sr)[0]

    #spectral bandwidth

    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)

    #fetching spectral rolloff

    spec_rolloff = librosa.feature.spectral_rolloff(y+0.01, sr=sr)[0]

    #zero crossing rate

    zero_crossing = librosa.feature.zero_crossing_rate(y)

    #mfcc

    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    #metadata dictionary

    metadata_dict = {'tempo':tempo,'chroma_stft':np.mean(chroma_stft),'rmse':np.mean(rmse),
                     'spectral_centroid':np.mean(spec_centroid),'spectral_bandwidth':np.mean(spec_bw), 
                     'rolloff':np.mean(spec_rolloff), 'zero_crossing_rates':np.mean(zero_crossing)}

    for i in range(1,21):
        metadata_dict.update({'mfcc'+str(i):np.mean(mfcc[i-1])})


    data = {
            "Inputs": {
                    "input1":
                    [
                        {
                                'chroma_stft': str(metadata_dict["chroma_stft"]),   
                                'rmse': str(metadata_dict["rmse"]),   
                                'spectral_centroid': str(metadata_dict["spectral_centroid"]),   
                                'spectral_bandwidth': str(metadata_dict["spectral_bandwidth"]),   
                                'rolloff': str(metadata_dict["rolloff"]),   
                                'zero_crossing_rate': str(metadata_dict["zero_crossing_rates"]),   
                                'mfcc1': str(metadata_dict["mfcc1"]),   
                                'mfcc2': str(metadata_dict["mfcc2"]),   
                                'mfcc3': str(metadata_dict["mfcc3"]),   
                                'mfcc4': str(metadata_dict["mfcc4"]),   
                                'mfcc5': str(metadata_dict["mfcc5"]),   
                                'mfcc6': str(metadata_dict["mfcc6"]),   
                                'mfcc7': str(metadata_dict["mfcc7"]),   
                                'mfcc8': str(metadata_dict["mfcc8"]),   
                                'mfcc9': str(metadata_dict["mfcc9"]),   
                                'mfcc10': str(metadata_dict["mfcc10"]),   
                                'mfcc11': str(metadata_dict["mfcc11"]),   
                                'mfcc12': str(metadata_dict["mfcc12"]),   
                                'mfcc13': str(metadata_dict["mfcc13"]),   
                                'mfcc14': str(metadata_dict["mfcc14"]),   
                                'mfcc15': str(metadata_dict["mfcc15"]),   
                                'mfcc16': str(metadata_dict["mfcc16"]),   
                                'mfcc17': str(metadata_dict["mfcc17"]),   
                                'mfcc18': str(metadata_dict["mfcc18"]),   
                                'mfcc19': str(metadata_dict["mfcc19"]),   
                                'mfcc20': str(metadata_dict["mfcc20"]),   
                        }
                    ],
            },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/259f8cd91f254ccfb40dad88fffd9116/services/f2f07fe950cc4427a971f87e18700a93/execute?api-version=2.0&format=swagger'
    api_key = 'Y2PFaXa7TBnO3knI27UmiLWdW96dl22P/YYj9TAQLC+fPhHGFQRFXzaHn9ItYp25pnXxTKeQDnpHLYaLo332yg==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        #print(result)

        return str(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))
        
        return json.loads(error.read().decode("utf8", 'ignore'))
        
        
    
    #return list(metadata_dict.values())



