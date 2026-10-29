# Tamil AD2: Tamil Brahmi Character Recognition

Tamil AD2 is a small desktop proof of concept for matching Early Tamil Brahmi characters in an image and exporting corresponding Tamil Unicode characters. It uses OpenCV template matching; it is not a general-purpose OCR system and does not perform word or line segmentation.

## Requirements

- Python 3
- OpenCV (`opencv-python`)
- Pillow
- NumPy
- Tkinter, including its operating-system Tcl/Tk support

## Installation

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install opencv-python Pillow numpy
```

On Windows PowerShell, create and activate the environment with:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install opencv-python Pillow numpy
```

Tkinter is included with many Python installations. On Ubuntu or Debian, if it is missing, install the system package with `sudo apt install python3-tk`. On Windows, use a Python installation that includes Tcl/Tk. A graphical desktop session is required to use the app.

## Run

Run the app from the project directory so it can find the templates in `test-data/`:

```bash
python main.py
```

1. Select **Import Image**.
2. Choose an image containing characters to recognize.
3. Read the detected characters in the terminal and in `output.txt` in the project directory. Each run overwrites the previous output. The app also attempts to show a preview with detected matches highlighted.

Select **Exit** to close the app.

## Project Files

- `main.py` starts the Tkinter interface and performs image matching.
- `test-data/` contains the 26 character templates used by the matcher.
- `test-images/` contains sample images that can be selected for recognition.
- `texts/` contains additional image files.
- `unicode.py` prints the character mapping; it is a standalone helper and is not required to run the app.
- `output.txt` is overwritten with the recognized Unicode text.

## Limitations

The matcher compares grayscale image regions with fixed templates using a similarity threshold of `0.90`. Characters that differ in size, orientation, or appearance from the templates may be missed or misidentified. The current implementation does not reliably remove repeated overlapping matches or arrange detections into normal reading order, so output may contain duplicates or be out of order. Use clear images with characters close in scale and orientation to the supplied templates; review the output rather than treating it as definitive transcription.

## Experimental ML Classifier

The repository also includes an experimental HOG+SVM classifier for **individual, already-cropped glyph images**. It is separate from the GUI, which continues to use template matching. Install the requirements above, then list class IDs and their Unicode labels:

```bash
python ml_classifier.py labels
```

Create a `training-data/` directory with numbered class folders. Each folder contains image crops of the character printed by the `labels` command for that ID. For example:

```text
training-data/
	00/
		glyph-a.png
		glyph-b.png
	01/
		glyph-a.png
		glyph-b.png
	...
	25/
		glyph-a.png
		glyph-b.png
```

Use PNG, JPEG, BMP, or TIFF crops. Every class folder you include needs at least two images, and the dataset must contain at least two different classes. For a useful 26-character classifier, collect examples for every class, including variation in handwriting, scale, and image quality. The 26 files in `test-data/` are templates, not a sufficient training set. Keep crops from the same source document or writer together when creating a final evaluation set to avoid overly optimistic results.

Train and evaluate with a held-out split:

```bash
python ml_classifier.py train --data-dir training-data
```

The command randomly holds out part of each class for validation, reports the resulting accuracy, and writes the model to `models/glyph-svm.yml`. This random split is useful as a quick check, but can overestimate performance when related crops appear in both splits. Classify an individual cropped glyph with:

```bash
python ml_classifier.py predict path/to/glyph.png
```

Prediction prints the class ID and mapped Unicode character; it does not currently report a calibrated confidence score. This model does not detect or crop glyphs from full pages, and its predictions are not yet integrated into the GUI. No LLM features are implemented.

Run the class-mapping tests from the project directory with:

```bash
python -m unittest discover -s tests
```
