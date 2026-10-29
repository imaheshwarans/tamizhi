import argparse
from pathlib import Path

import cv2
import numpy as np

from labels import CHARACTERS


IMAGE_SIZE = (64, 64)
IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff"}
HOG = cv2.HOGDescriptor(
    IMAGE_SIZE,
    (16, 16),
    (8, 8),
    (8, 8),
    9,
)


def extract_features(image_path):
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    image = cv2.resize(image, IMAGE_SIZE, interpolation=cv2.INTER_AREA)
    return HOG.compute(image).reshape(-1)


def load_dataset(data_dir):
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise ValueError(f"Dataset directory does not exist: {data_dir}")

    class_samples = {}
    for class_id in range(len(CHARACTERS)):
        class_dir = data_dir / f"{class_id:02d}"
        samples = sorted(
            path for path in class_dir.iterdir()
            if class_dir.is_dir() and path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        ) if class_dir.is_dir() else []
        if samples:
            if len(samples) < 2:
                raise ValueError(
                    f"Class {class_id:02d} needs at least 2 images for training and validation"
                )
            class_samples[class_id] = samples

    if len(class_samples) < 2:
        raise ValueError("Add images for at least 2 different class folders (00-25)")

    return class_samples


def split_dataset(class_samples, validation_fraction, seed):
    rng = np.random.default_rng(seed)
    training_paths = []
    validation_paths = []

    for class_id, paths in class_samples.items():
        shuffled = list(paths)
        rng.shuffle(shuffled)
        validation_count = min(
            max(1, round(len(shuffled) * validation_fraction)),
            len(shuffled) - 1,
        )
        validation_paths.extend((path, class_id) for path in shuffled[:validation_count])
        training_paths.extend((path, class_id) for path in shuffled[validation_count:])

    return training_paths, validation_paths


def features_and_labels(samples):
    features = np.asarray([extract_features(path) for path, _ in samples], dtype=np.float32)
    labels = np.asarray([class_id for _, class_id in samples], dtype=np.int32)
    return features, labels


def train(args):
    class_samples = load_dataset(args.data_dir)
    training_samples, validation_samples = split_dataset(
        class_samples, args.validation_fraction, args.seed
    )
    training_features, training_labels = features_and_labels(training_samples)
    validation_features, validation_labels = features_and_labels(validation_samples)

    model = cv2.ml.SVM_create()
    model.setType(cv2.ml.SVM_C_SVC)
    model.setKernel(cv2.ml.SVM_LINEAR)
    model.setC(1.0)
    model.train(
        training_features,
        cv2.ml.ROW_SAMPLE,
        training_labels.reshape(-1, 1),
    )

    _, predicted = model.predict(validation_features)
    accuracy = np.mean(predicted.reshape(-1).astype(np.int32) == validation_labels)

    model_path = Path(args.model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path))

    print(f"Training images: {len(training_samples)}")
    print(f"Validation images: {len(validation_samples)}")
    print(f"Validation accuracy: {accuracy:.1%}")
    print(f"Model saved to: {model_path}")


def predict(args):
    model_path = Path(args.model_path)
    if not model_path.is_file():
        raise ValueError(f"Model file does not exist: {model_path}")

    model = cv2.ml.SVM_load(str(model_path))
    _, result = model.predict(extract_features(args.image))
    class_id = int(result[0, 0])
    print(f"Class {class_id:02d}: {CHARACTERS[class_id]}")


def list_labels(_args):
    for class_id, character in enumerate(CHARACTERS):
        print(f"{class_id:02d}\t{character}")


def build_parser():
    parser = argparse.ArgumentParser(description="Train and run a glyph HOG+SVM classifier")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("labels", help="list class IDs and their Unicode labels")
    commands.choices["labels"].set_defaults(handler=list_labels)

    train_parser = commands.add_parser("train", help="train and evaluate from labeled glyph crops")
    train_parser.add_argument("--data-dir", default="training-data")
    train_parser.add_argument("--model-path", default="models/glyph-svm.yml")
    train_parser.add_argument("--validation-fraction", type=float, default=0.2)
    train_parser.add_argument("--seed", type=int, default=42)
    train_parser.set_defaults(handler=train)

    predict_parser = commands.add_parser("predict", help="classify one cropped glyph image")
    predict_parser.add_argument("image")
    predict_parser.add_argument("--model-path", default="models/glyph-svm.yml")
    predict_parser.set_defaults(handler=predict)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not 0 < getattr(args, "validation_fraction", 0.2) < 1:
        parser.error("--validation-fraction must be between 0 and 1")
    try:
        args.handler(args)
    except (OSError, ValueError, cv2.error) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()