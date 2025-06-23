from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from src.workflow import Workflow
from fastapi.middleware.cors import CORSMiddleware # NEW: Import CORS middleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app and workflow agent
app = FastAPI()
workflow = Workflow()

# NEW: Configure CORS middleware
# This list specifies which origins (domains/ports) are allowed to make requests to your API.
# You MUST include 'http://localhost:8080' for your local development.
# When you deploy your frontend, add its production URL here as well.
origins = [
    "http://localhost:8080",  # Your local frontend development server
    # "https://research-ai-frontend-4qn2.onrender.com", # <--- ADDED: Your deployed frontend URL
    # If you need to allow all origins during initial development (less secure, use with caution):
    # "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,         # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allow all headers in cross-origin requests
)


# Define request model
class QueryRequest(BaseModel):
    query: str

# Health check route
@app.get("/")
def root():
    return {"status": "🟢 Developer Tools Research API is live"}

# Research endpoint
@app.post("/run-research")
def run_research(request: QueryRequest):
    result = workflow.run(request.query)

    companies = [
        {
            "name": c.name,
            "website": c.website,
            "pricing_model": c.pricing_model,
            "is_open_source": c.is_open_source,
            "tech_stack": c.tech_stack[:5] if c.tech_stack else [],
            "language_support": c.language_support[:5] if c.language_support else [],
            "api_available": "✅ Available" if c.api_available else "❌ Not Available" if c.api_available is not None else None,
            "integration_capabilities": c.integration_capabilities[:4] if c.integration_capabilities else [],
            "description": c.description if c.description != "Analysis failed" else None
        }
        for c in result.companies
    ]

    return {
        "query": request.query,
        "companies": companies,
        "developer_recommendations": result.analysis
    }

# uvicorn main:app --reload --port 8000
