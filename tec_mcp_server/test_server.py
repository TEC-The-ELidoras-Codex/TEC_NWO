#!/usr/bin/env python3
"""
TEC MCP Server Test Suite
Basic functionality tests for The Asimov Engine
"""

import requests
import json
import time
from datetime import datetime

class AsimovEngineTests:
    """Test suite for the Asimov Engine MCP Server"""
    
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log(self, message, level='INFO'):
        """Log test messages"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {level}: {message}")
    
    def test_health_check(self):
        """Test the health check endpoint"""
        self.log("Testing health check endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'status' in data and 'version' in data:
                    self.log(f"✅ Health check passed - Status: {data['status']}, Version: {data['version']}")
                    self.passed_tests += 1
                    return True
                else:
                    self.log("❌ Health check failed - Invalid response format")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"❌ Health check failed - Status code: {response.status_code}")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"❌ Health check failed - Error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_axiom_validation(self):
        """Test axiom validation endpoint"""
        self.log("Testing axiom validation...")
        try:
            test_content = "This is a story about a flawed hero who struggles to do the right thing, learning that true strength comes from admitting mistakes and protecting the innocent."
            
            payload = {
                'content': test_content,
                'type': 'story'
            }
            
            response = requests.post(
                f"{self.base_url}/axioms/validate", 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'valid' in data and 'axiom_scores' in data:
                    validity = data['valid']
                    avg_score = data.get('average_score', 0)
                    self.log(f"✅ Axiom validation passed - Valid: {validity}, Avg Score: {avg_score:.2f}")
                    self.passed_tests += 1
                    return True
                else:
                    self.log("❌ Axiom validation failed - Invalid response format")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"❌ Axiom validation failed - Status code: {response.status_code}")
                self.failed_tests += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Axiom validation failed - Error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_memory_query(self):
        """Test memory query endpoint"""
        self.log("Testing memory query...")
        try:
            payload = {
                'query': 'hero journey',
                'context_type': 'general'
            }
            
            response = requests.post(
                f"{self.base_url}/memory/query",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and 'query' in data:
                    results_count = len(data['results'])
                    self.log(f"✅ Memory query passed - Found {results_count} results")
                    self.passed_tests += 1
                    return True
                else:
                    self.log("❌ Memory query failed - Invalid response format")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"❌ Memory query failed - Status code: {response.status_code}")
                self.failed_tests += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Memory query failed - Error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_tool_execution(self):
        """Test tool execution endpoint"""
        self.log("Testing tool execution...")
        try:
            payload = {
                'tool_name': 'narrative_generator',
                'parameters': {
                    'prompt': 'A hero faces a moral dilemma',
                    'style': 'balanced'
                }
            }
            
            response = requests.post(
                f"{self.base_url}/tools/execute",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'validated' in data:
                    validated = data['validated']
                    self.log(f"✅ Tool execution passed - Validated: {validated}")
                    self.passed_tests += 1
                    return True
                else:
                    self.log("❌ Tool execution failed - Invalid response format")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"❌ Tool execution failed - Status code: {response.status_code}")
                self.failed_tests += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Tool execution failed - Error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_hybrid_synthesis(self):
        """Test the core hybrid synthesis endpoint"""
        self.log("Testing hybrid synthesis (Ellison-Asimov)...")
        try:
            payload = {
                'creative_input': 'I have this idea about a world where the good guys aren\'t always good and the bad guys have reasons for what they do. It\'s all grey areas and moral complexity.',
                'context': {
                    'setting': 'fantasy world',
                    'tone': 'mature'
                }
            }
            
            response = requests.post(
                f"{self.base_url}/synthesis/ellison-asimov",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'structured_output' in data and 'hybrid_synthesis' in data:
                    synthesis_flag = data['hybrid_synthesis']
                    self.log(f"✅ Hybrid synthesis passed - Synthesis: {synthesis_flag}")
                    self.passed_tests += 1
                    return True
                else:
                    self.log("❌ Hybrid synthesis failed - Invalid response format")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"❌ Hybrid synthesis failed - Status code: {response.status_code}")
                self.failed_tests += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Hybrid synthesis failed - Error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def run_all_tests(self):
        """Run all tests and report results"""
        self.log("🏛️  Starting TEC MCP Server Tests - The Asimov Engine")
        self.log("=" * 60)
        
        # Wait a moment for server to be ready
        self.log("Waiting for server to be ready...")
        time.sleep(2)
        
        # Run all tests
        tests = [
            self.test_health_check,
            self.test_axiom_validation,
            self.test_memory_query,
            self.test_tool_execution,
            self.test_hybrid_synthesis
        ]
        
        for test in tests:
            test()
            time.sleep(1)  # Brief pause between tests
        
        # Report results
        self.log("=" * 60)
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.log(f"Test Results: {self.passed_tests}/{total_tests} passed ({pass_rate:.1f}%)")
        
        if self.failed_tests == 0:
            self.log("🎉 All tests passed! The Asimov Engine is operational.")
        else:
            self.log(f"⚠️  {self.failed_tests} test(s) failed. Check server configuration.")
        
        return self.failed_tests == 0

def main():
    """Main test runner"""
    import sys
    
    # Allow custom server URL
    server_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    
    # Run tests
    test_suite = AsimovEngineTests(server_url)
    success = test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
