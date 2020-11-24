from flask import Flask, request
from controller import corona_controller, news_controller
import requests

app = Flask(__name__)


@app.route('/corona-status')
def corona_status():
    args = request.args.get('region', None)
    data = corona_controller.get_corona_status(args)

    if data is None:
        return {'message': '검증 오류'}, 400

    return data

@app.route('/corona-info')
def corona_info():
    args = request.args.get('text', None)
    if args is None:
        return {'message': '음성 메세지를 입력해주세요'}, 400
    language_processing_server = "http://172.30.1.58:3000/analyze"
    parameter = {'text': args}
    r = requests.get(language_processing_server, parameter)
    date = r.json()['Date']
    region = r.json()['Location']
    data = corona_controller.get_corona_info(date, region)
    return {'data': data}, 200

@app.route('/news')
def corona_news():
    data = news_controller.get_news()
    return data


if __name__ == '__main__':
    app.run()
