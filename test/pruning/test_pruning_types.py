import unittest

import torch
import torchvision
import torch.nn as nn

from neural_compressor.data import Datasets
from neural_compressor.experimental.data.dataloaders.pytorch_dataloader import PyTorchDataLoader
from neural_compressor.config import WeightPruningConfig
from neural_compressor.pruner.pruning import Pruning

local_types_config = [
    {
        "start_step": 0,
        "end_step": 0,
        "pruning_type": "pattern_lock",
        "op_names": ['layer1.*'],
        "excluded_op_names": ['layer2.*'],
        "pruning_scope": "global"
    },
    {
        "start_step": 1,
        "end_step": 1,
        "target_sparsity": 0.5,
        "pruning_type": "snip_momentum_progressive",
        "pruning_frequency": 2,
        "op_names": ['layer2.*'],
        "pruning_scope": "local",
        "pattern": "4x1",
        "sparsity_decay_type": "exp"
    },
    {
        "start_step": 2,
        "end_step": 8,
        "target_sparsity": 0.8,
        "pruning_type": "snip_progressive",
        "pruning_frequency": 1,
        "op_names": ['layer3.*'],
        "pruning_scope": "local",
        "pattern": "16x1",
        "sparsity_decay_type": "cube"
    }
]

fake_snip_config = WeightPruningConfig(local_types_config, target_sparsity=0.9, start_step=0, \
                                       end_step=10, pruning_frequency=3, sparsity_decay_type="exp")


class TestPruningTypes(unittest.TestCase):
    model = torchvision.models.resnet18()

    def test_pruning_types(self):
        prune = Pruning(fake_snip_config)
        prune.model = self.model
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.0001)
        datasets = Datasets('pytorch')
        dummy_dataset = datasets['dummy'](shape=(10, 3, 224, 224), low=0., high=1., label=True)
        dummy_dataloader = PyTorchDataLoader(dummy_dataset)
        prune.on_train_begin()
        prune.update_config(pruning_frequency=1)
        for epoch in range(2):
            self.model.train()
            prune.on_epoch_begin(epoch)
            local_step = 0
            for image, target in dummy_dataloader:
                prune.on_step_begin(local_step)
                output = self.model(image)
                loss = criterion(output, target)
                optimizer.zero_grad()
                loss.backward()
                prune.on_before_optimizer_step()
                optimizer.step()
                prune.on_after_optimizer_step()
                prune.on_step_end()
                local_step += 1

            prune.on_epoch_end()
        prune.get_sparsity_ratio()
        prune.on_train_end()
        prune.on_before_eval()
        prune.on_after_eval()


if __name__ == "__main__":
    unittest.main()
