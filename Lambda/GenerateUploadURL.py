import json
import boto3
import os
import uuid

s3 = boto3.client("s3")

UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        file_name = body.get("fileName")
        file_type = body.get("fileType", "text/plain")

        if not file_name:
            return response(400, {"error": "fileName is required"})

        # generate safe key
        file_id = str(uuid.uuid4())
        safe_name = file_name.replace(" ", "_")
        s3_key = f"uploads/{file_id}_{safe_name}"

        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": UPLOAD_BUCKET,
                "Key": s3_key,
                "ContentType": file_type
            },
            ExpiresIn=300
        )

        return response(200, {
            "uploadUrl": presigned_url,
            "bucket": UPLOAD_BUCKET,
            "key": s3_key
        })

    except Exception as e:
        return response(500, {"error": str(e)})

def response(code, body):
    return {
        "statusCode": code,
        "headers": cors_headers(),
        "body": json.dumps(body)
    }

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
