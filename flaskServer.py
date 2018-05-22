import base64
import sys
import os

from flask import Flask, jsonify, request
import firebaseInterface as fbi
from object_detection_tutorial import get_image_objects

sys.path.append('..')
app = Flask(__name__)
path_to_script = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(path_to_script,"downloaded_images", "image1.jpg")
print(file_name)

@app.route('/getPic', methods=['POST'])
def get_content():
    image_64_coded = request.data
    image_64_decoded = base64.b64decode(image_64_coded)
    image_result = open(file_name, 'wb')
    image_result.write(image_64_decoded)
    image_result.close()
    detected_classes = get_image_objects()
    print(detected_classes)
    if detected_classes:
        fbi.addProductForUser(detected_classes[0].title())
    return jsonify(detected_classes)


@app.route('/')
def classify():
    detected_classes = get_image_objects()
    print(detected_classes)
    return jsonify(detected_classes)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# input_height = 331
# input_width = 331
# input_mean = 0
# input_std = 331
# input_layer = "Placeholder"
# output_layer = "final_result"
#
# graph1 = load_graph()
# t1 = read_tensor_from_image_file(
#     input_height=331,
#     input_width=331,
#     input_mean=input_mean,
#     input_std=331)
#
# input_name = "import/" + input_layer
# output_name = "import/" + output_layer
# input_operation1 = graph1.get_operation_by_name(input_name)
# output_operation1 = graph1.get_operation_by_name(output_name)
#
# banana_session = tf.Session(graph=graph1)
#
# graph2 = load_graph(model_path=MODEL_PATH2)
# t2 = read_tensor_from_image_file(
#     input_height=224,
#     input_width=224,
#     input_mean=224,
#     input_std=input_std)
#
# input_name = "import/" + input_layer
# output_name = "import/" + output_layer
# input_operation2 = graph2.get_operation_by_name(input_name)
# output_operation2 = graph2.get_operation_by_name(output_name)
#
# apple_session = tf.Session(graph=graph2)


# results = banana_session.run(output_operation1.outputs[0], {
#     input_operation1.outputs[0]: t1
# })
# results = np.squeeze(results)
#
# top_k = results.argsort()[-5:][::-1]
# labels = load_labels(label_file=LABEL_FILE)
# dic1 = parse_results(labels, results, top_k,"banana_model ")
#
# print(dic1)
#
# results = apple_session.run(output_operation2.outputs[0], {
#     input_operation2.outputs[0]: t2
# })
# results = np.squeeze(results)
# top_k = results.argsort()[-5:][::-1]
#
# dic2 = parse_results(labels, results, top_k,"apple_model ")
#
# total = merge_two_dicts(dic1,dic2)
# print(total)
#
# return jsonify(total)
