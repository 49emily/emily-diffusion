#!/usr/bin/env python3
"""
Flask server for fal inference with LoRA support.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import fal_client
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize OpenAI client
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Warning: Failed to initialize OpenAI client: {e}")
    openai_client = None


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "Fal inference server is running"})


@app.route("/upload-lora", methods=["POST"])
def upload_lora():
    """
    Upload a LoRA file to fal.
    Expects a file in the request.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith(".safetensors"):
            return jsonify({"error": "File must be a .safetensors file"}), 400

        # Save the file temporarily
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)

        # Upload to fal
        lora_url = fal_client.upload_file(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        return jsonify(
            {"success": True, "lora_url": lora_url, "filename": file.filename}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate", methods=["POST"])
def generate_image():
    """
    Generate an image using fal-ai/flux-lora.

    Expected JSON payload:
    {
        "prompt": "your prompt here",
        "loras": [
            {
                "path": "https://...",  // LoRA URL
                "scale": 0.8
            }
        ],
        "sync_mode": true  // optional
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        if "prompt" not in data:
            return jsonify({"error": "Prompt is required"}), 400

        # Prepare arguments for fal
        arguments = {"prompt": data["prompt"], "sync_mode": data.get("sync_mode", True)}

        # Add LoRAs if provided
        if "loras" in data and data["loras"]:
            arguments["loras"] = data["loras"]

        # Call fal inference using the correct API
        handler = fal_client.submit(
            "fal-ai/flux-lora",
            arguments=arguments,
        )

        # Get the result
        result = handler.get()

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate-simple", methods=["POST"])
def generate_simple():
    """
    Simplified endpoint that matches your original example.

    Expected JSON payload:
    {
        "prompt": "portrait photo in my custom style",
        "lora_url": "https://...",
        "lora_scale": 0.8
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        if "prompt" not in data:
            return jsonify({"error": "Prompt is required"}), 400

        # Prepare arguments
        arguments = {"prompt": data["prompt"], "image_size": "square"}

        # Add LoRA if provided
        if "lora_url" in data:
            # lora_scale = data.get("lora_scale", 0.8)
            arguments["loras"] = [{"path": data["lora_url"]}]

        # Call fal inference using the correct API
        handler = fal_client.submit(
            "fal-ai/flux-lora",
            arguments=arguments,
        )

        # Get the result
        result = handler.get()

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate-prompt", methods=["POST"])
def generate_prompt():
    """
    Generate a new prompt using GPT based on the provided examples.

    Expected JSON payload:
    {
        "style": "zsh-oil" | "zsh-watercolor"   // optional, will be chosen randomly if not provided
    }
    """
    try:
        # Check if OpenAI client is available
        if openai_client is None:
            return (
                jsonify(
                    {
                        "error": "OpenAI client not available. Please check your OPENAI_API_KEY."
                    }
                ),
                500,
            )

        data = request.get_json() or {}
        requested_style = data.get("style")

        # Define the example prompts
        example_prompts = [
            "in the style of zsh-oil, 1girl, leaning on railing, oval face smooth tan skin, subtle asym mouth eyes, medium forehead, dark straight thick eyebrows, almond brown eyes medium lashes, gaze slightly past camera, straight medium nose rounded tip, full closed lips neutral, left ear silver stud earring, long straight black hair middle part stray strands, natural makeup soft blush muted pink lips, cream satin low v-neck spaghetti-strap dress loose fit, shoulders collarbones upper chest exposed, right arm extended back hand on railing, left arm bent on hip, slight forward lean torso turned slightly left, head upright slight tilt left, background, green metal structure left side vertical beams matte muted green with bolts, calm blue-teal water spans horizon gentle ripples, sunset sky upper band gradient blue to orange patchy clouds, distant dark cityscape silhouette along horizon, green-white metal guard railing runs behind subject, view from eye-level slight left front",
            "in the style of zsh-oil, 1girl, standing, long straight dark-brown hair center-part, almond eyes looking down left, pensive melancholic expression, smooth warm-tan skin, no makeup, elongated symmetrical face, natural arched eyebrows, straight medium nose, small pursed lips, rounded chin soft jawline, relaxed slouched shoulders, arms at sides, light-blue sleeveless square-neck top loose fit, no accessories, head tilted down left three-quarter, frontal torso, background, dark navy blue painterly backdrop full frame subtle gradients, white chalk-like handwritten chinese text overlay scattered and overlapping figure semi-transparent varied size, camera eye-level frontal view",
            "in the style of zsh-watercolor, 1girl, floating supine, face tilted upward partially submerged, eyes closed gentle curve, long light eyelashes, faint eyebrows, bluish eyelids, delicate nose, lips gently parted reddish pink no teeth, small rounded chin, flushed pink cheeks, smooth pale forehead, soft jawline, pale cool undertones smooth complexion, cool blue-green reflections on skin, serene expression, long reddish-brown hair fans in water soft hairline, subtle wet sheen, youthful skin, no makeup, no accessories, no tattoos or marks, long pale neck, bare submerged shoulders arms hidden, no clothing visible, blurred waterline soft edges, head tilted back angled up viewer left upside-down, background, abstract color washes, around head blend outward, wet-on-wet texture, muted greens aquas smoky grays, feathered diffuse edges, muted palette, greens browns light blues cluster edges, low saturation gentle gradients, layered depth, dreamy texture, watery blurry swirls around figure, fluid gradients no sharp forms, tranquil ethereal atmosphere, no distinct objects, purely abstract backdrop, swirling watercolor patterns, soft blending with figure, top-down bird's-eye close view from above",
        ]

        # Available styles
        styles = ["zsh-oil", "zsh-watercolor"]

        # Validate requested style or choose randomly
        if requested_style and requested_style not in styles:
            return (
                jsonify(
                    {"error": f"Invalid style. Must be one of: {', '.join(styles)}"}
                ),
                400,
            )

        target_style = (
            requested_style if requested_style else "one of zsh-oil, zsh-watercolor"
        )

        # # Create the GPT prompt
        # system_prompt = """You are an expert at creating detailed art prompts. Given example prompts, create a new prompt that follows the same style and structure but with different content. The prompt should be highly detailed and specific, maintaining the same level of descriptive precision as the examples."""

        user_prompt = f"""Given these prompts, write a new text prompt I can use to generate a painting adhering to the same style and central concepts described here. Choose either zsh-oil or zsh-watercolor.

Examples:
{chr(10).join(f"- {prompt}" for prompt in example_prompts)}

Return only the prompt text, no additional explanation."""

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                # {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.8,
        )

        generated_prompt = response.choices[0].message.content.strip()

        return jsonify(
            {
                "success": True,
                "prompt": generated_prompt,
                "style_used": requested_style or "randomly_chosen",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.getenv("FAL_KEY"):
        print("Warning: FAL_KEY environment variable not set!")
        print("Please set your fal API key in a .env file or environment variable.")

    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key in a .env file or environment variable.")

    app.run(debug=True, host="0.0.0.0", port=8000)
