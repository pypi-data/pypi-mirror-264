import os, joblib

def asivaRF_model():
    path = os.path.dirname(os.path.realpath(__file__))
    clf = joblib.load(f"{path}/asivaRF_model.joblib")
    return clf

def asivaRF_cm():
    path = os.path.dirname(os.path.realpath(__file__))
    return open(f"{path}/asivaRF_cm.png", "rb").read()

def logo():
    path = os.path.dirname(os.path.realpath(__file__))
    return open(f"{path}/logo.png", "rb").read()