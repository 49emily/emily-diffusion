# 🎨 AI Image Generator Frontend

A beautiful React frontend for generating images using FLUX with LoRA support.

## Features

- ✨ Clean, modern UI with gradient backgrounds
- 🎯 Simple prompt input for image generation
- 🔧 Optional LoRA URL and scale controls
- 📱 Responsive design for mobile and desktop
- ⚡ Real-time loading states and error handling
- 🖼️ Image display with full-size viewing

## Setup

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Start the development server:**

   ```bash
   npm run dev
   ```

3. **Make sure your backend is running:**
   - The backend should be running on `http://localhost:8000`
   - See the `backend/` directory for setup instructions

## Usage

1. **Enter a prompt** describing the image you want to generate
2. **Optionally add a LoRA URL** if you have a custom style model
3. **Adjust the LoRA scale** (0.0 to 2.0) to control style strength
4. **Click "Generate Image"** and wait for the result
5. **View and download** your generated image

## API Integration

The frontend connects to the Flask backend at:

- **Endpoint:** `POST http://localhost:8000/generate-simple`
- **Payload:**
  ```json
  {
    "prompt": "your image description",
    "lora_url": "https://optional-lora-url.safetensors",
    "lora_scale": 0.8
  }
  ```

## Technologies Used

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **CSS3** - Modern styling with gradients and animations
- **Fetch API** - HTTP requests to backend

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Responsive Design

The interface is fully responsive and works great on:

- 📱 Mobile phones
- 📱 Tablets
- �� Desktop computers
