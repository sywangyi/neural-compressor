# Stable Diffusion

The script ```run_diffusion.py``` is based on [huggingface/diffusers](https://github.com/huggingface/diffusers/tree/main/examples/text_to_image) and provides post-training static quantization approach based on Intel® Neural Compressor.


## Requirements
 The dataset [pokemon-blip-captions](https://huggingface.co/datasets/lambdalabs/pokemon-blip-captions) and metric FID from ```pyotrch_fid``` is necessary for the work.
```
pip install -r requirements.txt
```

## Metric and Ground Truth Image
In this case, we used FID metric to evaluate the model, so we should download training datasets and choose one image to a directory(like "base_images").
>**Note:** In this case we used picture: [Ground_Truth_Image](https://datasets-server.huggingface.co/assets/lambdalabs/pokemon-blip-captions/--/lambdalabs--pokemon-blip-captions/train/14/image/image.jpg).

## Quantization
```bash
python run_diffusion.py \
    --model_name_or_path lambdalabs/sd-pokemon-diffusers \
    --tune \
    --quantization_approach PostTrainingStatic \
    --perf_tol 0.02 \
    --output_dir /tmp/diffusion_output \
    --base_images base_images \
    --input_text "a drawing of a gray and black dragon" \
    --calib_text "a drawing of a green pokemon with red eyes"
```


the images before and after quantization show below:

The image generated by original model(FID with ground truth: 333):

<img src=images/fp32.png />

The image generated by quantized UNet(FID with ground truth: 246):

<img src=images/int8.png />


## Performance
Original model
```bash
python run_diffusion.py \
    --model_name_or_path lambdalabs/sd-pokemon-diffusers \
    --output_dir /tmp/diffusion_output \
    --base_images base_images \
    --benchmark
```
The model of quantized UNet
```bash
python run_diffusion.py \
    --model_name_or_path lambdalabs/sd-pokemon-diffusers \
    --output_dir /tmp/diffusion_output \
    --base_images base_images \
    --benchmark \
    --int8
```

>**Note:** You will see the inference performance speedup with Intel DL Boost (VNNI) on Intel(R) Xeon(R) hardware. You may also refer to [Performance Tuning Guide](https://intel.github.io/intel-extension-for-pytorch/cpu/latest/tutorials/performance_tuning/tuning_guide.html) for more optimizations.
