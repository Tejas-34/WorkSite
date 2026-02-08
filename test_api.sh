#!/bin/bash

# WorkSite Backend API Test Script
# This script tests all major API endpoints

BASE_URL="http://localhost:8000/api"

echo "🧪 Testing WorkSite Backend API Endpoints"
echo "=========================================="
echo ""

# Test 1: Register a Worker
echo "1️⃣  Testing User Registration (Worker)..."
curl -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "worker1@example.com",
    "password": "password123",
    "password2": "password123",
    "full_name": "John Worker",
    "role": "worker",
    "city": "Mumbai"
  }' \
  -b cookies.txt -c cookies.txt
echo -e "\n"

# Test 2: Register an Employer
echo "2️⃣  Testing User Registration (Employer)..."
curl -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "employer1@example.com",
    "password": "password123",
    "password2": "password123",
    "full_name": "Jane Employer",
    "role": "employer",
    "city": "Mumbai"
  }' \
  -b cookies2.txt -c cookies2.txt
echo -e "\n"

# Test 3: Login as Employer
echo "3️⃣  Testing Login (Employer)..."
curl -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "employer1@example.com",
    "password": "password123"
  }' \
  -b cookies2.txt -c cookies2.txt
echo -e "\n"

# Test 4: Check Auth Status
echo "4️⃣  Testing Auth Status..."
curl -X GET $BASE_URL/auth/status \
  -b cookies2.txt -c cookies2.txt
echo -e "\n"

# Test 5: Create a Job
echo "5️⃣  Testing Job Creation (Employer)..."
curl -X POST $BASE_URL/jobs/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $(grep csrftoken cookies2.txt | cut -f7)" \
  -d '{
    "title": "Construction Worker Needed",
    "description": "Need experienced workers for building construction",
    "daily_wage": 800.00,
    "required_workers": 3
  }' \
  -b cookies2.txt -c cookies2.txt
echo -e "\n"

# Test 6: List Jobs
echo "6️⃣  Testing Job Listing..."
curl -X GET $BASE_URL/jobs/ \
  -b cookies2.txt
echo -e "\n"

# Test 7: Login as Worker
echo "7️⃣  Testing Login (Worker)..."
curl -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "worker1@example.com",
    "password": "password123"
  }' \
  -b cookies.txt -c cookies.txt
echo -e "\n"

# Test 8: Apply for Job
echo "8️⃣  Testing Job Application (Worker)..."
curl -X POST $BASE_URL/jobs/1/apply/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $(grep csrftoken cookies.txt | cut -f7)" \
  -b cookies.txt -c cookies.txt
echo -e "\n"

# Test 9: View My Applications
echo "9️⃣  Testing View My Applications..."
curl -X GET $BASE_URL/applications/my \
  -b cookies.txt
echo -e "\n"

# Test 10: View Job Applications (Employer)
echo "🔟 Testing View Job Applications (Employer)..."
curl -X GET $BASE_URL/jobs/1/applications/ \
  -b cookies2.txt
echo -e "\n"

# Test 11: Accept Application
echo "1️⃣1️⃣  Testing Accept Application (Employer)..."
curl -X PUT $BASE_URL/applications/status \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $(grep csrftoken cookies2.txt | cut -f7)" \
  -d '{
    "application_id": 1,
    "status": "accepted"
  }' \
  -b cookies2.txt -c cookies2.txt
echo -e "\n"

# Test 12: Google OAuth Initiation URL
echo "1️⃣2️⃣  Testing Google OAuth URL Generation..."
curl -X GET $BASE_URL/auth/google
echo -e "\n"

echo "✅ Tests Complete!"
echo ""
echo "📝 Note: Some tests may fail due to CSRF or authentication issues."
echo "For full testing, use the Swagger UI at http://localhost:8000/api/docs/"
echo ""

# Cleanup
rm -f cookies.txt cookies2.txt
