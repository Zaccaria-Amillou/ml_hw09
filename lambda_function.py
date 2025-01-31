import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor

preprocessor = create_preprocessor('xception', target_size=(200, 200))

interpreter = tflite.Interpreter(model_path="model_2024_hairstyle.tflite")
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

def predict(url):
    X = preprocessor.from_url(url)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    float_predictions = preds[0].tolist()


    return {'prediction': float_predictions[0]}

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result
