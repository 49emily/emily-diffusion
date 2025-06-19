# 🎨 AI Image Generator Setup Guide

Complete setup instructions for the Flask backend + React frontend AI image generator.

## 📁 Project Structure

```
emily-sd/
├── backend/                 # Flask server with fal inference
│   ├── app.py              # Main Flask application
│   ├── upload_lora.py      # LoRA upload script
│   ├── test_fal_api.py     # API testing script
│   ├── requirements.txt    # Python dependencies
│   ├── env.example         # Environment variables template
│   └── README.md           # Backend documentation
└── frontend/               # React frontend
    ├── src/
    │   ├── App.jsx         # Main React component
    │   ├── App.css         # Styling
    │   └── index.css       # Global styles
    ├── package.json        # Node dependencies
    └── README.md           # Frontend documentation
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file with your FAL API key
cp env.example .env
# Edit .env and add your actual FAL_KEY

# Start the Flask server
python app.py
```

The backend will start on `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:5173`

## 🔑 Environment Setup

### Backend (.env file)

```
FAL_KEY=your_actual_fal_api_key_here
```

Get your FAL API key from [fal.ai](https://fal.ai)

## 🎯 Usage

1. **Open your browser** to `http://localhost:5173`
2. **Enter a prompt** describing the image you want to generate
3. **Optionally add a LoRA URL** for custom styles
4. **Click "Generate Image"** and wait for the result
5. **View and download** your generated image

## 🛠 Development

### Backend Development

- `python app.py` - Start Flask server
- `python test_fal_api.py` - Test fal API methods
- `python upload_lora.py <file>` - Upload LoRA files

### Frontend Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 📡 API Endpoints

### Backend (Flask)

- `GET /` - Health check
- `POST /upload-lora` - Upload LoRA files
- `POST /generate-simple` - Generate images (simplified)
- `POST /generate` - Generate images (full control)

### Example API Call

```bash
curl -X POST http://localhost:8000/generate-simple \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape painting",
    "lora_url": "https://optional-lora-url.safetensors",
    "lora_scale": 0.8
  }'
```

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**

   - Make sure you've installed dependencies: `pip install -r requirements.txt`

2. **"FAL_KEY not set" warning**

   - Create `.env` file in backend directory with your API key

3. **CORS errors**

   - Make sure both backend (port 8000) and frontend (port 5173) are running

4. **"fal_client has no attribute 'subscribe'" error**
   - Update to latest fal-client: `pip install fal-client==0.7.0`

### Port Configuration

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

If you need to change ports, update:

- Backend: `app.py` line with `app.run(port=8000)`
- Frontend: `App.jsx` fetch URL

## 🎨 Features

### Frontend

- ✨ Modern gradient UI design
- 🎯 Simple prompt input
- 🔧 LoRA URL and scale controls
- 📱 Responsive mobile design
- ⚡ Real-time loading states
- 🖼️ Image display with download

### Backend

- 🚀 Flask REST API
- 🎨 FLUX image generation
- 🔧 LoRA support
- 📁 File upload handling
- ⚡ CORS enabled
- 🛡️ Error handling

## 📚 Technologies Used

- **Backend**: Python, Flask, fal-client
- **Frontend**: React 19, Vite, CSS3
- **AI**: FLUX model with LoRA support
- **Deployment**: Local development setup

## 🎉 You're Ready!

Your AI image generator is now set up and ready to create amazing images! 🎨✨
