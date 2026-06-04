# Deployment

The service is packaged as a Dockerized FastAPI app. A generic cloud deployment would include:

- containerized API service
- managed secrets
- managed vector database
- centralized logging
- request and retrieval latency metrics
- trace metadata for AI behavior
- CI/CD pipeline with tests, safety scan, and evaluation
- deployment rollback workflow

The local vector index is suitable for demonstration. A larger environment should use a managed retrieval backend, access controls, backup policies, and environment-specific configuration.

