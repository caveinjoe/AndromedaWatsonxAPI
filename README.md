# Andromeda Project
**Powered by watsonx**

This project provides API solutions for extracting and analyzing news data, allowing users to retrieve structured information based on document identifiers.

---

## Currently Available API(s)

### News Extraction API by Document ID

This API allows users to retrieve detailed news information based on a unique document ID. The response is a JSON list containing essential details about the specified document, including metadata and analytical insights.

---

## Getting Started

### Prerequisites
- **Python** 3.x

### Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/caveinjoe/AndromedaWatsonxAPI.git
    ```
2. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Create .env file with the following variables. Replace the placeholder values with your actual values.
    ```bash
    # Watson Discovery
    WD_API_KEY="YOUR_KEY"
    WD_BASE_URL="YOUR_URL"
    WD_PROJECT_ID="YOUR_PROJECT_ID"

    # watsonx
    WX_API_KEY="YOUR_KEY" 
    WX_BASE_URL="YOUR_URL"
    WX_PROJECT_ID="YOUR_PROJECT_ID"
    ```
4. Run the API
    ```bash
    python host_watsonx_api.py
    ```

---

## API Documentation

### News Extraction by Document ID

**Endpoint**: `/api/extract_news_by_doc_id`

**Method**: `GET`

**Description**: Retrieve structured news data using a unique `doc_id`.

#### Query Parameters
- **`doc_id`** (required): The document ID for retrieving the relevant news information.

#### Example Request

```http
GET /api/extract_news_by_doc_id?doc_id=document_id_1234
```

#### Example Response

The API returns a JSON array with the following document details:

```json
[
    "document_id_1234",
    "Document Title",
    "This is a brief summary of the document.",
    "Main Headline of the News",
    "en",
    "Technology",
    ["County1", "County2"],
    "Positive",
    ["Organization1", "Organization2"],
    ["Person1", "Person2"],
    "Additional analysis insights",
    "Key insights from the document."
]
```
#### Response Fields
- **`document_id`**: Unique identifier of the document.
- **`title`**: Title of the document.
- **`summary`**: Brief summary of the content.
- **`headline`**: Main headline of the news.
- **`language`**: Document language.
- **`category`**: News category.
- **`countries`**: List of countries associated with the news.
- **`sentiment`**: Sentiment analysis result.
- **`organization`**: Organizations mentioned.
- **`person`**: People mentioned.
- **`analysis`**: Additional analytical insights.
- **`insight`**: Key insights derived from the document.



