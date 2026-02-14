import json
import boto3
import os
import uuid

s3 = boto3.client("s3")

UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    file_name = body.get("fileName")
    file_type = body.get("fileType")

    if not file_name:
        return {
            "statusCode": 400,
            "headers": cors_headers(),
            "body": json.dumps({"error": "fileName is required"})
        }

    file_id = str(uuid.uuid4())
    safe_name = file_name.replace(" ", "_")
    s3_key = f"uploads/{file_id}_{safe_name}"

    presigned_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": UPLOAD_BUCKET,
            "Key": s3_key,
            "ContentType": file_type or "application/octet-stream"
        },
        ExpiresIn=300
    )

    return {
        "statusCode": 200,
        "headers": cors_headers(),
        "body": json.dumps({
            "uploadUrl": presigned_url,
            "bucket": UPLOAD_BUCKET,
            "key": s3_key
        })
    }

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
