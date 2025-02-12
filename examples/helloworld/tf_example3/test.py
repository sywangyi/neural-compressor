from argparse import ArgumentParser
from neural_compressor.data.datasets.dataset import TensorflowImageRecord
from neural_compressor.data.transforms.imagenet_transform import BilinearImagenetTransform
from neural_compressor.data.transforms.transform import ComposeTransform
from neural_compressor.data.dataloaders.default_dataloader import DefaultDataLoader

arg_parser = ArgumentParser(description='Parse args')
arg_parser.add_argument('--dataset_location',
                        help='location of calibration dataset and evaluate dataset')
args = arg_parser.parse_args()

eval_dataset = TensorflowImageRecord(root=args.dataset_location, transform=ComposeTransform(transform_list= \
        [BilinearImagenetTransform(height=224, width=224)]))
eval_dataloader = DefaultDataLoader(dataset=eval_dataset, batch_size=1)

def main():
    from neural_compressor.config import MixedPrecisionConfig
    from neural_compressor import mix_precision
    config = MixedPrecisionConfig()
    mix_precision_model = mix_precision.fit(
        model="./mobilenet_v1_1.0_224_frozen.pb",
        config=config,
        eval_dataloader=eval_dataloader)

if __name__ == "__main__":
    main()
