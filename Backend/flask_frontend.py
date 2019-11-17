

import flask
from flask import jsonify, request
import os
import sys
import OCR.text_from_im as OCR
import time

# function to join all the websites


def join(lst, sep):
    print("[LIST] ", str(lst))

    s = ''
    for i in range(len(lst) - 1):
        s += lst[i] + sep

    s += lst[-1]

    return s


app = flask.Flask("__main__")

# Frontend route
@app.route("/")
def my_index():
    # token can be sent, it can be anything usable by javascript
    return flask.render_template("index.html")

# Route where image is sent
@app.route("/OCR", methods=['POST', 'GET'])
def get_img():
    img = request.get_json()
    # print(img)

    question = OCR.text_from_image(img['img'])
    # question = "iitians man running"

    print(question)

    return jsonify({'question': question})

# Route where question is sent
@app.route("/scrapy", methods=['POST', 'GET'])
def get_question():

    websites = ["stackexchange.com", "doubtnut.com",
                "askiitians.com", "brainly.in"]

    current_dict = {}
    question = request.get_json()

    os.system('scrapy crawl spider -a question="{}"'.format(question["question"].replace(
        " ", "+").replace("\\n", "+").replace("\\t", "+")+"site%3A" + join(websites, "+OR+site%3A")))

    with open("ans.txt", "r") as file:
        ans = eval(file.read())

    print("ANSWER:", ans)

    current_dict["question"] = question["question"]
    current_dict["answers"] = ans["answer"]
    current_dict["websites"] = ans["domain"]

    print(type(current_dict["answers"]), type(current_dict["websites"]))

    print("CURRENT_DICT:", current_dict)

    return jsonify(current_dict)


@app.errorhandler(404)
def error404(error):
    return flask.render_template("404.html"), 404


app.run(host="0.0.0.0")
