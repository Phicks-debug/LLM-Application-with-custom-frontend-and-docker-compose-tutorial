from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import boto3
import json
import os
from botocore.exceptions import ClientError
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],
    expose_headers=["*"],
)

# Safely print CORS middleware configuration
try:
    print("CORS middleware configured with the following settings:")
    if app.middleware_stack and app.middleware_stack.middlewares:
        cors_middleware = next((m for m in app.middleware_stack.middlewares if isinstance(m, CORSMiddleware)), None)
        if cors_middleware:
            print(f"allow_origins: {cors_middleware.options['allow_origins']}")
            print(f"allow_methods: {cors_middleware.options['allow_methods']}")
            print(f"allow_headers: {cors_middleware.options['allow_headers']}")
        else:
            print("CORS middleware not found in the middleware stack.")
    else:
        print("Middleware stack is not initialized yet.")
except Exception as e:
    print(f"Error occurred while trying to print CORS configuration: {str(e)}")

# Enable CORS logging
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Received request: {request.method} {request.url}")
    print(f"Request headers: {request.headers}")
    response = await call_next(request)
    print(f"Returning response: {response.status_code}")
    return response

# Use environment variables for configuration
REGION_NAME = os.environ.get('AWS_REGION', 'us-east-1')
MODEL_ID = os.environ.get('MODEL_ID', 'amazon.titan-text-premier-v1:0')

# Create a single boto3 client to be reused
runtime = boto3.client('bedrock-runtime', region_name=REGION_NAME)

@app.get("/chat/clear")
def clear():
    return {"message": "Chat history is cleared"}

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/chat")
async def invoke(prompt: str, request: Request):
    print(f"Received chat request with prompt: {prompt}")
    print(f"Request headers: {request.headers}")
    print(f"Request method: {request.method}")
    print(f"Request URL: {request.url}")
    try:
        kwargs = {
            "modelId": MODEL_ID,
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 3072,
                    "stopSequences": [],
                    "temperature": 0.7,
                    "topP": 0.9
                }
            })
        }
        
        print("Invoking Bedrock model...")
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, lambda: runtime.invoke_model(**kwargs)
        )
        
        print("Parsing response...")
        response_body = json.loads(result.get("body").read().decode())
        message = response_body.get("results", [{}])[0].get("outputText", "")
        print(f"Generated message: {message}")
        return {"message": message}
    
    except ClientError as e:
        print(f"AWS API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AWS API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting API server...")
    print(f"CORS settings: {app.middleware_stack.middlewares[0].options}")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug", reload=True, ssl_keyfile=None, ssl_certfile=None)
