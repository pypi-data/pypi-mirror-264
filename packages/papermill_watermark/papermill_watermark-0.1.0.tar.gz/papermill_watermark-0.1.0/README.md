# Watermark Engine for Papermill

Papermill Add-On which adds information for the system and all packages used in the notebook as an output in the end of the notebook.
The package currently works with R & Python only.

## Installation

```bash
pip install papermill_watermark
```

To display GPU information (Python only) install:
```bash
pip install papermill_watermark[gpu]
```

## Usage

```bash
papermill --engine papermill_watermark <INPUT_NOTEBOOK> <OUTPUT_NOTEBOOK>
```