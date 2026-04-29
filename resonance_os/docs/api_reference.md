# ResonanceOS API Documentation

## Overview

The ResonanceOS API provides a comprehensive RESTful interface for style profiling, text generation, and content optimization. The API is built with FastAPI and provides automatic interactive documentation.

## Base URL

```
Development: http://localhost:8000
Production: https://api.resonance-os.com
```

## Authentication

Currently, the API uses API key authentication. Include your API key in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

## Core Endpoints

### Profile Management

#### Create Profile from Corpus

```http
POST /profiles
Content-Type: application/json

{
  "name": "my_style",
  "corpus_path": "/path/to/corpus",
  "description": "My writing style",
  "tier": 2,
  "metadata": {}
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile 'my_style' created successfully",
  "data": {
    "profile_name": "my_style",
    "confidence": 0.92,
    "documents_analyzed": 150,
    "tier": 2
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Create Profile from Text

```http
POST /profiles/create
Content-Type: application/json

{
  "name": "quick_profile",
  "text_content": "Your sample text here...",
  "description": "Quick style profile",
  "tier": 1
}
```

#### List Profiles

```http
GET /profiles
```

**Response:**
```json
{
  "success": true,
  "message": "Found 3 profiles",
  "data": {
    "profiles": [
      {
        "name": "my_style",
        "description": "My writing style",
        "confidence": 0.92,
        "created_at": "2024-01-01T12:00:00Z",
        "format": "json"
      }
    ]
  }
}
```

#### Get Profile Details

```http
GET /profiles/{profile_name}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile 'my_style' retrieved",
  "data": {
    "name": "my_style",
    "description": "My writing style",
    "resonance_vector": [0.85, 0.78, 0.72, ...],
    "dimensions": ["lexical_density", "emotional_valence", ...],
    "confidence": 0.92,
    "emotional_curve": [0.5, 0.6, 0.7, 0.6, 0.5],
    "cadence_pattern": [0.4, 0.6, 0.8, 0.7],
    "abstraction_preference": 0.75
  }
}
```

#### Clone Profile

```http
POST /profiles/{profile_name}/clone
Content-Type: application/json

{
  "new_name": "cloned_style",
  "modifications": {
    "emotional_valence": 0.9,
    "assertiveness_score": 0.8
  }
}
```

#### Delete Profile

```http
DELETE /profiles/{profile_name}
```

### Text Generation

#### Generate Text

```http
POST /generate
Content-Type: application/json

{
  "topic": "The future of artificial intelligence",
  "profile_name": "my_style",
  "max_tokens": 1000,
  "similarity_threshold": 0.92,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "success": true,
  "message": "Text generated successfully",
  "data": {
    "content": "The future of artificial intelligence holds immense promise...",
    "similarity_score": 0.94,
    "target_similarity": 0.92,
    "corrections_made": 2,
    "generation_time": 3.2,
    "tokens_generated": 847,
    "status": "completed",
    "drift_rate": 0.02,
    "profile_used": "my_style"
  }
}
```

#### Progressive Generation

```http
POST /generate/progressive
Content-Type: application/json

{
  "topic": "Machine learning trends",
  "profile_name": "my_style",
  "target_paragraphs": 5,
  "similarity_threshold": 0.95,
  "enable_corrections": true
}
```

#### Batch Generation

```http
POST /generate/batch
Content-Type: application/json

{
  "requests": [
    {
      "topic": "AI in healthcare",
      "profile_name": "medical_style",
      "max_tokens": 800
    },
    {
      "topic": "AI in finance",
      "profile_name": "business_style",
      "max_tokens": 800
    }
  ]
}
```

#### Comparison Generation

```http
POST /generate/comparison
Content-Type: application/json

{
  "topic": "Climate change solutions",
  "profile_names": ["scientific", "journalistic", "creative"],
  "similarity_threshold": 0.90
}
```

### Similarity Analysis

#### Calculate Similarity

```http
POST /similarity
Content-Type: application/json

{
  "profile1_name": "my_style",
  "profile2_name": "professional",
  "method": "cosine"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Similarity calculated",
  "data": {
    "similarity_score": 0.87,
    "method": "cosine",
    "profile1_name": "my_style",
    "profile2_name": "professional"
  }
}
```

#### Similarity Matrix

```http
POST /analyze/similarity-matrix
Content-Type: application/json

{
  "profile_names": ["style1", "style2", "style3"],
  "method": "cosine"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Similarity matrix created",
  "data": {
    "profile_names": ["style1", "style2", "style3"],
    "similarity_matrix": [
      [1.0, 0.85, 0.72],
      [0.85, 1.0, 0.78],
      [0.72, 0.78, 1.0]
    ],
    "method": "cosine",
    "statistics": {
      "average_similarity": 0.78,
      "most_similar_pair": {
        "profile1": "style1",
        "profile2": "style2",
        "similarity": 0.85
      },
      "least_similar_pair": {
        "profile1": "style1",
        "profile2": "style3",
        "similarity": 0.72
      }
    }
  }
}
```

### Profile Evolution

#### Evolve Profile

```http
POST /evolution
Content-Type: application/json

{
  "profile_name": "my_style",
  "target_topics": ["technology", "innovation", "future"],
  "generations": 100,
  "population_size": 50
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile evolution completed",
  "data": {
    "evolved_profile_name": "my_style_evolved",
    "generations_completed": 87,
    "final_fitness": 0.94,
    "fitness_improvement": 0.12,
    "convergence_generation": 87
  }
}
```

### System Management

#### System Statistics

```http
GET /statistics
```

**Response:**
```json
{
  "success": true,
  "message": "Statistics retrieved",
  "data": {
    "profiles": {
      "total_profiles": 15,
      "average_confidence": 0.87
    },
    "generation": {
      "total_generations": 1250,
      "success_rate": 0.94,
      "average_similarity": 0.91
    },
    "drift": {
      "total_measurements": 5000,
      "average_drift_rate": 0.03
    }
  }
}
```

#### Health Check

```http
GET /health
```

**Response:**
```json
{
  "success": true,
  "message": "ResonanceOS API is healthy",
  "data": {
    "status": "healthy",
    "version": "0.1.0"
  }
}
```

#### Detailed Health Check

```http
GET /system/health/detailed
```

**Response:**
```json
{
  "success": true,
  "message": "Health check completed",
  "data": {
    "api": "healthy",
    "components": {
      "profiles": {
        "status": "healthy",
        "profile_count": 15
      },
      "generation": {
        "status": "healthy",
        "total_generations": 1250,
        "success_rate": 0.94
      },
      "drift": {
        "status": "healthy",
        "total_measurements": 5000
      }
    }
  }
}
```

#### Export Data

```http
GET /export
```

#### System Reset

```http
POST /system/reset
Content-Type: application/json

{
  "component": "generation"
}
```

#### Create Backup

```http
POST /backup
```

## Response Format

All API responses follow a consistent format:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "errors": string[] | null,
  "timestamp": string
}
```

## Error Handling

### HTTP Status Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **404**: Not Found
- **422**: Validation Error
- **500**: Internal Server Error

### Error Response Format

```json
{
  "success": false,
  "message": "Validation error",
  "errors": [
    "Profile name is required",
    "Corpus path must exist"
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Rate Limiting

- **Free Tier**: 100 requests per hour
- **Pro Tier**: 1000 requests per hour
- **Enterprise**: Custom limits

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Pagination

List endpoints support pagination:

```http
GET /profiles?page=1&limit=10
```

Response includes pagination metadata:

```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

## Webhooks

### Configure Webhook

```http
POST /webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["profile.created", "generation.completed"],
  "secret": "your_webhook_secret"
}
```

### Webhook Events

- **profile.created**: New profile created
- **generation.completed**: Text generation completed
- **evolution.completed**: Profile evolution completed

### Webhook Payload

```json
{
  "event": "generation.completed",
  "data": {
    "generation_id": "gen_123",
    "profile_name": "my_style",
    "similarity_score": 0.94,
    "timestamp": "2024-01-01T12:00:00Z"
  },
  "signature": "sha256=..."
}
```

## SDK Examples

### Python SDK

```python
from resonance_os import ResonanceOSClient

# Initialize client
client = ResonanceOSClient(api_key="your_api_key")

# Create profile
profile = client.create_profile(
    name="my_style",
    corpus_path="./my_writings/",
    description="My writing style"
)

# Generate text
result = client.generate_text(
    topic="AI and society",
    profile_name="my_style",
    max_tokens=1000
)

print(f"Generated: {result.content}")
print(f"Similarity: {result.similarity_score}")
```

### JavaScript SDK

```javascript
import { ResonanceOSClient } from 'resonance-os-js';

// Initialize client
const client = new ResonanceOSClient('your_api_key');

// Create profile
const profile = await client.createProfile({
  name: 'my_style',
  corpusPath: './my_writings/',
  description: 'My writing style'
});

// Generate text
const result = await client.generateText({
  topic: 'AI and society',
  profileName: 'my_style',
  maxTokens: 1000
});

console.log('Generated:', result.content);
console.log('Similarity:', result.similarityScore);
```

### cURL Examples

```bash
# Create profile
curl -X POST "http://localhost:8000/profiles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "name": "my_style",
    "corpus_path": "./my_writings/",
    "description": "My writing style"
  }'

# Generate text
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "topic": "AI and society",
    "profile_name": "my_style",
    "max_tokens": 1000
  }'
```

## Interactive Documentation

When running the API server locally, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation with testing capabilities.

## Support

- **Documentation**: https://docs.resonance-os.com
- **API Reference**: https://api.resonance-os.com/docs
- **Support**: support@resonance-os.com
- **GitHub Issues**: https://github.com/trenaman/resonance-os/issues
