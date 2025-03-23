# model_loader.py
import torch
from diffusers import DiffusionPipeline

print("Loading Stable Diffusion model...")

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16"
)
pipe.to("cpu")

print("Model loaded successfully!")
