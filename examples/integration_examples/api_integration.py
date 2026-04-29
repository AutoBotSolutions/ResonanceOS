#!/usr/bin/env python3
"""
API Integration Example

This example demonstrates how to integrate with ResonanceOS v6 API,
including REST API calls, authentication, error handling, and response processing.
"""

import sys
import os
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, List

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.api.hr_server import app, SimpleRequest, hr_generate


class ResonanceOSAPIClient:
    """Client for interacting with ResonanceOS v6 API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ResonanceOS-Client/1.0'
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def generate_content(self, prompt: str, tenant: str = None, 
                        profile_name: str = None, **kwargs) -> Dict[str, Any]:
        """Generate content using API"""
        request_data = {
            "prompt": prompt
        }
        
        if tenant:
            request_data["tenant"] = tenant
        if profile_name:
            request_data["profile_name"] = profile_name
        
        # Add additional parameters
        request_data.update(kwargs)
        
        try:
            response = self.session.post(
                f"{self.base_url}/hr_generate",
                json=request_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "response_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def get_profiles(self, tenant: str = None) -> Dict[str, Any]:
        """Get available profiles"""
        try:
            params = {}
            if tenant:
                params["tenant"] = tenant
            
            response = self.session.get(
                f"{self.base_url}/profiles",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def create_profile(self, tenant: str, profile_name: str, 
                      hrv_vector: List[float], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new profile"""
        request_data = {
            "tenant": tenant,
            "profile_name": profile_name,
            "hrv_vector": hrv_vector
        }
        
        if metadata:
            request_data["metadata"] = metadata
        
        try:
            response = self.session.post(
                f"{self.base_url}/profiles",
                json=request_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        try:
            response = self.session.get(
                f"{self.base_url}/metrics",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}


def basic_api_example():
    """Demonstrate basic API usage"""
    print("🌐 Basic API Integration Example")
    print("=" * 50)
    
    # Initialize API client
    client = ResonanceOSAPIClient()
    
    # Health check
    print("🔍 Checking API health...")
    health = client.health_check()
    
    if health.get("status") == "error":
        print(f"❌ API health check failed: {health['message']}")
        print("Make sure the ResonanceOS API server is running on localhost:8000")
        return
    
    print("✅ API is healthy!")
    print(f"Status: {health}")
    print()
    
    # Generate content
    print("📝 Generating content via API...")
    prompts = [
        "The future of artificial intelligence",
        "Sustainable technology solutions",
        "Digital transformation strategies"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"Request {i}: {prompt}")
        
        result = client.generate_content(prompt)
        
        if result.get("status") == "error":
            print(f"❌ Generation failed: {result['message']}")
        else:
            print(f"✅ Generated {len(result.get('article', ''))} characters")
            print(f"HRV Feedback: {result.get('hrv_feedback', 'N/A')}")
            print(f"Profile: {result.get('profile_name', 'default')}")
        
        print()
    
    print("✅ Basic API example completed!")


def advanced_api_example():
    """Demonstrate advanced API features"""
    print("\n🚀 Advanced API Integration Example")
    print("=" * 50)
    
    client = ResonanceOSAPIClient()
    
    # Test with different profiles
    print("🎨 Testing with different profiles...")
    
    test_prompt = "The importance of innovation in business"
    profiles_to_test = ["neutral_professional", "creative_storytelling", "marketing_enthusiastic"]
    
    for profile in profiles_to_test:
        print(f"Testing profile: {profile}")
        
        result = client.generate_content(
            prompt=test_prompt,
            profile_name=profile
        )
        
        if result.get("status") == "error":
            print(f"❌ Failed with profile {profile}: {result['message']}")
        else:
            print(f"✅ Success with {profile}")
            print(f"   HRV: {result.get('hrv_feedback', 'N/A'):.3f}")
            print(f"   Length: {len(result.get('article', ''))}")
        
        print()
    
    # Test tenant-specific generation
    print("🏢 Testing tenant-specific generation...")
    
    tenant_result = client.generate_content(
        prompt="Company quarterly report",
        tenant="demo_tenant",
        profile_name="professional_business"
    )
    
    if tenant_result.get("status") == "error":
        print(f"❌ Tenant generation failed: {tenant_result['message']}")
    else:
        print("✅ Tenant-specific generation successful")
        print(f"   Tenant: {tenant_result.get('tenant', 'N/A')}")
        print(f"   Profile: {tenant_result.get('profile_name', 'N/A')}")
    
    print()
    print("✅ Advanced API example completed!")


def batch_api_requests():
    """Demonstrate batch API requests"""
    print("\n📦 Batch API Requests Example")
    print("=" * 50)
    
    client = ResonanceOSAPIClient()
    
    # Prepare batch requests
    batch_requests = [
        {"prompt": "Introduction to machine learning", "profile_name": "technical_academic"},
        {"prompt": "Marketing strategy for startups", "profile_name": "marketing_enthusiastic"},
        {"prompt": "Creative writing tips", "profile_name": "creative_storytelling"},
        {"prompt": "Business report summary", "profile_name": "professional_business"},
        {"prompt": "Social media content", "profile_name": "marketing_enthusiastic"}
    ]
    
    print(f"Processing {len(batch_requests)} batch requests...")
    print()
    
    results = []
    start_time = time.time()
    
    for i, request in enumerate(batch_requests, 1):
        print(f"Processing request {i}/{len(batch_requests)}: {request['prompt'][:30]}...")
        
        result = client.generate_content(**request)
        
        if result.get("status") == "error":
            print(f"❌ Failed: {result['message']}")
        else:
            print(f"✅ Success: {len(result.get('article', ''))} chars")
        
        results.append({
            "request": request,
            "result": result,
            "success": result.get("status") != "error"
        })
    
    total_time = time.time() - start_time
    
    # Batch statistics
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"\n📊 Batch Processing Statistics:")
    print(f"Total Requests: {len(batch_requests)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {successful/len(batch_requests)*100:.1f}%")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Avg Time per Request: {total_time/len(batch_requests):.2f} seconds")
    
    return results


def error_handling_example():
    """Demonstrate comprehensive error handling"""
    print("\n⚠️ Error Handling Example")
    print("=" * 50)
    
    client = ResonanceOSAPIClient()
    
    # Test various error conditions
    error_tests = [
        {
            "name": "Invalid URL",
            "test": lambda: ResonanceOSAPIClient("http://invalid-url:8000").health_check()
        },
        {
            "name": "Timeout",
            "test": lambda: ResonanceOSAPIClient(timeout=0.001).generate_content("test")
        },
        {
            "name": "Invalid Profile",
            "test": lambda: client.generate_content("test", profile_name="invalid_profile")
        },
        {
            "name": "Empty Prompt",
            "test": lambda: client.generate_content("")
        },
        {
            "name": "Very Long Prompt",
            "test": lambda: client.generate_content("x" * 10000)
        }
    ]
    
    for error_test in error_tests:
        print(f"Testing: {error_test['name']}")
        
        try:
            result = error_test["test"]()
            
            if result.get("status") == "error":
                print(f"✅ Error handled correctly: {result['message']}")
            else:
                print(f"⚠️  Expected error but got success")
        except Exception as e:
            print(f"✅ Exception handled correctly: {str(e)}")
        
        print()
    
    print("✅ Error handling example completed!")


def performance_monitoring_example():
    """Demonstrate API performance monitoring"""
    print("\n📈 Performance Monitoring Example")
    print("=" * 50)
    
    client = ResonanceOSAPIClient()
    
    # Performance test parameters
    test_prompts = [
        "Short prompt",
        "This is a medium length prompt that contains more detail and context for the AI to work with",
        "This is a very long prompt that includes extensive detail, multiple clauses, and complex sentence structures that might challenge the API's processing capabilities and affect response times significantly"
    ]
    
    performance_results = []
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Performance test {i}: {len(prompt)} characters")
        
        # Measure response time
        start_time = time.time()
        result = client.generate_content(prompt)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if result.get("status") == "error":
            print(f"❌ Request failed: {result['message']}")
        else:
            content_length = len(result.get('article', ''))
            hrv_feedback = result.get('hrv_feedback', 0)
            
            performance_data = {
                "prompt_length": len(prompt),
                "response_time": response_time,
                "content_length": content_length,
                "hrv_feedback": hrv_feedback,
                "chars_per_second": content_length / response_time if response_time > 0 else 0
            }
            
            performance_results.append(performance_data)
            
            print(f"✅ Response time: {response_time:.3f}s")
            print(f"   Content length: {content_length} chars")
            print(f"   Chars/sec: {performance_data['chars_per_second']:.1f}")
            print(f"   HRV Feedback: {hrv_feedback:.3f}")
        
        print()
    
    # Performance summary
    if performance_results:
        avg_response_time = sum(r['response_time'] for r in performance_results) / len(performance_results)
        avg_chars_per_sec = sum(r['chars_per_second'] for r in performance_results) / len(performance_results)
        
        print("📊 Performance Summary:")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        print(f"Average Throughput: {avg_chars_per_sec:.1f} chars/sec")
        
        if avg_chars_per_sec > 100:
            print("✅ API performance is excellent")
        elif avg_chars_per_sec > 50:
            print("✅ API performance is good")
        else:
            print("⚠️  API performance could be improved")
    
    return performance_results


def authentication_example():
    """Demonstrate API authentication (placeholder)"""
    print("\n🔐 Authentication Example")
    print("=" * 50)
    
    print("Note: This is a placeholder for authentication demonstration.")
    print("In a production environment, you would implement:")
    print("- API key authentication")
    print("- OAuth 2.0 integration")
    print("- JWT token management")
    print("- Rate limiting")
    print()
    
    # Example of how authentication might be implemented
    class AuthenticatedAPIClient(ResonanceOSAPIClient):
        def __init__(self, base_url: str, api_key: str = None):
            super().__init__(base_url)
            if api_key:
                self.session.headers.update({
                    'Authorization': f'Bearer {api_key}'
                })
    
    # This would be used like:
    # client = AuthenticatedAPIClient("https://api.resonanceos.ai", "your-api-key")
    
    print("✅ Authentication example completed (placeholder)")


def webhook_integration_example():
    """Demonstrate webhook integration pattern"""
    print("\n🪝 Webhook Integration Example")
    print("=" * 50)
    
    print("This example shows how to set up webhook integration")
    print("for real-time content generation notifications.")
    print()
    
    # Webhook handler example
    class WebhookHandler:
        def __init__(self, webhook_url: str):
            self.webhook_url = webhook_url
            self.client = ResonanceOSAPIClient()
        
        def generate_and_notify(self, prompt: str, **kwargs):
            """Generate content and send webhook notification"""
            # Generate content
            result = self.client.generate_content(prompt, **kwargs)
            
            # Prepare webhook payload
            webhook_payload = {
                "event": "content_generated",
                "timestamp": time.time(),
                "prompt": prompt,
                "result": result,
                "metadata": kwargs
            }
            
            # Send webhook (placeholder implementation)
            print(f"📡 Sending webhook to {self.webhook_url}")
            print(f"   Event: {webhook_payload['event']}")
            print(f"   Prompt: {webhook_payload['prompt']}")
            print(f"   Status: {'Success' if result.get('status') != 'error' else 'Error'}")
            
            return result
    
    # Example usage
    webhook_handler = WebhookHandler("https://your-app.com/webhook/resonanceos")
    
    # Generate content with webhook notification
    print("Generating content with webhook notification...")
    result = webhook_handler.generate_and_notify(
        "Latest industry trends and insights",
        profile_name="professional_business",
        tenant="demo_tenant"
    )
    
    print("✅ Webhook integration example completed!")


def main():
    """Run all API integration examples"""
    print("🎯 ResonanceOS v6 - API Integration Examples")
    print("=" * 60)
    print("This example demonstrates API integration capabilities.")
    print("You'll learn how to:")
    print("- Make basic API calls")
    print("- Handle different profiles and tenants")
    print("- Process batch requests")
    print("- Implement error handling")
    print("- Monitor API performance")
    print("- Set up authentication")
    print("- Integrate with webhooks")
    print()
    
    try:
        # Run examples
        basic_api_example()
        advanced_api_example()
        batch_results = batch_api_requests()
        error_handling_example()
        performance_results = performance_monitoring_example()
        authentication_example()
        webhook_integration_example()
        
        print("\n🎉 All API integration examples completed!")
        print("\nKey Takeaways:")
        print("- ResonanceOS API is RESTful and easy to integrate")
        print("- Comprehensive error handling ensures reliability")
        print("- Performance monitoring helps optimize usage")
        print("- Authentication and webhooks enable enterprise integration")
        print("- Batch processing improves efficiency")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and API server")


if __name__ == "__main__":
    main()
