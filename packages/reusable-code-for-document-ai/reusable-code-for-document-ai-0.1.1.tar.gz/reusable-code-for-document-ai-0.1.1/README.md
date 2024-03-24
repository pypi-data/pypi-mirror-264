## Instructions
### Installing

5. Install using `pip` command

Use the pip command to install this package:

```shell
pip install reusable-code-for-document-ai
```


## Basic Usage

**NOTE:** Our system will support only image file and pdf file.

```
from reusable_code.process_document import CustomGoogleDocAIProcessor

processor = GoogleDocAIProcessor(
    location="your_location",
    processor_name="your_processor_name",
    processor_options=your_processor_options
)

document = processor.process_document("path_to_your_document", extract_page_number)

```

`path_to_your_document` = your pdf or image file path.

`extract_page_number` = Which page you want to extract, page number.

### processor options

**NOTE:** Additional configurations for Document OCR Processor (Optional).
```
# For more information: https://cloud.google.com/document-ai/docs/enterprise-document-ocr

process_options = documentai.ProcessOptions(
    ocr_config=documentai.OcrConfig(
        enable_native_pdf_parsing=True,
        enable_image_quality_scores=True,
        enable_symbol=True,
        # OCR Add Ons https://cloud.google.com/document-ai/docs/ocr-add-ons
        premium_features=documentai.OcrConfig.PremiumFeatures(
            compute_style_info=True,
            enable_math_ocr=False,  # Enable to use Math OCR Model
            enable_selection_mark_detection=True,
        ),
    )
)
```

#### Follow this pattern for set processor name

`
your_processor_name = projects/<PROJECT_ID>/locations/us/processors/<processor-id>/processorVersions/<version-id>
`

Make sure to replace `your_location`, `your_processor_name`, `your_processor_options`, and `path_to_your_document` with appropriate values.


