# Adapted for use in InvokeAI by Lincoln Stein, July 2023
#
"""Conversion script for the Stable Diffusion checkpoints."""

from pathlib import Path
from typing import Dict

import torch
from diffusers import AutoencoderKL
from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
    convert_ldm_vae_checkpoint,
    create_vae_diffusers_config,
    download_controlnet_from_original_ckpt,
    download_from_original_stable_diffusion_ckpt,
)
from omegaconf import DictConfig


def convert_ldm_vae_to_diffusers(
    checkpoint: Dict[str, torch.Tensor],
    vae_config: DictConfig,
    image_size: int,
    precision: torch.dtype = torch.float16,
) -> AutoencoderKL:
    """Convert a checkpoint-style VAE into a Diffusers VAE"""
    vae_config = create_vae_diffusers_config(vae_config, image_size=image_size)
    converted_vae_checkpoint = convert_ldm_vae_checkpoint(checkpoint, vae_config)

    vae = AutoencoderKL(**vae_config)
    vae.load_state_dict(converted_vae_checkpoint)
    return vae.to(precision)


def convert_ckpt_to_diffusers(
    checkpoint_path: str | Path,
    dump_path: str | Path,
    precision: torch.dtype = torch.float16,
    use_safetensors: bool = True,
    **kwargs,
):
    """
    Takes all the arguments of download_from_original_stable_diffusion_ckpt(),
    and in addition a path-like object indicating the location of the desired diffusers
    model to be written.
    """
    pipe = download_from_original_stable_diffusion_ckpt(Path(checkpoint_path).as_posix(), **kwargs)
    pipe = pipe.to(precision)

    # TO DO: save correct repo variant
    pipe.save_pretrained(
        dump_path,
        safe_serialization=use_safetensors,
    )


def convert_controlnet_to_diffusers(
    checkpoint_path: Path,
    dump_path: Path,
    precision: torch.dtype = torch.float16,
    **kwargs,
):
    """
    Takes all the arguments of download_controlnet_from_original_ckpt(),
    and in addition a path-like object indicating the location of the desired diffusers
    model to be written.
    """
    pipe = download_controlnet_from_original_ckpt(checkpoint_path.as_posix(), **kwargs)
    pipe = pipe.to(precision)

    # TO DO: save correct repo variant
    pipe.save_pretrained(dump_path, safe_serialization=True)
