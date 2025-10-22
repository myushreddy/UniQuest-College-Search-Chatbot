import pandas as pd
import re
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import numpy as np

class MultiDatasetCollegeChatbot:
    def __init__(self):
        self.df_main = None      # Main engineering colleges dataset (detailed info)
        self.df_nirf = None      # NIRF rankings dataset 
        self.df_courses = None   # Course-specific dataset
        self.load_data()
        
    def load_data(self):
        """Load all three college datasets"""
        try:
            base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            
            # Dataset 1: Main engineering colleges data (detailed info)
            main_path = os.path.join(base_path, 'engineering colleges in India.csv')
            if os.path.exists(main_path):
                self.df_main = pd.read_csv(main_path)
                # Clean up fee data
                self.df_main['Average Fees'] = pd.to_numeric(self.df_main['Average Fees'], errors='coerce')
                print(f"✅ Main dataset: Loaded {len(self.df_main)} colleges with detailed info")
            else:
                print("❌ Main dataset not found")
                
            # Dataset 2: NIRF Rankings
            nirf_path = os.path.join(base_path, 'NIRF Ranking for Engineering Colleges 2024.csv')
            if os.path.exists(nirf_path):
                self.df_nirf = pd.read_csv(nirf_path)
                print(f"✅ NIRF dataset: Loaded {len(self.df_nirf)} ranked colleges")
            else:
                print("❌ NIRF dataset not found")
                
            # Dataset 3: Course-specific data
            course_path = os.path.join(base_path, 'Engineering.csv')
            if os.path.exists(course_path):
                self.df_courses = pd.read_csv(course_path)
                print(f"✅ Course dataset: Loaded {len(self.df_courses)} course entries")
            else:
                print("❌ Course dataset not found")
                
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            
    def normalize_college_name(self, name):
        """Normalize college names for better matching across datasets"""
        if pd.isna(name):
            return ""
        name = str(name).lower()
        # Remove common prefixes/suffixes and standardize
        name = re.sub(r'\b(university|college|institute|technology|engineering)\b', '', name)
        name = re.sub(r'[^\w\s]', ' ', name)  # Remove punctuation
        name = ' '.join(name.split())  # Clean whitespace
        return name
    
    def find_college_across_datasets(self, college_name):
        """Find college information across all three datasets"""
        normalized_name = self.normalize_college_name(college_name)
        result = {}
        
        # Search in main dataset
        if self.df_main is not None:
            main_mask = self.df_main['College Name'].apply(
                lambda x: normalized_name in self.normalize_college_name(x) if pd.notna(x) else False
            )
            if main_mask.any():
                result['main'] = self.df_main[main_mask].iloc[0]
        
        # Search in NIRF dataset
        if self.df_nirf is not None:
            nirf_mask = self.df_nirf['Name'].apply(
                lambda x: normalized_name in self.normalize_college_name(x) if pd.notna(x) else False
            )
            if nirf_mask.any():
                result['nirf'] = self.df_nirf[nirf_mask].iloc[0]
        
        # Search in course dataset
        if self.df_courses is not None:
            course_mask = self.df_courses['college name'].apply(
                lambda x: normalized_name in self.normalize_college_name(x) if pd.notna(x) else False
            )
            if course_mask.any():
                result['courses'] = self.df_courses[course_mask]
                
        return result
    
    def extract_numbers(self, text):
        """Extract numbers from text"""
        numbers = re.findall(r'\d+(?:\.\d+)?', text.lower())
        return [float(num) for num in numbers]
    
    def extract_location(self, text):
        """Extract location mentions from text"""
        locations = [
            'mumbai', 'delhi', 'bangalore', 'bengaluru', 'chennai', 'kolkata', 'hyderabad', 
            'pune', 'ahmedabad', 'surat', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'patna',
            'indore', 'thane', 'bhopal', 'visakhapatnam', 'vadodara', 'firozabad', 'coimbatore',
            'madurai', 'kochi', 'thiruvananthapuram', 'bhubaneswar', 'guwahati', 'chandigarh',
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
    
    def search_by_ranking(self, query):
        """Search colleges by NIRF ranking"""
        if self.df_nirf is None:
            return None
            
        query_lower = query.lower()
        
        # Extract rank numbers or ranges
        numbers = self.extract_numbers(query)
        
        if 'top' in query_lower:
            if numbers:
                top_n = int(min(numbers))  # Get the smallest number as top N
                return self.df_nirf.head(top_n)
            else:
                return self.df_nirf.head(10)  # Default top 10
        elif numbers:
            # Specific rank range
            if len(numbers) >= 2:
                start_rank = int(min(numbers))
                end_rank = int(max(numbers))
                return self.df_nirf[(self.df_nirf['Rank'] >= start_rank) & (self.df_nirf['Rank'] <= end_rank)]
            else:
                # Single rank or top N
                rank = int(numbers[0])
                if rank <= len(self.df_nirf):
                    return self.df_nirf[self.df_nirf['Rank'] == rank]
        
        return None
    
    def search_by_course(self, query):
        """Search colleges by specific courses"""
        if self.df_courses is None:
            return None
            
        query_lower = query.lower()
        
        # Course mappings
        course_mappings = {
            'computer science': ['computer science', 'cse', 'computer engineering'],
            'mechanical': ['mechanical engineering', 'mechanical'],
            'electrical': ['electrical', 'electrical and electronics'],
            'electronics': ['electronics', 'ece', 'electronics and communication'],
            'civil': ['civil engineering', 'civil'],
            'chemical': ['chemical engineering', 'chemical'],
            'biotechnology': ['biotechnology', 'biotech'],
            'information technology': ['information technology', 'it'],
            'aerospace': ['aerospace', 'aeronautical'],
            'automobile': ['automobile', 'automotive']
        }
        
        mentioned_courses = []
        for course_key, course_variants in course_mappings.items():
            if any(variant in query_lower for variant in course_variants):
                mentioned_courses.extend(course_variants)
        
        if mentioned_courses:
            course_filter = self.df_courses['Course'].str.contains('|'.join(mentioned_courses), case=False, na=False)
            return self.df_courses[course_filter]
        
        return None
    
    def search_colleges(self, query):
        """Main search function that intelligently uses all three datasets"""
        query_lower = query.lower()
        results = []
        
        # 1. Check for ranking-based queries first
        if any(word in query_lower for word in ['rank', 'top', 'nirf', 'best ranked']):
            ranking_results = self.search_by_ranking(query)
            if ranking_results is not None and not ranking_results.empty:
                return self.format_nirf_results(ranking_results, query)
        
        # 2. Check for course-specific queries
        course_results = self.search_by_course(query)
        if course_results is not None and not course_results.empty:
            # Get unique colleges from course results
            unique_colleges = course_results['college name'].unique()[:5]
            return self.format_course_results(unique_colleges, course_results, query)
        
        # 3. Use main dataset for detailed searches (fees, facilities, etc.)
        if self.df_main is not None and not self.df_main.empty:
            return self.search_main_dataset(query)
        
        return "Sorry, I couldn't find relevant information. Please try rephrasing your query."
    
    def search_main_dataset(self, query):
        """Search in the main dataset with detailed college information"""
        query_lower = query.lower()
        results = self.df_main.copy()
        
        # Fee-based queries
        if any(word in query_lower for word in ['fee', 'fees', 'cost', 'cheap', 'expensive', 'budget', 'affordable']):
            numbers = self.extract_numbers(query)
            if numbers:
                max_fee = max(numbers) * 100000 if max(numbers) < 100 else max(numbers)
                results = results[results['Average Fees'] <= max_fee]
                if 'cheap' in query_lower or 'low' in query_lower or 'affordable' in query_lower:
                    results = results.nsmallest(10, 'Average Fees')
            else:
                results = results.nsmallest(10, 'Average Fees')
        
        # Location-based queries
        locations = self.extract_location(query)
        if locations:
            location_filter = results['City'].str.contains('|'.join(locations), case=False, na=False) | \
                           results['State'].str.contains('|'.join(locations), case=False, na=False)
            results = results[location_filter]
        
        # Rating-based queries
        if any(word in query_lower for word in ['best', 'highest rated', 'rating', 'excellent']):
            results = results.dropna(subset=['Rating'])
            results = results.nlargest(10, 'Rating')
        
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
        
        if len(results) == 0:
            return "Sorry, I couldn't find any colleges matching your criteria in the detailed database."
        
        return self.format_main_results(results.head(5), query)
    
    def format_main_results(self, results, query):
        """Format results from main dataset"""
        if len(results) == 0:
            return "No colleges found matching your criteria."
        
        response = f"🎓 Found {len(results)} college(s) in our detailed database:\n\n"
        
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
            
            # Add NIRF ranking if available
            college_info = self.find_college_across_datasets(college['College Name'])
            if 'nirf' in college_info:
                response += f"🏆 NIRF Rank: {int(college_info['nirf']['Rank'])}\n"
            
            response += "\n"
        
        return response
    
    def format_nirf_results(self, results, query):
        """Format NIRF ranking results"""
        response = f"🏆 NIRF Ranked Engineering Colleges ({len(results)} results):\n\n"
        
        for idx, (_, college) in enumerate(results.iterrows(), 1):
            response += f"{idx}. **{college['Name']}** (Rank: {int(college['Rank'])})\n"
            response += f"📍 Location: {college['City']}, {college['State']}\n"
            
            # Try to get additional info from main dataset
            college_info = self.find_college_across_datasets(college['Name'])
            if 'main' in college_info:
                main_info = college_info['main']
                if pd.notna(main_info['Rating']):
                    response += f"⭐ Rating: {main_info['Rating']}/5.0\n"
                if pd.notna(main_info['Average Fees']):
                    fees_in_lakhs = main_info['Average Fees'] / 100000
                    response += f"💰 Average Fees: ₹{fees_in_lakhs:.2f} lakhs\n"
                response += f"🏫 Type: {main_info['College Type']}\n"
            
            response += "\n"
        
        return response
    
    def format_course_results(self, unique_colleges, course_data, query):
        """Format course-specific results"""
        response = f"🎯 Engineering Colleges offering relevant courses ({len(unique_colleges)} colleges):\n\n"
        
        for idx, college_name in enumerate(unique_colleges, 1):
            response += f"{idx}. **{college_name}**\n"
            
            # Get courses offered at this college
            college_courses = course_data[course_data['college name'] == college_name]['Course'].unique()
            if len(college_courses) > 0:
                response += f"📚 Courses: {', '.join(college_courses[:3])}"
                if len(college_courses) > 3:
                    response += f" (+{len(college_courses)-3} more)"
                response += "\n"
            
            # Get additional info from other datasets
            college_info = self.find_college_across_datasets(college_name)
            
            if 'main' in college_info:
                main_info = college_info['main']
                response += f"📍 Location: {main_info['City']}, {main_info['State']}\n"
                if pd.notna(main_info['Average Fees']):
                    fees_in_lakhs = main_info['Average Fees'] / 100000
                    response += f"💰 Average Fees: ₹{fees_in_lakhs:.2f} lakhs\n"
            elif 'nirf' in college_info:
                nirf_info = college_info['nirf']
                response += f"📍 Location: {nirf_info['City']}, {nirf_info['State']}\n"
                response += f"🏆 NIRF Rank: {int(nirf_info['Rank'])}\n"
            
            response += "\n"
        
        return response

# Flask application setup
app = Flask(__name__)
CORS(app)
chatbot = MultiDatasetCollegeChatbot()

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>UniQuest Multi-Dataset College Chatbot API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .dataset-info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .api-info { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
            code { background: #34495e; color: white; padding: 2px 5px; border-radius: 3px; }
            .feature { margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 UniQuest Multi-Dataset College Chatbot API</h1>
            
            <div class="dataset-info">
                <h3>📊 Integrated Datasets:</h3>
                <div class="feature">1. <strong>Detailed College Info</strong> - Fees, facilities, ratings, courses</div>
                <div class="feature">2. <strong>NIRF Rankings 2024</strong> - Official government rankings (Top 200+)</div>
                <div class="feature">3. <strong>Course-Specific Data</strong> - Individual program details and accreditations</div>
            </div>
            
            <div class="api-info">
                <h3>🚀 Enhanced Capabilities:</h3>
                <div class="feature">• <strong>Smart Dataset Selection</strong> - Automatically chooses the best data source</div>
                <div class="feature">• <strong>Cross-Dataset Integration</strong> - Combines information from multiple sources</div>
                <div class="feature">• <strong>NIRF Ranking Queries</strong> - "Show top 10 colleges" or "colleges ranked 20-30"</div>
                <div class="feature">• <strong>Course-Specific Search</strong> - "Computer Science colleges" or "Mechanical engineering"</div>
                <div class="feature">• <strong>Detailed Filters</strong> - Fees, location, facilities, ratings</div>
            </div>
            
            <div class="api-info">
                <h3>📡 API Usage:</h3>
                <p><strong>POST</strong> <code>/chat</code> - Send queries to the enhanced chatbot</p>
                <p><strong>Examples:</strong></p>
                <code>{"message": "Top 10 NIRF ranked colleges"}</code><br><br>
                <code>{"message": "Computer science colleges under 5 lakhs"}</code><br><br>
                <code>{"message": "Best colleges in Maharashtra with good facilities"}</code>
            </div>
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
        
        response = chatbot.search_colleges(message)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    print("🎓 Starting UniQuest Multi-Dataset College Chatbot...")
    print("📊 Loading multiple college databases...")
    app.run(debug=True, host='0.0.0.0', port=5000)