from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras import layers
from PIL import Image
import numpy as np
import json
import os

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "https://detect-disease.vercel.app"}},
    supports_credentials=True
)

# paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
weights_path = os.path.join(BASE_DIR, "final_resnet_oversampled_weights.weights.h5")
label_encoder_path = os.path.join(BASE_DIR, "class_indices.json")

IMG_SIZE = (380, 380)
NUM_CLASSES = 7

# model
base_model = ResNet50V2(
    weights=None,
    include_top=False,
    input_shape=IMG_SIZE + (3,)
)
base_model.trainable = False

inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.4)(x)
x = layers.Dense(256, activation='relu')(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs, outputs)
model.load_weights(weights_path)
model.compile(optimizer='adam', loss='categorical_crossentropy')

# labels
with open(label_encoder_path, "r") as f:
    data = json.load(f)

label_encoder = [k for k, _ in sorted(data.items(), key=lambda x: x[1])]

# routes
@app.route("/", methods=["GET"])
def health():
    return {"status": "API running"}

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    file = request.files["image"]

    try:
        img = Image.open(file.stream).convert("RGB").resize(IMG_SIZE)
        arr = np.expand_dims(preprocess_input(np.array(img)), axis=0)

        preds = model.predict(arr)[0]
        idx = np.argmax(preds)

        confidence = float(preds[idx]) * 100
        label = label_encoder[idx]

        return jsonify({
            "final_prediction": label,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
