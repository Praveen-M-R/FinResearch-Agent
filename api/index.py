"""
Vercel serverless function handler for FastAPI application
"""

from mangum import Mangum
from app.main import app

# Create the Mangum handler for AWS Lambda (Vercel uses Lambda under the hood)
handler = Mangum(app, lifespan="off")
