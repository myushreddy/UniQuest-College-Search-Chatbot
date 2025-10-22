import sys
import os
import pandas as pd
import requests
import time

def test_data_loading():
    """Test if the CSV data can be loaded properly"""
    print("🧪 Testing data loading...")
    try:
        data_path = os.path.join('data', 'engineering colleges in India.csv')
        df = pd.read_csv(data_path)
        print(f"✅ Successfully loaded {len(df)} colleges from CSV")
        
        # Check required columns
        required_cols = ['College Name', 'City', 'State', 'Average Fees', 'Rating']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"⚠️  Missing columns: {missing_cols}")
        else:
            print("✅ All required columns present")
        
        return True
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return False

def test_backend_server():
    """Test if the backend server is running and responding"""
    print("\n🧪 Testing backend server...")
    try:
        # Test if server is running
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
        
        # Test chat endpoint
        test_message = {"message": "Which college is the best?"}
        response = requests.post('http://localhost:5000/chat', 
                               json=test_message, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                print("✅ Chat endpoint working correctly")
                print(f"   Sample response length: {len(data['response'])} characters")
                return True
            else:
                print("❌ Chat endpoint response missing 'response' field")
                return False
        else:
            print(f"❌ Chat endpoint failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure to run 'python backend/chatbot.py' first")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_search_functionality():
    """Test different types of search queries"""
    print("\n🧪 Testing search functionality...")
    
    test_queries = [
        "cheap colleges in Mumbai",
        "best colleges for computer science",
        "government colleges",
        "colleges with hostel facilities",
        "Which college has the highest rating?"
    ]
    
    success_count = 0
    for query in test_queries:
        try:
            response = requests.post('http://localhost:5000/chat', 
                                   json={"message": query}, 
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and len(data['response']) > 50:
                    print(f"✅ Query '{query[:30]}...' - Success")
                    success_count += 1
                else:
                    print(f"⚠️  Query '{query[:30]}...' - Empty response")
            else:
                print(f"❌ Query '{query[:30]}...' - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Query '{query[:30]}...' - Error: {e}")
    
    print(f"\n📊 Search test results: {success_count}/{len(test_queries)} queries successful")
    return success_count == len(test_queries)

def main():
    print("🎓 UniQuest College Search Chatbot - System Test")
    print("=" * 50)
    
    # Test 1: Data loading
    data_ok = test_data_loading()
    
    if not data_ok:
        print("\n❌ Cannot proceed with other tests - data loading failed")
        return False
    
    # Test 2: Backend server
    print("\n⏳ Waiting 3 seconds for potential server startup...")
    time.sleep(3)
    
    server_ok = test_backend_server()
    
    if not server_ok:
        print("\n❌ Cannot test search functionality - server not responding")
        print("💡 Start the backend server first: python backend/chatbot.py")
        return False
    
    # Test 3: Search functionality
    search_ok = test_search_functionality()
    
    # Final results
    print("\n" + "=" * 50)
    print("📋 FINAL TEST RESULTS:")
    print(f"   Data Loading: {'✅ PASS' if data_ok else '❌ FAIL'}")
    print(f"   Backend Server: {'✅ PASS' if server_ok else '❌ FAIL'}")
    print(f"   Search Functionality: {'✅ PASS' if search_ok else '❌ FAIL'}")
    
    if data_ok and server_ok and search_ok:
        print("\n🎉 ALL TESTS PASSED! Your UniQuest chatbot is ready to use!")
        print("👉 Open frontend/index.html in your browser to start chatting")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
    
    return data_ok and server_ok and search_ok

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)