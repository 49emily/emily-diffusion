# Fal Inference Flask Server

A Flask server that provides API endpoints for fal inference with LoRA support.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   - Copy `env.example` to `.env`
   - Add your fal API key:
     ```
     FAL_KEY=your_actual_fal_api_key_here
     ```

3. **Run the server:**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check

- **GET** `/`
- Returns server status

### Upload LoRA File

- **POST** `/upload-lora`
- Upload a `.safetensors` LoRA file
- Form data with `file` field
- Returns the public URL for the uploaded file

### Generate Image (Full)

- **POST** `/generate`
- Generate images with full control over parameters
- JSON payload:
  ```json
  {
    "prompt": "your prompt here",
    "loras": [
      {
        "path": "https://uploaded-lora-url",
        "scale": 0.8
      }
    ],
    "sync_mode": true
  }
  ```

### Generate Image (Simple)

- **POST** `/generate-simple`
- Simplified endpoint matching your original example
- JSON payload:
  ```json
  {
    "prompt": "portrait photo in my custom style",
    "lora_url": "https://uploaded-lora-url",
    "lora_scale": 0.8
  }
  ```

## Upload Script

Use the separate upload script to upload LoRA files:

```bash
python upload_lora.py path/to/your/lora.safetensors
```

This will upload the file and return the public URL that you can use in inference calls.

## Example Usage

1. **Upload a LoRA file:**

   ```bash
   python upload_lora.py my_custom_style.safetensors
   ```

2. **Generate an image using curl:**
   ```bash
   curl -X POST http://localhost:8000/generate-simple \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "portrait photo in my custom style",
       "lora_url": "https://your-uploaded-lora-url",
       "lora_scale": 0.8
     }'
   ```

## File Structure

```
backend/
├── app.py              # Main Flask server
├── upload_lora.py      # Separate upload script
├── requirements.txt    # Python dependencies
├── env.example         # Environment variables template
└── README.md          # This file
```

## Environment Variables

- `FAL_KEY`: Your fal API key (required)
