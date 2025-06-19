import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingPrompt, setIsGeneratingPrompt] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [error, setError] = useState(null);

  // Fixed LoRA configuration
  const LORA_URL = "https://fal.media/files/kangaroo/XI5TnkDaCxJIVlszsEKRb.bin";
  const LORA_SCALE = 0.8;

  // Art style presets
  const presets = [
    { name: "Oil", style: "in the style of zsh-oil" },
    { name: "Watercolor", style: "in the style of zsh-watercolor" },
    { name: "Colored Pencil", style: "in the style of zsh-pencil" },
    { name: "Acrylic", style: "in the style of zsh-acrylic" },
  ];

  const handlePresetClick = (style) => {
    if (isLoading || isGeneratingPrompt) return;

    // Replace the entire prompt with the style
    setPrompt(style);
  };

  const handleGeneratePrompt = async () => {
    if (isLoading || isGeneratingPrompt) return;

    setIsGeneratingPrompt(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/generate-prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), // Let the backend choose a random style
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate prompt");
      }

      if (data.success && data.prompt) {
        setPrompt(data.prompt);
      } else {
        throw new Error("No prompt generated");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGeneratingPrompt(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!prompt.trim()) {
      setError("Please enter a prompt");
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedImage(null);

    try {
      const payload = {
        prompt: prompt.trim(),
        lora_url: LORA_URL,
        lora_scale: LORA_SCALE,
      };

      const response = await fetch("http://localhost:8000/generate-simple", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate image");
      }

      if (data.success && data.result && data.result.images && data.result.images.length > 0) {
        setGeneratedImage(data.result.images[0].url);
      } else {
        throw new Error("No image generated");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>emily-diffusion</h1>
        <p className="subtitle">me when i replace myself</p>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="prompt">Prompt *</label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the image you want to generate..."
              rows={3}
              disabled={isLoading || isGeneratingPrompt}
            />
            <button
              type="button"
              className="generate-prompt-btn"
              onClick={handleGeneratePrompt}
              disabled={isLoading || isGeneratingPrompt}
            >
              {isGeneratingPrompt ? "Generating Prompt..." : "Generate Prompt"}
            </button>
          </div>

          <div className="presets">
            <label>Art Style Presets:</label>
            <div className="preset-buttons">
              {presets.map((preset) => (
                <button
                  key={preset.name}
                  type="button"
                  className="preset-btn"
                  onClick={() => handlePresetClick(preset.style)}
                  disabled={isLoading || isGeneratingPrompt}
                >
                  {preset.name}
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading || isGeneratingPrompt || !prompt.trim()}
            className="generate-btn"
          >
            {isLoading ? "Generating..." : "Generate Image"}
          </button>
        </form>

        {error && (
          <div className="error">
            <p>❌ {error}</p>
          </div>
        )}

        {isLoading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Generating your image... This may take a few moments.</p>
          </div>
        )}

        {generatedImage && (
          <div className="result">
            <h3>Generated Image</h3>
            <div className="image-container">
              <img
                src={generatedImage}
                alt="Generated artwork"
                onError={() => setError("Failed to load generated image")}
              />
            </div>
            <div className="image-actions">
              <a
                href={generatedImage}
                target="_blank"
                rel="noopener noreferrer"
                className="download-btn"
              >
                Open Full Size
              </a>
            </div>
          </div>
        )}

        <div className="info">
          <h3>How to use:</h3>
          <ol>
            <li>Enter a descriptive prompt for the image you want to generate</li>
            <li>Click an art style preset to add it to your prompt</li>
            <li>Click "Generate Image" and wait for the result</li>
            <li>View and download your generated image</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default App;
