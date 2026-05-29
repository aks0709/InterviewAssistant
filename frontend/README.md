# Interview Assistant Frontend

Professional React frontend for AI-powered JD-Resume similarity analysis.

## Features

- 🎯 **Professional UI** - Clean, modern interface with Tailwind CSS
- 📁 **File Upload** - Drag & drop support for PDF, DOCX, and TXT files
- 🤖 **AI Analysis** - Real-time similarity scoring with detailed insights
- 🎨 **Color Coding** - Visual feedback (Red < 80%, Green ≥ 80%)
- 📊 **Detailed Results** - Key matches, missing skills, and recommendations
- 📱 **Responsive** - Works on desktop and mobile devices

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **React Dropzone** - File upload with drag & drop
- **PDF.js** - PDF text extraction
- **Mammoth.js** - DOCX text extraction
- **Heroicons** - Beautiful SVG icons

## Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

## Installation & Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start development server
```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

## Usage Instructions

### 1. Upload Files
- **Job Description**: Upload PDF, DOCX, or TXT file containing the job requirements
- **Resume**: Upload candidate's resume in PDF, DOCX, or TXT format
- Use drag & drop or click to browse files

### 2. Analyze Similarity
- Click "Evaluate Similarity" button
- Wait for AI analysis (typically 5-10 seconds)

### 3. View Results
- **Similarity Score**: Percentage match with color coding
  - 🔴 Red: < 80% (Needs Improvement)
  - 🟢 Green: ≥ 80% (Strong Match)
- **Key Matches**: Expandable list of matching skills/requirements
- **Missing Skills**: Skills mentioned in JD but not found in resume
- **Recommendations**: AI-generated advice based on analysis

## File Support

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Portable Document Format |
| Word | `.docx` | Microsoft Word Document |
| Text | `.txt` | Plain text file |

## API Integration

The frontend connects to the backend API:
- **Endpoint**: `POST /agent1/evaluate`
- **Base URL**: `http://localhost:8000`
- **Request**: `{ jd_text: string, resume_text: string }`
- **Response**: Similarity analysis with scores and recommendations

## Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── FileUpload.jsx    # File upload component
│   │   └── Results.jsx       # Results display component
│   ├── utils/
│   │   └── fileParser.js     # File parsing utilities
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # React entry point
│   └── index.css            # Tailwind CSS imports
├── public/                  # Static assets
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind configuration
└── vite.config.js         # Vite configuration
```

## Troubleshooting

### Common Issues

1. **CORS Error**
   - Ensure backend is running with proper CORS configuration
   - Check backend URL in `App.jsx` (line 7)

2. **File Upload Issues**
   - Verify file format is supported (PDF, DOCX, TXT)
   - Check file size (large files may take longer to process)

3. **Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Update dependencies: `npm update`

### Development Tips

- Use browser dev tools to monitor network requests
- Check console for detailed error messages
- Ensure backend API is accessible at `http://localhost:8000`

## Next Steps

This frontend is specifically built for **Agent 1 (Similarity Analysis)**. Additional pages for Agent 2 (Scheduling) and Agent 3 (Questions) will be built separately upon confirmation.