# AI/ML Python Package: `ml_dronebase_data_utils`

This package contains commonly used data functions for the AI/ML Team at Zeitview (formerly: DroneBase).

This repo provides:

- Custom Python Package: `ml_dronebase_data_utils`

<!-- MarkdownTOC -->

- [Contributing Guidelines](#contributing-guidelines)
- [Usage](#usage)
- [Object Detection Annotation Formatting](#object-detection-annotation-formatting)
- [S3 Data Utils](#s3-data-utils)
  - [Installation from source](#installation-from-source)
  - [Installation using pip](#installation-using-pip)
- [References](#references)

<!-- /MarkdownTOC -->

<a id="contributing-guidelines"></a>
## Contributing Guidelines

Please see the [CONTRIBUTING.md](./.github/CONTRIBUTING.md) document for details on how to contribute to this repository through Pull-Requests.

<a id="usage"></a>
## Usage

```python
import ml_dronebase_data_utils as data_utils
...
```

<a id="object-detection-annotation-formatting"></a>
## Object Detection Annotation Formatting

This package provides a Pascal VOC writer that renders ```*.xml``` annotation files for object detection tasks.
It supports regular object detection and oriented object detection annotations with an additional ```<angle>```_some angle_```</angle>``` parameter.

```python
from ml_dronebase_data_utils import PascalVOCWriter
writer = PascalVOCWriter()

for box in boxes:
    xmin, ymin, xmax, ymax, angle = box
    writer.addObject(
        name="some class name",
        xmin=xmin,
        ymin=ymin,
        xmax=xmax,
        ymax=ymax,
        angle=angle # Optional parameter
    )
writer.save(annotation_path)
```

This package also provide CLI interfaces for the same,

`convert_geojson` can be used to convert geojson to voc format. This also has the ability to process in batch.

```txt
usage: convert_geojson [-h] --ortho-path ORTHO_PATH --geojson GEOJSON 
                       --save-path SAVE_PATH 
                      [--class-attribute CLASS_ATTRIBUTE[CLASS_ATTRIBUTE ...]]
                      [--class-mapping CLASS_MAPPING]
                      [--skip-classes SKIP_CLASSES [SKIP_CLASSES ...]] 
                      [--rotated] [--batch] [--prefix PREFIX]

Convert geojson to voc format data

optional arguments:
  -h, --help            show this help message and exit
  --ortho-path ORTHO_PATH
                        The ortho path, can be local/s3
  --geojson GEOJSON     The geojson path
  --save-path SAVE_PATH
                        The save path
  --class-attribute CLASS_ATTRIBUTE [CLASS_ATTRIBUTE ...]
                        The class attribute to use from the geojson for class labels
  --class-mapping CLASS_MAPPING
                        A plain txt file containing class mappings
  --skip-classes SKIP_CLASSES [SKIP_CLASSES ...]
                        Classes to skip, specify multiple
  --rotated             Use rotated bounding box, defaults to false
  --batch               Process a batch of orthos
  --prefix PREFIX       The prefix to use when saving the annotation
```

Example,

```bash
convert_geojson --ortho-path s3://ml-solar-ortho-fault-detection/orthos/tiff/PA140004_Thermal.tif --geojson s3://ml-solar-ortho-fault-detection/orthos/geojson/PA140004_Thermal.geojson --save-path s3://ml-solar-ortho-fault-detection/orthos/annotations/PA140004_Thermal.xml --class-attribute id --skip-classes 0 4 5 6 7 8 9 10 --class-mapping mapping.txt
```

mapping.txt must contain mappings in the format `0 = Normal`

`visualize_converted_geojson` can be used to visualize the generated annotations. This also has the ability to process in batch.

```txt
usage: visualize_converted_geojson [-h] --ortho-path ORTHO_PATH --anno-path
                                   ANNO_PATH --save-path SAVE_PATH
                                   [--draw-labels] [--batch]

Visualize converted geojson for quick visual inspection

optional arguments:
  -h, --help            show this help message and exit
  --ortho-path ORTHO_PATH, -o ORTHO_PATH
                        The ortho path, can be local/s3
  --anno-path ANNO_PATH, -a ANNO_PATH
                        The ortho path, can be local/s3
  --save-path SAVE_PATH, -s SAVE_PATH
                        The ortho path, can be local/s3
  --draw-labels, -d     Draw the class labels
  --batch, -b           Run in batched mode
```

Example,

```bash
visualize_converted_geojson -o s3://ml-solar-ortho-fault-detection/orthos/tiff/PA140004_Thermal.tif -a s3://ml-solar-ortho-fault-detection/orthos/annotations/PA140004_Thermal.xml -s s3://ml-solar-ortho-fault-detection/orthos/visual_validation/PA140004_Thermal_drawn.png -d
```

<a id="s3-data-utils"></a>
## S3 Data Utils

This package also provides common AWS S3 data functions like downloading data, uploading data (data or trained models), train/test split, etc.

<a id="installation-from-source"></a>
### Installation from source

Clone and ```cd``` into the root directory of this repo, then run the following:

```bash
pip install -e .
```

<a id="installation-using-pip"></a>
### Installation using pip

```bash
pip install ml-dronebase-data-utils
```

<a id="references"></a>
## References

- [AI/ML Confluence Wiki](https://dronebase.atlassian.net/l/cp/1bcAYU82)
- [AI/ML DevOps Confluence Wiki](https://dronebase.atlassian.net/l/cp/Am4YKXPF)
- [AI/ML MLOps Confluence Wiki](https://dronebase.atlassian.net/l/cp/FER9Q0JV)
