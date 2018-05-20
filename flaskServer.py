import numpy as np
import tensorflow as tf
from graphSetup import *
from flask import Flask, jsonify

app = Flask(__name__)

input_height = 331
input_width = 331
input_mean = 0
input_std = 331
input_layer = "Placeholder"
output_layer = "final_result"


graph = load_graph()
t = read_tensor_from_image_file(
    input_height=input_height,
    input_width=input_width,
    input_mean=input_mean,
    input_std=input_std)

input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation = graph.get_operation_by_name(input_name)
output_operation = graph.get_operation_by_name(output_name)

sess = tf.Session(graph=graph)


@app.route('/')
def classify():
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels()
    results_regular = results.tolist()
    answer_dic = {}
    for i in top_k:
        answer_dic[labels[i]] = results_regular[i]
    return jsonify(answer_dic)


if __name__ == '__main__':
    app.run()
