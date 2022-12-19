from flask import Flask, request, jsonify 
from flasgger import Swagger, LazyString, LazyJSONEncoder,swag_from
import time
import pandas as pd
from text_cleansing import lower_case, remove_newline, remove_hashtag, remove_link, remove_punctuation, remove_spaces, indo_stemming, stopwords_remove, _normalization
from db_lstm import checkTableText, checkTableFile, input_text, input_file

app = Flask(__name__)
app.json_encoder =LazyJSONEncoder

swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API for LSTM'),
        'version': LazyString(lambda: '1'),
        'description': LazyString(lambda: 'API Tester for Sentiment Analysis using LSTM algorithm')
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers":[],
    "specs": [
        {
            "endpoint":"docs",
            "route":"/docs.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template,config=swagger_config)

def text_cleaning():
    text = s
    s = lower_case(s)
    s = stopwords_remove(s)
    s = remove_hashtag(s)
    s = remove_link(s)
    s = remove_punctuation(s)
    s = remove_spaces(s)
    s = remove_newline(s)
    s = indo_stemming(s)
    s = _normalization(s)
    input_text(s)
    return jsonify({"Result" : s})

def file_processing(df):
    df['lower_case'] = df['sentence'].apply(lower_case)
    df['sw'] = df['lower_case'].apply(stopwords_remove)
    df['hashtag'] = df['sw'].apply(remove_hashtag)
    df['link'] = df['hashtag'].apply(remove_link)
    df['punct'] = df['link'].apply(remove_punctuation)
    df['multi_space'] = df['punct'].apply(remove_spaces)
    df['newline'] = df['multi_space'].apply(remove_newline)
    df['stemming'] = df['newline'].apply(indo_stemming)
    df['normal'] = df['stemming'].apply(_normalization)
    df['normal'].to_csv('output.csv', index=False, header=False)
    a = pd.DataFrame(df[['sentence','label']])
    input_file(a)

@swag_from("swagger_config_text.yml", methods=['POST']) #endpoint 1
@app.route('/api_lstm/text/v1', methods=['POST'])
def text_cleaning():
    checkTableText()
    s = request.get_json()
    text_clean = text_cleaning(s['text'])
    return jsonify({"result":text_clean})

@swag_from("swagger_config_file.yml", methods=['POST']) #endpoint 2
@app.route('/api_lstm/file/v1', methods=['POST'])
def file_cleaning():
    checkTableFile()
    start_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, encoding=('ISO-8859-1'))
    file_processing(df)
    return jsonify({"result":"file berhasil diupload ke database","time_exc":"--- %s seconds ---" % (time.time() - start_time)})


if __name__=="__main__":
    app.run(port=1234, debug=True)