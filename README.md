# 🎓 UniQuest College Search Chatbot

An intelligent AI-powered chatbot that helps students find the perfect engineering college in India based on their preferences and requirements.

## ✨ Features

### 🔍 **Intelligent Search Capabilities**
- **Budget-based Search**: Find colleges within your fee range
- **Location-based Search**: Discover colleges in specific cities or states  
- **Rating-based Search**: Get top-rated institutions
- **Course-specific Search**: Find colleges offering specific engineering branches
- **Facility-based Search**: Filter by hostels, gym, library, sports facilities
- **College Type**: Search for government or private institutions

### 🤖 **Natural Language Processing**
- Ask questions in plain English like "Show me affordable government colleges in Karnataka for computer science"
- No need to learn specific commands or syntax
- Understands context and multiple search criteria

### 📊 **Comprehensive Database**
- **5,400+ Engineering Colleges** across India
- Real data including fees, ratings, facilities, courses, and locations
- Regular updates with latest information

### 🎯 **Smart Features**
- Quick action buttons for common queries
- Real-time search results
- Mobile-responsive design
- Beautiful, modern interface

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Web browser (Chrome, Firefox, Safari, etc.)

### 1. Clone the Repository
```bash
git clone https://github.com/myushreddy/UniQuest-College-Search-Chatbot.git
cd UniQuest-College-Search-Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server
```bash
python backend/chatbot.py
```
The server will start at `http://localhost:5000`

### 4. Open the Frontend
Open `frontend/index.html` in your web browser or use a local server:
```bash
# Option 1: Direct file opening
# Simply double-click frontend/index.html

# Option 2: Using Python's built-in server (recommended)
cd frontend
python -m http.server 8080
# Then open http://localhost:8080 in your browser
```

## 📁 Project Structure

```
UniQuest-College-Search-Chatbot/
├── 📂 data/                          # College databases
│   ├── engineering colleges in India.csv
│   ├── Engineering.csv
│   └── NIRF Ranking for Engineering Colleges 2024.csv
├── 📂 backend/                       # Python backend
│   └── chatbot.py                   # Main chatbot logic & Flask API
├── 📂 frontend/                      # Web interface
│   └── index.html                   # Main HTML file
├── 📂 assets/                        # Static assets
│   ├── 📂 css/
│   │   └── style.css                # Styling
│   └── 📂 js/
│       └── script.js                # Frontend JavaScript
├── 📂 chatbot/CRR/                   # Legacy files (for reference)
├── requirements.txt                  # Python dependencies
└── README.md                        # This file
```

## 💬 How to Use

### Example Questions You Can Ask:

#### 🏷️ **Fee-based Queries**
- "Show me colleges under 5 lakhs"
- "What are the cheapest engineering colleges?"
- "Affordable colleges in Maharashtra"

#### 📍 **Location-based Queries**  
- "Best colleges in Mumbai"
- "Engineering colleges in Karnataka"
- "Top colleges in South India"

#### ⭐ **Rating & Quality Queries**
- "Highest rated colleges"
- "Which college is the best?"
- "Top 5 engineering colleges"

#### 🏠 **Facility-based Queries**
- "Colleges with hostels and gym"
- "Which colleges have good sports facilities?"
- "Colleges with swimming pool"

#### 📚 **Course-specific Queries**
- "Best colleges for computer science"
- "Mechanical engineering colleges in Delhi"
- "Electronics colleges with good placement"

#### 🏛️ **Institution Type**
- "Government engineering colleges"
- "Private colleges under 10 lakhs"
- "NIT colleges in India"

### Quick Action Buttons
The interface also provides quick buttons for common queries:
- **Best College**
- **Top 5 Colleges** 
- **Cheapest Colleges**
- **Highest Rated**
- **Mumbai Colleges**
- **CS Colleges**

## 🔧 Technical Details

### Backend (Python Flask)
- **Framework**: Flask with CORS support
- **Data Processing**: Pandas for CSV parsing and filtering
- **Search Algorithm**: Natural language processing with regex patterns
- **API Endpoints**: RESTful API for chat functionality

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Gradient backgrounds, smooth animations
- **Real-time Chat**: Asynchronous communication with backend
- **Interactive Elements**: Typing indicators, hover effects

### Database
- **Format**: CSV files with comprehensive college information
- **Fields**: Name, Location, Fees, Rating, Facilities, Courses, Type, etc.
- **Size**: 5,400+ engineering colleges across India

## 🎯 Use Cases

### For Students:
- **College Research**: Compare colleges based on multiple criteria
- **Budget Planning**: Find colleges within fee range
- **Location Preference**: Discover options in preferred cities/states
- **Course Selection**: Find colleges with specific engineering branches

### For Parents:
- **Cost Analysis**: Compare fee structures across institutions
- **Safety & Facilities**: Check hostel and campus facilities
- **Reputation Check**: Verify college ratings and rankings

### For Counselors:
- **Quick References**: Instant access to college database
- **Student Guidance**: Help students make informed decisions
- **Comparative Analysis**: Easy comparison of multiple institutions

## 🛠️ Development

### Adding New Features
1. **Backend**: Modify `backend/chatbot.py` to add new search logic
2. **Frontend**: Update `assets/js/script.js` for UI changes
3. **Styling**: Edit `assets/css/style.css` for design updates

### Data Updates
Replace or update CSV files in the `data/` directory. The system automatically loads the latest data on restart.

### API Endpoints

#### POST `/chat`
Send a message to the chatbot
```json
{
  "message": "Show me cheap colleges in Mumbai"
}
```

**Response:**
```json
{
  "response": "🎓 Found 3 college(s) for your query:..."
}
```

## 🐛 Troubleshooting

### Common Issues:

#### "Backend server not responding"
- Ensure Python backend is running: `python backend/chatbot.py`
- Check if port 5000 is available
- Verify dependencies are installed: `pip install -r requirements.txt`

#### "No colleges found"
- Check if CSV files are in the `data/` directory
- Verify CSV file format matches expected structure
- Try rephrasing your query

#### "Frontend not loading properly"  
- Use a local server instead of opening HTML directly
- Check browser console for JavaScript errors
- Ensure all asset files (CSS, JS) are in correct locations

### Performance Tips:
- For faster searches, use specific criteria
- Backend caches data after first load
- Large result sets are automatically limited to top 5 matches

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Areas for Contribution:
- 🔍 Enhanced search algorithms
- 📊 Additional data sources
- 🎨 UI/UX improvements  
- 📱 Mobile app development
- 🧪 Test coverage
- 📚 Documentation improvements

## 📈 Future Enhancements

### Planned Features:
- **🔮 ML-based Recommendations**: Personalized college suggestions
- **📊 Advanced Analytics**: Placement statistics, alumni data
- **💬 Multi-language Support**: Hindi, regional languages
- **📱 Mobile App**: Native iOS and Android applications
- **🎯 Admission Guidance**: Application deadlines, entrance exam info
- **📈 Trend Analysis**: College ranking trends over time

### Data Expansions:
- **🎓 More Course Types**: MBA, Medical, Arts, Commerce colleges
- **🌍 International Colleges**: Study abroad options
- **📋 Scholarship Information**: Financial aid opportunities
- **🏆 Alumni Success Stories**: Graduate achievements and career paths

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

### Need Help?
- **📧 Email**: [your-email@example.com]
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/myushreddy/UniQuest-College-Search-Chatbot/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/myushreddy/UniQuest-College-Search-Chatbot/discussions)

### Documentation:
- **🚀 Quick Start Guide**: See above
- **🔧 API Documentation**: Check `/chat` endpoint details
- **💻 Development Guide**: Contribution guidelines above

## 🏆 Acknowledgments

- **Data Sources**: Engineering college information compiled from various educational databases
- **Design Inspiration**: Modern chat interfaces and educational platforms
- **Technology Stack**: Flask, Pandas, HTML5, CSS3, JavaScript ES6
- **Community**: Thanks to all contributors and users providing feedback

## 📊 Stats

- **🎓 Colleges Covered**: 5,400+
- **🌍 States Covered**: All Indian states and territories  
- **💬 Query Types Supported**: 15+ categories
- **⚡ Response Time**: < 2 seconds average
- **📱 Device Support**: Desktop, tablet, mobile

---

**Made with ❤️ for students seeking their perfect college**

*UniQuest - Where your educational journey begins!*