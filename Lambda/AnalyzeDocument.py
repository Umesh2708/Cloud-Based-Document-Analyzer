import json
import boto3
import os
import re
from datetime import datetime

s3 = boto3.client("s3")
comprehend = boto3.client("comprehend")
dynamodb = boto3.resource("dynamodb")

UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]
TABLE_NAME = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        key = body.get("key")

        if not key:
            return response(400, {"error": "key is required"})

        # Read file from S3
        obj = s3.get_object(Bucket=UPLOAD_BUCKET, Key=key)
        raw_bytes = obj["Body"].read()

        # Support only TXT for simplest free deployment
        # (PDF needs extra library/layer, I can give that also)
        text = raw_bytes.decode("utf-8", errors="ignore")

        text = clean_text(text)

        if len(text) < 5:
            return response(400, {"error": "File has no readable text."})

        # AWS Comprehend has input size limits
        text_for_ai = text[:4500]

        entities = comprehend.detect_entities(Text=text_for_ai, LanguageCode="en")["Entities"]
        phrases = comprehend.detect_key_phrases(Text=text_for_ai, LanguageCode="en")["KeyPhrases"]
        sentiment = comprehend.detect_sentiment(Text=text_for_ai, LanguageCode="en")["Sentiment"]

        # Filter best entities + phrases
        top_entities = []
        for e in entities:
            if e.get("Score", 0) >= 0.80:
                top_entities.append(f"{e['Text']} ({e['Type']})")
        top_entities = list(dict.fromkeys(top_entities))[:10]

        top_phrases = []
        for p in phrases:
            if p.get("Score", 0) >= 0.80:
                top_phrases.append(p["Text"])
        top_phrases = list(dict.fromkeys(top_phrases))[:10]

        # Human readable summary
        summary = f"File analyzed: {key}\n"
        summary += f"Sentiment: {sentiment}\n\n"

        summary += "Top Entities Detected:\n"
        if top_entities:
            for ent in top_entities:
                summary += f"- {ent}\n"
        else:
            summary += "- No strong entities found\n"

        summary += "\nTop Key Phrases:\n"
        if top_phrases:
            for ph in top_phrases:
                summary += f"- {ph}\n"
        else:
            summary += "- No strong key phrases found\n"

        # Save to DynamoDB (optional)
        if TABLE_NAME:
            table = dynamodb.Table(TABLE_NAME)
            table.put_item(Item={
                "fileId": key,
                "sentiment": sentiment,
                "entities": top_entities,
                "keyPhrases": top_phrases,
                "timestamp": datetime.utcnow().isoformat()
            })

        return response(200, {"summary": summary})

    except Exception as e:
        return response(500, {"error": str(e)})

def clean_text(t):
    t = t.replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }
