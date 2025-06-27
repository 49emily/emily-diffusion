# emily-diffusion

a flux lora that i trained on 21 samples of my artwork from my recent portfolio, across 4 media, for 26 epochs.

each work was labeled by a custom image annotation script with gpt-4o. you can find the training dataset in `training_data/` and the final lora weights at `backend/emily-000026.safetensors`. you need to upload this to your local fal storage and provide openai and fal api keys (see `env.example`) to run the backend and the web UI.


