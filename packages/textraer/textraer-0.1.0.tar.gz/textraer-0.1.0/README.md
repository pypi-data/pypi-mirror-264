# Textraer: Dataset Mention Detection in Documents

We introduce "textraer" which leverages a fine-tuned BERT model, specifically DataBERT, to identify sentences in documents that mention datasets. It's designed to process documents provided via URLs, extract text content sentence by sentence, and classify each sentence to determine whether it mentions a dataset.

## Installation

Before using textraer, ensure you have all necessary dependencies installed. This project requires Python 3.x and the following Python libraries: `transformers`, `datasets`, `nltk`, `PyPDF2`, `tqdm`, and `requests`.

You can install these dependencies using pip:

```bash
pip install transformers datasets nltk PyPDF2 tqdm requests
```

## Initialization

First, import DocumentProcessor from textraer and initialize it with the necessary parameters:

```python
from textraer import DocumentProcessor

organization = 'your_huggingface_org'
json_cache_dir = './cache'
tokenizer_model = 'bert-base-uncased'
model_path = 'jamesliounis/DataBERT'

processor = DocumentProcessor(organization, json_cache_dir, tokenizer_model, model_path)
```

Replace `'your_huggingface_org'` with your Hugging Face organization name and adjust the `json_cache_dir`, `tokenizer_model`, and `model_path` as needed.

## Extracting and Classifying Text

### From a PDF URL

To process a PDF document from a URL, extract its text content sentence by sentence, and classify each sentence, use the following methods:

```python
pdf_url = 'https://arxiv.org/pdf/1706.03762.pdf'  # Example PDF URL
mode = 'sent'  # Extract text sentence by sentence

# Extract sentences from the PDF
sentences = processor.get_doc_from_url(pdf_url, mode)

# Classify each sentence
classifications = processor.classify(sentences)

# Print classification results
for sentence, classification in zip(sentences, classifications):
    print(f"Sentence: {sentence}")
    print(f"Classification: {classification}")
```

### Creating a Dataset
If you want to create a dataset from the processed documents and push it to the Hugging Face Hub:

```python
# Assuming 'sentences' contains your extracted sentences
processor.create_dataset(sentences, mode='sent')
```

This method will push the sentences as a dataset to your specified Hugging Face organization.

### Understanding the Output

The classify method returns a list of dictionaries. Each dictionary contains two keys: 'label' and 'score'. The 'label' key can be either 'LABEL_0' or 'LABEL_1', where 'LABEL_1' indicates a mention of a dataset. The 'score' key provides the confidence level of the classification.




