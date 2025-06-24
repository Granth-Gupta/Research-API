from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from src.workflow import Workflow

# Load environment variables
load_dotenv()

# Initialize FastAPI app and workflow agent
app = FastAPI()
workflow = Workflow()

# Define the origins that are allowed to make requests to your API
# In a production environment, you should replace "*" with the specific domain(s) of your frontend application.
# For example: origins = ["https://research-ai-frontend.gh2.onrender.com"]
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",  # Your local frontend development server
    "https://research-ai-frontend-4qh2.onrender.com", # Your deployed frontend
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows specific origins
    allow_credentials=True, # Allows cookies to be included in cross-origin requests
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
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
