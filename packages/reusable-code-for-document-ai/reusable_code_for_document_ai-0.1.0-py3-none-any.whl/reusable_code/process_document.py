import logging
import mimetypes

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError
from google.cloud import documentai
from google.cloud.documentai_v1 import Document

from exceptions import DocAIException  # Importing custom exception
from read_pdf_or_image_files import read_files_content  # Importing file reading function

# Set up logging
logging.basicConfig(level=logging.INFO)


class CustomGoogleDocAIProcessor:
    def __init__(self, location: str, processor_name: str, processor_options: None):
        """
        Initialize GoogleDocAIProcessor.

        Args:
            location (str): The location of the processor.
            processor_name (str): The name of the processor.
            processor_options: The options to be used for processing.
        """
        self.location = location
        self.processor_name = processor_name
        self.processor_options = processor_options

        # Initialize DocumentProcessorServiceClient with specified location
        self.client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(
                api_endpoint=f"{location}-documentai.googleapis.com"
            )
        )

    def process_document(self, file_path: str, extract_page_number: int) -> Document:
        """
        Process a document using Google Cloud Document AI.

        Args:
            extract_page_number: Which page you want to extract, page number.
            file_path (str): The path to the file to be processed.

        Returns:
            Document: The processed document.

        Raises:
            DocAIException: If there is an error during processing.
        """
        try:
            # Read file content
            file_content = read_files_content(file_path, extract_page_number)

            # Guess MIME type of the file
            mime_type = mimetypes.guess_type(file_path)[0]

            # Log file path and MIME type
            logging.info(f"File path {file_path} and type {mime_type}")

            # Configure the process request
            if self.processor_options:
                logging.info("Requesting using processor option...")
                request = documentai.ProcessRequest(
                    name=self.processor_name,
                    raw_document=documentai.RawDocument(content=file_content, mime_type=mime_type),
                    process_options=self.processor_options,  # Set the processor options
                )
            else:
                request = documentai.ProcessRequest(
                    name=self.processor_name,
                    raw_document=documentai.RawDocument(content=file_content, mime_type=mime_type)
                )

            # Process the document
            result = self.client.process_document(request=request)
        except GoogleAPIError as ex:
            # Handle API errors
            raise DocAIException(processor_name=self.processor_name, error=str(ex))
        else:
            # Return the processed document
            return result.document
