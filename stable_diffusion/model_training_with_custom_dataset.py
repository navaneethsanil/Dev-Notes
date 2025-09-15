# Install extra training tools
!pip install xformers bitsandbytes

from diffusers import StableDiffusionXLTrainer
import torch

# Point to your dataset (images + captions in a folder)
dataset_path = "./my_dataset"

trainer = StableDiffusionXLTrainer(
    model="stabilityai/stable-diffusion-xl-base-1.0",
    dataset=dataset_path,
    output_dir="./lora-output",
    use_lora=True,
    train_text_encoder=True,
    resolution=1024,
    train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=1e-4,
    max_train_steps=1000,
    checkpointing_steps=100,
    mixed_precision="fp16",
    report_to="tensorboard",
)

trainer.train()


# This produces a LoRA checkpoint you can later load into your pipeline:
pipe.load_lora_weights("./lora-output")
