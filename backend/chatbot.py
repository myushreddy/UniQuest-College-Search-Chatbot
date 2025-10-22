import pandas as pd
import re
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

class CollegeChatbot:
    def __init__(self):
        self.colleges_df = None
        self.load_data()
        
    def load_data(self):
        """Load college data from CSV file"""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'engineering colleges in India.csv')
            self.colleges_df = pd.read_csv(data_path)
            print(f"Loaded {len(self.colleges_df)} colleges from database")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.colleges_df = pd.DataFrame()
    
    def extract_numbers(self, text):
        """Extract numbers from text"""
        numbers = re.findall(r'\d+(?:\.\d+)?', text.lower())
        return [float(num) for num in numbers]
    
    def extract_location(self, text):
        """Extract location mentions from text"""
        # Common cities and states
        locations = [
            'mumbai', 'delhi', 'bangalore', 'bengaluru', 'chennai', 'kolkata', 'hyderabad', 
            'pune', 'ahmedabad', 'surat', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'patna',
            'indore', 'thane', 'bhopal', 'visakhapatnam', 'vadodara', 'firozabad',
            'maharashtra', 'karnataka', 'tamil nadu', 'kerala', 'andhra pradesh', 'telangana',
            'gujarat', 'rajasthan', 'uttar pradesh', 'west bengal', 'bihar', 'odisha',
            'punjab', 'haryana', 'madhya pradesh', 'jharkhand', 'assam', 'uttarakhand'
        ]
        
        text_lower = text.lower()
        found_locations = []
        for location in locations:
            if location in text_lower:
                found_locations.append(location.title())
        return found_locations
    
    def search_colleges(self, query):
        """Main search function that processes natural language queries"""
        if self.colleges_df.empty:
            return "Sorry, I couldn't load the college database. Please try again later."
        
        query_lower = query.lower()
        results = self.colleges_df.copy()
        
        # Fee-based queries
        if any(word in query_lower for word in ['fee', 'fees', 'cost', 'cheap', 'expensive', 'budget', 'affordable']):
            numbers = self.extract_numbers(query)
            if numbers:
                max_fee = max(numbers) * 100000 if max(numbers) < 100 else max(numbers)  # Convert lakhs to rupees if needed
                results = results[results['Average Fees'] <= max_fee]
                if 'cheap' in query_lower or 'low' in query_lower or 'affordable' in query_lower:
                    results = results.nsmallest(10, 'Average Fees')
            else:
                # Default to cheapest colleges
                results = results.nsmallest(10, 'Average Fees')
        
        # Location-based queries
        locations = self.extract_location(query)
        if locations:
            location_filter = results['City'].str.contains('|'.join(locations), case=False, na=False) | \
                           results['State'].str.contains('|'.join(locations), case=False, na=False)
            results = results[location_filter]
        
        # Rating-based queries
        if any(word in query_lower for word in ['best', 'top', 'highest rated', 'rating', 'excellent']):
            results = results.dropna(subset=['Rating'])
            results = results.nlargest(10, 'Rating')
        
        # Course-based queries
        courses = ['computer science', 'cse', 'mechanical', 'electrical', 'civil', 'electronics', 'chemical', 'biotechnology']
        mentioned_courses = [course for course in courses if course in query_lower]
        if mentioned_courses:
            course_filter = results['Courses'].str.contains('|'.join(mentioned_courses), case=False, na=False)
            results = results[course_filter]
        
        # Facility-based queries
        facilities = ['hostel', 'gym', 'library', 'sports', 'cafeteria', 'wifi', 'medical', 'swimming pool']
        mentioned_facilities = [facility for facility in facilities if facility in query_lower]
        if mentioned_facilities:
            facility_filter = results['Facilities'].str.contains('|'.join(mentioned_facilities), case=False, na=False)
            results = results[facility_filter]
        
        # College type queries
        if 'government' in query_lower or 'public' in query_lower:
            results = results[results['College Type'] == 'Public/Government']
        elif 'private' in query_lower:
            results = results[results['College Type'] == 'Private']
        
        # Return top results
        if len(results) == 0:
            return "Sorry, I couldn't find any colleges matching your criteria. Try rephrasing your query."
        
        return self.format_results(results.head(5), query)
    
    def format_results(self, results, query):
        """Format search results into a readable response"""
        if len(results) == 0:
            return "No colleges found matching your criteria."
        
        response = f"🎓 Found {len(results)} college(s) for your query:\n\n"
        
        for idx, (_, college) in enumerate(results.iterrows(), 1):
            response += f"{idx}. **{college['College Name']}**\n"
            response += f"📍 Location: {college['City']}, {college['State']}\n"
            
            if pd.notna(college['Rating']):
                response += f"⭐ Rating: {college['Rating']}/5.0\n"
            
            if pd.notna(college['Average Fees']):
                fees_in_lakhs = college['Average Fees'] / 100000
                response += f"💰 Average Fees: ₹{fees_in_lakhs:.2f} lakhs\n"
            
            response += f"🏫 Type: {college['College Type']}\n"
            
            if pd.notna(college['Established Year']):
                response += f"📅 Established: {int(college['Established Year'])}\n"
            
            response += "\n"
        
        return response
    
    def get_predefined_response(self, query_type):
        """Handle predefined queries"""
        if self.colleges_df.empty:
            return "Sorry, I couldn't load the college database."
        
        responses = {
            'best_college': self.search_colleges("best rated college"),
            'top_colleges': self.search_colleges("top 5 colleges"),
            'low_fee': self.search_colleges("cheapest college low fees"),
            'cultural_activities': "🎭 For vibrant cultural activities, consider colleges like IIT Bombay, BITS Pilani, and NIT Trichy which are known for their active cultural festivals and student clubs.",
            'highest_rating': self.search_colleges("highest rating college"),
            'oldest_college': self.colleges_df.loc[self.colleges_df['Established Year'].idxmin(), 'College Name'] + f" is the oldest college, established in {int(self.colleges_df['Established Year'].min())}",
            'placement_rate': "💼 For high placement rates, consider IITs, NITs, and premier institutes like IIIT Hyderabad, BITS Pilani which consistently achieve 90%+ placement rates.",
            'hostel_facilities': self.search_colleges("best hostel facilities"),
            'international_exposure': "🌏 For international exposure, consider colleges with exchange programs like IIT Bombay, IIT Delhi, BITS Pilani, and VIT University.",
            'entrepreneurship_support': "🚀 For entrepreneurship support, IIT Madras, IIT Bombay, and BITS Pilani have excellent incubation centers and startup ecosystems.",
            'research_opportunities': "🔬 For research opportunities, IITs, IISc Bangalore, and premier NITs offer excellent research facilities and PhD programs.",
            'sports_facilities': self.search_colleges("sports facilities"),
            'student_clubs': "🎉 BITS Pilani, IIT Roorkee, and NIT Trichy are known for having the most active and diverse student clubs.",
            'safe_for_girls': "👩‍🎓 Women-friendly colleges include Lady Shri Ram College, Mount Carmel College, and most NITs which have dedicated women's hostels and safety measures.",
            'modern_infrastructure': "🏢 Colleges with modern infrastructure include newer IITs, Shiv Nadar University, and Amity University with smart classrooms and advanced labs.",
            'distance_learning': "🧑‍💻 For distance learning, IGNOU offers the most comprehensive programs, followed by universities like Amity and Manipal for online engineering courses."
        }
        
        return responses.get(query_type, "I'm not sure about that. Try asking about college fees, locations, ratings, or facilities!")

# Flask web application
app = Flask(__name__)
CORS(app)
chatbot = CollegeChatbot()

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>UniQuest College Chatbot API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .api-info { background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }
            code { background: #34495e; color: white; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 UniQuest College Chatbot API</h1>
            <div class="api-info">
                <h3>API Endpoints:</h3>
                <p><strong>POST</strong> <code>/chat</code> - Send a message to the chatbot</p>
                <p><strong>Example:</strong> <code>{"message": "Show me cheap colleges in Mumbai"}</code></p>
            </div>
            <p>This API serves the UniQuest College Search Chatbot. Use the frontend interface for a better user experience.</p>
        </div>
    </body>
    </html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check for predefined queries
        predefined_queries = {
            'which college is the best': 'best_college',
            'what are the top 5 colleges': 'top_colleges',
            'which college has less fee': 'low_fee',
            'which college has better cultural activities': 'cultural_activities',
            'which college has the highest rating': 'highest_rating',
            'which is the oldest college': 'oldest_college',
            'which college has the highest placement rate': 'placement_rate',
            'which college has the best hostel facilities': 'hostel_facilities',
            'which college offers good international exposure': 'international_exposure',
            'which college supports startups and entrepreneurship': 'entrepreneurship_support',
            'which college is best for research opportunities': 'research_opportunities',
            'which college has the best sports facilities': 'sports_facilities',
            'which college has the most active student clubs': 'student_clubs',
            'which is the safest college for girls': 'safe_for_girls',
            'which college has the most modern infrastructure': 'modern_infrastructure',
            'which college offers the best distance learning programs': 'distance_learning'
        }
        
        # Check if it's a predefined query
        message_lower = message.lower().strip('?')
        if message_lower in predefined_queries:
            response = chatbot.get_predefined_response(predefined_queries[message_lower])
        else:
            # Use intelligent search for custom queries
            response = chatbot.search_colleges(message)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    print("🎓 Starting UniQuest College Chatbot...")
    print("📊 Loading college database...")
    app.run(debug=True, host='0.0.0.0', port=5000)