# Additional API Systems Guide - ResonanceOS v6

## Overview

The Additional API Systems module provides advanced API endpoints and FastAPI server implementation for ResonanceOS v6. This module extends the base API systems with progressive generation, profile comparison, similarity matrices, system management, and comprehensive monitoring capabilities.

## System Architecture

```
Additional API Systems
├── endpoints.py (Advanced API Endpoints)
└── fastapi_server.py (FastAPI Server Implementation)
```

## System Components

### 1. Advanced API Endpoints (`endpoints.py`)

Provides advanced API endpoints for profile management, progressive generation, comparison, analysis, and system management.

#### Architecture

```python
router = APIRouter(prefix="/api/v1", tags=["resonance"])

# Dependencies
profile_persistence = ProfilePersistence()
adaptive_writer = AdaptiveWriter()
```

#### Profile Endpoints

**Create Profile from Text**
```python
POST /api/v1/profiles/create
```

Create a profile directly from text input without needing a corpus.

**Request Parameters:**
- `name`: Profile name
- `text_content`: Text content to analyze
- `description`: Optional profile description
- `tier`: Analysis tier (1-3)

**Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/profiles/create",
    params={
        "name": "my_profile",
        "text_content": "Your sample text here...",
        "description": "My custom profile",
        "tier": 2
    }
)

result = response.json()
print(f"Profile created: {result['data']['profile_name']}")
print(f"Confidence: {result['data']['confidence']}")
```

**Analyze Profile**
```python
GET /api/v1/profiles/{profile_name}/analyze
```

Get detailed analysis of a profile including dimension levels and characteristics.

**Example:**
```python
response = requests.get(
    "http://localhost:8000/api/v1/profiles/professional/analyze"
)

result = response.json()
print(f"Dimension analysis: {result['data']['dimension_analysis']}")
```

**Clone Profile**
```python
POST /api/v1/profiles/{profile_name}/clone
```

Clone a profile with optional modifications to specific dimensions.

**Request Parameters:**
- `profile_name`: Original profile name
- `new_name`: New profile name
- `modifications`: Optional dict of dimension modifications

**Example:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/profiles/professional/clone",
    params={
        "new_name": "professional_modified",
        "modifications": {
            "emotional_valence": 0.8,
            "assertiveness_score": 0.9
        }
    }
)
```

#### Advanced Generation Endpoints

**Progressive Generation**
```python
POST /api/v1/generate/progressive
```

Generate text with paragraph-by-paragraph feedback and progress tracking.

**Request Parameters:**
- `topic`: Generation topic
- `profile_name`: Profile to use
- `target_paragraphs`: Number of paragraphs (default: 5)
- `similarity_threshold`: Target similarity (default: 0.92)
- `enable_corrections`: Enable automatic corrections (default: True)

**Example:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/generate/progressive",
    params={
        "topic": "AI technology in healthcare",
        "profile_name": "professional",
        "target_paragraphs": 5,
        "similarity_threshold": 0.92,
        "enable_corrections": True
    }
)

result = response.json()
print(f"Content: {result['data']['content']}")
print(f"Progress data: {result['data']['progress_data']}")
print(f"Corrections: {result['data']['corrections_made']}")
```

**Comparison Generation**
```python
POST /api/v1/generate/comparison
```

Generate text using multiple profiles for comparison.

**Request Parameters:**
- `topic`: Generation topic
- `profile_names`: List of profile names to compare
- `similarity_threshold`: Target similarity (default: 0.92)

**Example:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/generate/comparison",
    params={
        "topic": "Sustainable energy",
        "profile_names": ["professional", "creative", "technical"],
        "similarity_threshold": 0.92
    }
)

result = response.json()
for r in result['data']['results']:
    print(f"{r['profile_name']}: similarity={r['similarity_score']:.3f}")
```

#### Analysis Endpoints

**Similarity Matrix**
```python
POST /api/v1/analyze/similarity-matrix
```

Create a similarity matrix for multiple profiles.

**Request Parameters:**
- `profile_names`: List of profile names
- `method`: Similarity method (default: COSINE)

**Example:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/analyze/similarity-matrix",
    params={
        "profile_names": ["professional", "creative", "technical"],
        "method": "COSINE"
    }
)

result = response.json()
print(f"Matrix: {result['data']['similarity_matrix']}")
print(f"Most similar: {result['data']['statistics']['most_similar_pair']}")
print(f"Least similar: {result['data']['statistics']['least_similar_pair']}")
```

**Dimension Importance**
```python
GET /api/v1/analyze/dimension-importance
```

Get importance weights for different resonance dimensions.

**Example:**
```python
response = requests.get(
    "http://localhost:8000/api/v1/analyze/dimension-importance"
)

result = response.json()
print(f"Feature weights: {result['data']['feature_weights']}")
```

#### System Management Endpoints

**Reset System**
```python
POST /api/v1/system/reset
```

Reset system components (generation, drift detector, parameters).

**Request Parameters:**
- `component`: Component to reset (all, generation, drift, parameters)

**Example:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/system/reset",
    params={"component": "generation"}
)

result = response.json()
print(f"Reset components: {result['data']['reset_components']}")
```

**Detailed Health Check**
```python
GET /api/v1/system/health/detailed
```

Get detailed health check with component status.

**Example:**
```python
response = requests.get(
    "http://localhost:8000/api/v1/system/health/detailed"
)

result = response.json()
print(f"Overall status: {result['data']['api']}")
print(f"Components: {result['data']['components']}")
```

### 2. FastAPI Server (`fastapi_server.py`)

Complete FastAPI server implementation with CORS, middleware, background tasks, and comprehensive error handling.

#### Architecture

```python
app = FastAPI(
    title="ResonanceOS API",
    description="Adaptive Stylistic Alignment Engine",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global components
corpus_loader = CorpusLoader()
vector_builder = StyleVectorBuilder()
profile_persistence = ProfilePersistence()
adaptive_writer = AdaptiveWriter()
tone_evolver = ToneEvolver()
```

#### Server Configuration

**CORS Middleware**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Request Logging Middleware**
```python
@app.middleware("http")
async def log_requests(request, call_next):
    """Log API requests"""
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_api_request(request.method, str(request.url), response.status_code, process_time)
    return response
```

#### Core Endpoints

**Health Check**
```python
GET /health
```

Basic health check endpoint.

**Example:**
```python
response = requests.get("http://localhost:8000/health")
result = response.json()
print(f"Status: {result['data']['status']}")
```

#### Profile Management Endpoints

**Create Profile**
```python
POST /profiles
```

Create a new style profile from corpus.

**Request Body:**
```json
{
  "name": "professional",
  "corpus_path": "/path/to/corpus",
  "description": "Professional business writing",
  "tier": 2,
  "metadata": {"industry": "business"}
}
```

**Example:**
```python
response = requests.post(
    "http://localhost:8000/profiles",
    json={
        "name": "professional",
        "corpus_path": "/path/to/corpus",
        "description": "Professional business writing",
        "tier": 2
    }
)
```

**List Profiles**
```python
GET /profiles
```

List all available profiles.

**Example:**
```python
response = requests.get("http://localhost:8000/profiles")
result = response.json()
for profile in result['data']['profiles']:
    print(f"{profile['name']}: {profile['confidence']:.2f}")
```

**Get Profile**
```python
GET /profiles/{profile_name}
```

Get detailed profile information.

**Example:**
```python
response = requests.get("http://localhost:8000/profiles/professional")
result = response.json()
print(f"Vector: {result['data']['resonance_vector']}")
print(f"Dimensions: {result['data']['dimensions']}")
```

**Delete Profile**
```python
DELETE /profiles/{profile_name}
```

Delete a profile.

**Example:**
```python
response = requests.delete("http://localhost:8000/profiles/old_profile")
```

#### Generation Endpoints

**Generate Text**
```python
POST /generate
```

Generate text with style alignment.

**Request Body:**
```json
{
  "topic": "AI technology benefits",
  "profile_name": "professional",
  "max_tokens": 2048,
  "similarity_threshold": 0.92
}
```

**Example:**
```python
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "AI technology benefits",
        "profile_name": "professional",
        "max_tokens": 2048,
        "similarity_threshold": 0.92
    }
)

result = response.json()
print(f"Content: {result['data']['content']}")
print(f"Similarity: {result['data']['similarity_score']:.3f}")
print(f"Corrections: {result['data']['corrections_made']}")
```

**Batch Generation**
```python
POST /generate/batch
```

Generate multiple texts in batch.

**Request Body:**
```json
[
  {
    "topic": "AI in healthcare",
    "profile_name": "professional",
    "max_tokens": 500
  },
  {
    "topic": "AI in finance",
    "profile_name": "professional",
    "max_tokens": 500
  }
]
```

**Example:**
```python
requests = [
    {"topic": "AI in healthcare", "profile_name": "professional", "max_tokens": 500},
    {"topic": "AI in finance", "profile_name": "professional", "max_tokens": 500}
]

response = requests.post(
    "http://localhost:8000/generate/batch",
    json=requests
)

result = response.json()
print(f"Generated: {len(result['data']['results'])} texts")
print(f"Statistics: {result['data']['statistics']}")
```

#### Similarity Endpoints

**Calculate Similarity**
```python
POST /similarity
```

Calculate similarity between two profiles.

**Request Body:**
```json
{
  "profile1_name": "professional",
  "profile2_name": "creative",
  "method": "COSINE"
}
```

**Example:**
```python
response = requests.post(
    "http://localhost:8000/similarity",
    json={
        "profile1_name": "professional",
        "profile2_name": "creative",
        "method": "COSINE"
    }
)

result = response.json()
print(f"Similarity: {result['data']['similarity_score']:.3f}")
```

#### Evolution Endpoints

**Evolve Profile**
```python
POST /evolution
```

Evolve a profile to improve performance using genetic algorithms.

**Request Body:**
```json
{
  "profile_name": "professional",
  "target_topics": ["AI", "technology", "innovation"],
  "generations": 100,
  "population_size": 50
}
```

**Example:**
```python
response = requests.post(
    "http://localhost:8000/evolution",
    json={
        "profile_name": "professional",
        "target_topics": ["AI", "technology"],
        "generations": 100,
        "population_size": 50
    }
)

result = response.json()
print(f"Evolved profile: {result['data']['evolved_profile_name']}")
print(f"Final fitness: {result['data']['final_fitness']:.3f}")
```

#### Statistics and Monitoring Endpoints

**Get Statistics**
```python
GET /statistics
```

Get comprehensive system statistics.

**Example:**
```python
response = requests.get("http://localhost:8000/statistics")
result = response.json()
print(f"Profiles: {result['data']['profiles']}")
print(f"Generation: {result['data']['generation']}")
print(f"Drift: {result['data']['drift']}")
print(f"Parameters: {result['data']['parameters']}")
```

**Export Data**
```python
GET /export
```

Export all system data.

**Example:**
```python
response = requests.get("http://localhost:8000/export")
result = response.json()
print(f"Profiles: {len(result['data']['profiles'])}")
print(f"Generation data: {result['data']['generation_data']}")
```

#### Background Task Endpoints

**Create Backup**
```python
POST /backup
```

Create system backup in background.

**Example:**
```python
response = requests.post("http://localhost:8000/backup")
result = response.json()
print(f"Status: {result['message']}")
```

#### Error Handling

**404 Handler**
```python
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content=APIResponse(
            success=False,
            message="Resource not found",
            errors=["The requested resource was not found"]
        ).dict()
    )
```

**500 Handler**
```python
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            message="Internal server error",
            errors=["An unexpected error occurred"]
        ).dict()
    )
```

#### Server Lifecycle

**Startup Event**
```python
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("ResonanceOS API starting up")
    # Ensure directories exist
    config.paths.profiles_dir.mkdir(parents=True, exist_ok=True)
    # ... more initialization
```

**Shutdown Event**
```python
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("ResonanceOS API shutting down")
    # Save pending data, create backup
```

#### Running the Server

**Direct Execution**
```bash
python -m resonance_os.api.fastapi_server
```

**Using run_server Function**
```python
from resonance_os.api.fastapi_server import run_server

run_server(host="0.0.0.0", port=8000, workers=4, reload=True)
```

**Using uvicorn**
```bash
uvicorn resonance_os.api.fastapi_server:app --host 0.0.0.0 --port 8000 --workers 4 --reload
```

## Integration Points

The Additional API Systems module integrates with:

- **Core Systems**: Uses types, config, and logging
- **Profiling Systems**: Uses profile persistence and style vector builder
- **Generation Systems**: Uses adaptive writer and batch generator
- **Similarity Systems**: Uses similarity calculator
- **Evolution Systems**: Uses tone evolver

## Usage Patterns

### Progressive Generation with Monitoring

```python
import requests

# Generate with progress tracking
response = requests.post(
    "http://localhost:8000/api/v1/generate/progressive",
    params={
        "topic": "AI technology",
        "profile_name": "professional",
        "target_paragraphs": 10
    }
)

result = response.json()
progress = result['data']['progress_data']

for step in progress:
    print(f"Paragraph {step['paragraph']}: {step['content_length']} chars")
```

### Profile Comparison

```python
# Compare multiple profiles
response = requests.post(
    "http://localhost:8000/api/v1/generate/comparison",
    params={
        "topic": "Sustainable energy",
        "profile_names": ["professional", "creative", "technical"]
    }
)

result = response.json()
summary = result['data']['summary']
print(f"Best similarity: {summary['best_similarity']:.3f}")
```

### Similarity Analysis

```python
# Create similarity matrix
response = requests.post(
    "http://localhost:8000/api/v1/analyze/similarity-matrix",
    params={
        "profile_names": ["prof1", "prof2", "prof3", "prof4"],
        "method": "COSINE"
    }
)

result = response.json()
matrix = result['data']['similarity_matrix']

# Visualize matrix
import matplotlib.pyplot as plt
import seaborn as sns

sns.heatmap(matrix, annot=True)
plt.show()
```

### System Monitoring

```python
# Get detailed health
response = requests.get("http://localhost:8000/api/v1/system/health/detailed")
health = response.json()

for component, status in health['data']['components'].items():
    print(f"{component}: {status['status']}")

# Get statistics
response = requests.get("http://localhost:8000/statistics")
stats = response.json()

print(f"Total generations: {stats['data']['generation']['total_generations']}")
print(f"Success rate: {stats['data']['generation']['success_rate']:.2%}")
```

## Best Practices

1. **Use appropriate similarity thresholds**: Don't set too high or too low
2. **Monitor progress**: Use progressive generation for long content
3. **Batch operations**: Use batch generation for multiple requests
4. **Regular backups**: Schedule regular backups via background tasks
5. **Health monitoring**: Regularly check system health and statistics
6. **Error handling**: Implement proper error handling in clients
7. **Rate limiting**: Implement rate limiting for production use
8. **Authentication**: Add authentication for production deployments

## Common Issues

**Issue**: Profile not found
**Solution**: Verify profile exists and name is correct

**Issue**: Generation timeout
**Solution**: Reduce max_tokens or use progressive generation

**Issue**: CORS errors
**Solution**: Configure CORS middleware appropriately

**Issue**: Slow batch generation
**Solution**: Reduce concurrent requests or increase workers

## Performance Considerations

- **Async operations**: All endpoints are async for better performance
- **Background tasks**: Long-running operations use background tasks
- **Batch processing**: Batch generation is more efficient than individual calls
- **Caching**: Consider caching profile data for frequently accessed profiles
- **Connection pooling**: Use connection pooling for database operations

## Security Considerations

- **Authentication**: Add authentication middleware for production
- **Rate limiting**: Implement rate limiting to prevent abuse
- **Input validation**: All inputs are validated via Pydantic models
- **CORS**: Configure CORS appropriately for your use case
- **HTTPS**: Use HTTPS in production
- **API keys**: Require API keys for sensitive operations

## Future Enhancements

- **WebSocket support**: Real-time generation progress updates
- **Authentication**: OAuth2 and JWT authentication
- **Rate limiting**: Built-in rate limiting
- **Caching**: Redis caching for profiles and results
- **Webhooks**: Webhook notifications for long-running tasks
- **API versioning**: Proper API versioning strategy
- **GraphQL**: GraphQL endpoint alternative

## Dependencies

```bash
pip install fastapi uvicorn
pip install python-multipart  # For form data
pip install python-jose[cryptography]  # For JWT
pip install passlib[bcrypt]  # For password hashing
```

## References

- [API Systems Guide](./api-systems-guide.md)
- [Additional Generation Systems Guide](./additional-generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)
