from deepface.basemodels import SFace
import tensorflow as tf
import tf2onnx
import sys

model = SFace.loadModel()

onnx_model_path = sys.argv[1]

spec = (tf.TensorSpec((None, 160, 160, 3), tf.float32, name="input"),)
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=onnx_model_path)

print("Model converted to ONNX:", onnx_model_path)


