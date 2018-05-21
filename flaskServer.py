import numpy as np
from flask import Flask, jsonify

import firebaseInterface as fbi
from config import THRESHOLD
from graphSetup import *

app = Flask(__name__)

input_height = 331
input_width = 331
input_mean = 0
input_std = 331
input_layer = "Placeholder"
output_layer = "final_result"

graph1 = load_graph()
t1 = read_tensor_from_image_file(
    input_height=331,
    input_width=331,
    input_mean=input_mean,
    input_std=331)

input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation1 = graph1.get_operation_by_name(input_name)
output_operation1 = graph1.get_operation_by_name(output_name)

banana_session = tf.Session(graph=graph1)

graph2 = load_graph(model_path=MODEL_PATH2)
t2 = read_tensor_from_image_file(
    input_height=224,
    input_width=224,
    input_mean=224,
    input_std=input_std)

input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation2 = graph2.get_operation_by_name(input_name)
output_operation2 = graph2.get_operation_by_name(output_name)

apple_session = tf.Session(graph=graph2)


def parse_results(labels, results, top_k,session):
    results_regular = results.tolist()
    answer_dic = {}
    for i in top_k:
        answer_dic[session+labels[i]] = results_regular[i]
    # for product, product_confidence in answer_dic.items():
    #     if product_confidence > THRESHOLD:
    #         fbi.addProductForUser(product.title())
    return answer_dic

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

@app.route('/')
def classify():
    results = banana_session.run(output_operation1.outputs[0], {
        input_operation1.outputs[0]: t1
    })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file=LABEL_FILE)
    dic1 = parse_results(labels, results, top_k,"banana_model ")

    print(dic1)

    results = apple_session.run(output_operation2.outputs[0], {
        input_operation2.outputs[0]: t2
    })
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]

    dic2 = parse_results(labels, results, top_k,"apple_model ")

    total = merge_two_dicts(dic1,dic2)
    print(total)

    return jsonify(total)


if __name__ == '__main__':
    app.run()
