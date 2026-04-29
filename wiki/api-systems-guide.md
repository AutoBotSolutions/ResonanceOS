# API Systems Guide - ResonanceOS v6

## Overview

The API Systems module provides external communication protocols for ResonanceOS v6, enabling programmatic access to human-resonant content generation through a simple, dependency-free server implementation.

## System Architecture

```
API Systems
├── hr_server.py (HTTP Server)
├── Request/Response Models
└── Route Handlers
```

## System Components

### 1. HR Server (`hr_server.py`)

A lightweight HTTP server implementation that provides programmatic access to human-resonant content generation without requiring external dependencies like FastAPI.

#### Architecture

```python
# Request Model
class SimpleRequest:
    def __init__(self, prompt: str, tenant: str = None, profile_name: str = None):
        self.prompt = prompt
        self.tenant = tenant
        self.profile_name = profile_name

# Response Model
class SimpleResponse:
    def __init__(self, article: str, hrv_feedback: List[float]):
        self.article = article
        self.hrv_feedback = hrv_feedback

# Server Implementation
class SimpleApp:
    def __init__(self):
        self.routes = {}
    
    def post(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
```

#### Initialization

```python
# Initialize components
writer = HumanResonantWriter()
profile_manager = HRVProfileManager(Path("./profiles/hr_profiles"))

# Create app instance
app = SimpleApp()
app.post("/hr_generate")(hr_generate)
```

### 2. Endpoints

#### POST /hr_generate

Generate human-resonant content based on a prompt.

**Request:**
```json
{
  "prompt": "The future of artificial intelligence",
  "tenant": "default",
  "profile_name": "professional"
}
```

**Response:**
```json
{
  "article": "Generated content here...",
  "hrv_feedback": [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
}
```

**Parameters:**
- `prompt` (required): Content generation prompt
- `tenant` (optional): Tenant identifier for multi-tenant profile management
- `profile_name` (optional): Profile name for HRV targeting

**Response Fields:**
- `article`: Generated human-resonant content
- `hrv_feedback`: 8-dimensional HRV vector representing content characteristics

#### Usage Example

```python
from resonance_os.api.hr_server import SimpleRequest, hr_generate

# Create request
req = SimpleRequest(
    prompt="Write about sustainable technology",
    tenant="default",
    profile_name="professional"
)

# Generate content
resp = hr_generate(req)
print(resp.article)
print(resp.hrv_feedback)
```

### 3. Integration Patterns

#### Direct Python Integration

```python
from resonance_os.api.hr_server import SimpleRequest, hr_generate

def generate_content(prompt: str, profile: str = None) -> dict:
    req = SimpleRequest(prompt=prompt, profile_name=profile)
    resp = hr_generate(req)
    return {
        "content": resp.article,
        "hrv": resp.hrv_feedback
    }
```

#### Multi-Tenant Generation

```python
from resonance_os.api.hr_server import SimpleRequest, hr_generate

def generate_for_tenant(tenant: str, prompt: str, profile: str) -> dict:
    req = SimpleRequest(prompt=prompt, tenant=tenant, profile_name=profile)
    resp = hr_generate(req)
    return resp.article
```

#### Batch Processing

```python
from resonance_os.api.hr_server import SimpleRequest, hr_generate

prompts = [
    "Introduction to machine learning",
    "AI in healthcare",
    "Ethical considerations in AI"
]

results = []
for prompt in prompts:
    req = SimpleRequest(prompt=prompt, profile_name="professional")
    resp = hr_generate(req)
    results.append({"prompt": prompt, "article": resp.article})
```

## Integration Points

The API Systems module integrates with:

- **Generation Systems**: Uses HumanResonantWriter for content generation
- **Profile Systems**: Uses HRVProfileManager for multi-tenant profile management
- **Core Systems**: Uses HRV types and constants for data structures

## Configuration

### Profile Directory

The server expects profiles to be stored in `./profiles/hr_profiles/` by default. This can be customized by modifying the initialization:

```python
profile_manager = HRVProfileManager(Path("/custom/path/to/profiles"))
```

### Custom Routes

Additional routes can be added to the SimpleApp:

```python
app = SimpleApp()

@app.post("/custom_endpoint")
def custom_handler(req):
    # Custom logic here
    return SimpleResponse(article="...", hrv_feedback=[...])
```

## Performance Considerations

- **Lightweight**: No external dependencies required
- **Fast**: Simple request/response cycle
- **Scalable**: Can be deployed behind load balancers
- **Stateless**: Each request is independent

## Security Considerations

- **Authentication**: Not implemented in basic version
- **Rate Limiting**: Not implemented in basic version
- **Input Validation**: Basic validation recommended
- **HTTPS**: Should be deployed behind reverse proxy for production

## Best Practices

1. **Validate inputs**: Sanitize prompts to prevent injection attacks
2. **Handle errors**: Implement proper error handling for production
3. **Log requests**: Monitor API usage and performance
4. **Use profiles**: Leverage profile system for consistent results
5. **Monitor HRV feedback**: Track HRV alignment with expectations

## Common Issues

**Issue**: Profile not found
**Solution**: Verify profile exists in the profiles directory and tenant is correct

**Issue**: Empty content generation
**Solution**: Check prompt quality and ensure generation components are properly initialized

**Issue**: Slow response times
**Solution**: Profile generation pipeline and consider caching for repeated prompts

## Deployment

### Development

```bash
# Run server in development mode
python -m resonance_os.api.hr_server
```

### Production

For production deployment, consider:

1. **Reverse Proxy**: Use nginx or Apache for HTTPS and load balancing
2. **Process Manager**: Use gunicorn or supervisor for process management
3. **Monitoring**: Implement logging and monitoring
4. **Authentication**: Add API key authentication
5. **Rate Limiting**: Implement rate limiting to prevent abuse

### Docker Deployment

```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "resonance_os.api.hr_server"]
```

## Future Enhancements

- **FastAPI Integration**: Full FastAPI implementation with auto-generated docs
- **Authentication**: API key or OAuth2 authentication
- **Rate Limiting**: Request rate limiting
- **WebSocket Support**: Real-time generation updates
- **Batch Endpoint**: Dedicated batch processing endpoint
- **Webhook Support**: Async webhook notifications
- **Streaming**: Streaming response for long content

## Troubleshooting

**Issue**: Import errors
**Solution**: Ensure resonance_os is properly installed and in Python path

**Issue**: Port already in use
**Solution**: Change server port or stop conflicting process

**Issue**: Profile loading errors
**Solution**: Verify profile directory structure and file permissions

## API Reference

### hr_generate(req: SimpleRequest) -> SimpleResponse

Generate human-resonant content.

**Parameters:**
- `req` (SimpleRequest): Request object containing prompt and optional profile info

**Returns:**
- `SimpleResponse`: Response object containing generated content and HRV feedback

**Raises:**
- `ValueError`: If prompt is empty or invalid
- `FileNotFoundError`: If specified profile doesn't exist

## References

- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [CLI Systems Guide](./cli-systems-guide.md)
