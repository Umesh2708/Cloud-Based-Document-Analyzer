# 📄 AWS Document Analyzer (Serverless Case Study)

This project is a **serverless document analyzer** built using AWS Cloud services.

A user uploads a **.txt document** from a web frontend.  
The document is stored in **Amazon S3**, and then analyzed using **AWS Comprehend** through AWS Lambda.  
The results are displayed on the frontend in a **human-readable format** and optionally stored in **DynamoDB**.

---

## ✅ Key Features

- Upload `.txt` file from frontend  
- Upload directly to S3 using **Pre-Signed URL**  
- Analyze text using **AWS Comprehend**  
- Extract:
  - Sentiment
  - Entities
  - Key Phrases
  - Summary  
- Display results in frontend  
- Store results in DynamoDB (optional)  
- Frontend hosted using **AWS Amplify**

---

## 🧰 AWS Services Used

- **Amazon S3** – Stores uploaded documents  
- **AWS Lambda** – Backend processing (2 Lambda functions)  
- **Amazon API Gateway (HTTP API)** – Backend routing  
- **AWS Comprehend** – NLP text analysis  
- **Amazon DynamoDB** – Stores analysis results (optional)  
- **AWS Amplify** – Frontend hosting  

---
## 🏗️ Architecture Flow

1. User selects `.txt` file in frontend  
2. Frontend calls API Gateway route `/get-upload-url`  
3. Lambda returns a pre-signed S3 upload URL  
4. Frontend uploads file directly to S3  
5. Frontend calls API Gateway route `/analyze`  
6. Analyze Lambda reads file from S3  
7. Lambda sends text to AWS Comprehend  
8. Analysis results are generated  
9. Frontend displays the results  
10. (Optional) Results stored in DynamoDB  

---

# ✅ Step-by-Step Implementation

---

## Step 1: Create S3 Bucket

Go to:

**Amazon S3 → Create bucket**

Example bucket name:
    `` doc-analyzer-upload-12345 ``
- Keep public access blocked  
- Default settings are sufficient  

---

## Step 2: Enable CORS on S3 Bucket

Go to:

**S3 → Bucket → Permissions → CORS configuration**

Allow:
- Methods: `PUT`, `GET`
- Origins: `*`
- Headers: `*`

This is required because the browser uploads files directly to S3.

---

## Step 3: Create Lambda – GenerateUploadURL

Create a Lambda function:

- Name: `GenerateUploadURL`
- Runtime: Python 3.x

### Environment Variable

| Key | Value |
|---|---|
| `UPLOAD_BUCKET` | `doc-analyzer-upload-12345` |

### Code
Refer to:
   ``lambda/GenerateUploadURL.py``

---

## Step 4: Create Lambda – AnalyzeDocument

Create another Lambda function:

- Name: `AnalyzeDocument`
- Runtime: Python 3.x

### Environment Variables

| Key | Value |
|---|---|
| `UPLOAD_BUCKET` | `doc-analyzer-upload-12345` |
| `TABLE_NAME` | `DocumentAnalysis` (optional) |

### Code
Refer to:
   ``lambda/AnalyzeDocument.py``

---

## Step 5: Create API Gateway (HTTP API)

Go to:

**API Gateway → Create API → HTTP API**

Create the following routes:

### Route 1
- Method: `POST`
- Path: `/get-upload-url`
- Integration: `GenerateUploadURL` Lambda  

### Route 2
- Method: `POST`
- Path: `/analyze`
- Integration: `AnalyzeDocument` Lambda  

---

## Step 6: Enable CORS in API Gateway

Go to:

**API Gateway → CORS**

Enable:
- Allowed origins: `*`
- Allowed methods: `POST`, `OPTIONS`
- Allowed headers: `content-type`

Deploy the API.

---

## Step 7: Create DynamoDB Table (Optional)

Go to:

**DynamoDB → Create table**

- Table name: `DocumentAnalysis`
- Partition key: `fileId` (String)

This table stores:
- File ID
- Sentiment
- Entities
- Key phrases
- Timestamp

---

## Step 8: Frontend Setup

The frontend code is available in:
  ``frontend/index.html``

Inside the file:
- Paste your API Gateway endpoints for:
  - `/get-upload-url`
  - `/analyze`

Refer to the HTML file in this repository for the complete frontend code.

---

## Step 9: Deploy Frontend Using AWS Amplify

Go to:

**AWS Amplify → Host web app**

Steps:
1. Connect your GitHub repository  
2. Select the branch (example: `main`)  
3. Amplify auto-detects a static site  
4. No custom build settings required  
5. Click **Deploy**

Amplify provides a public URL:
       ``https://main.xxxxxx.amplifyapp.com``

This is the final working frontend.

---

## 📌 Output

After uploading a `.txt` document, the frontend displays:

- Document summary  
- Sentiment  
- Detected entities  
- Key phrases  

All output is shown in a **clear, human-readable format**.

---
## 👨‍💻 Author
   Umesh Saini
    > AWS Project
