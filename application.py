from flask import Flask, jsonify, send_file
from fpdf import FPDF
import datetime
import os

application = Flask(__name__)


data = [
    {
        'coupon': "AnyCoupon",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    },
    {
        'coupon': "ABCD",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    },
    {
        'coupon': "2021Launch",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    },
    {
        'coupon': "MyCoupon",
        'dic': 20,
        'avbl': 10,
        'for': 'all'
    }
]


@application.route('/')
def index():
    return "hello"



@application.route("/fetch", methods=['get'])
def get():
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
