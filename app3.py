from flask import Flask, request, jsonify
import pickle
# from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
print('xgboost version ',xgb.__version__)

from process_data2 import process_input

# For logging
import logging
import traceback
from logging.handlers import RotatingFileHandler
from time import strftime, time

file_name = "model_.pkl"

xgb_model_loaded = pickle.load(open(file_name, "rb"))
print(xgb_model_loaded)

app = Flask(__name__)


# Logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=5)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route("/")
def index():
    return "Prediction API on xgboost model"


@app.route("/predict", methods=['GET','POST'])
def predict():
    json_input = request.get_json(force=True)
    print('json_input:  ',json_input)

    # Request logging
    current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    logger.info(f'{current_datatime} request from {ip_address}: {request.json}')
    start_prediction = time()

    # id = json_input['ID']
    user_data = process_input(json_input)

    print('user_data:', user_data)

    # prediction_Claims = xgb_model_loaded.predict(user_data)

    user_data_matrix = xgb.DMatrix(user_data)
    prediction_Claims = xgb_model_loaded.predict(user_data_matrix)  # Посчитаем предсказанное значения

    ClaimInd = int(prediction_Claims[0])
    print('prediction:', ClaimInd)

    #
    # id = json_input['id']
    #
    # result = {
    #     'ID': id,
    #     'ClaimInd': 'ClaimInd'
    # }


    # Response logging
    end_prediction = time()
    duration = round(end_prediction - start_prediction, 6)
    current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
    logger.info(f'{current_datatime} predicted for {duration} msec: {ClaimInd}\n')

    return jsonify(ClaimInd)

# @app.errorhandler(Exception)
# def exceptions(e):
#     current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
#     error_message = traceback.format_exc()
#     logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
#                  current_datatime,
#                  request.remote_addr,
#                  request.method,
#                  request.scheme,
#                  request.full_path,
#                  error_message)
#     return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)