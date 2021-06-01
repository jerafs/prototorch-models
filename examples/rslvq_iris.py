"""Probabilistic-LVQ example using the Iris dataset."""

import argparse

import pytorch_lightning as pl
import torch

import prototorch as pt

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser()
    parser = pl.Trainer.add_argparse_args(parser)
    args = parser.parse_args()

    # Reproducibility
    pl.utilities.seed.seed_everything(seed=42)

    # Dataset
    train_ds = pt.datasets.Iris(dims=[0, 2])

    # Dataloaders
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=64)

    # Hyperparameters
    hparams = dict(
        distribution=[2, 2, 3],
        lr=0.05,
        variance=0.3,
    )

    # Initialize the model
    model = pt.models.probabilistic.RSLVQ(
        hparams,
        optimizer=torch.optim.Adam,
        prototype_initializer=pt.components.SSI(train_ds, noise=0.2),
    )

    print(model)

    # Callbacks
    vis = pt.models.VisGLVQ2D(data=train_ds)

    # Setup trainer
    trainer = pl.Trainer.from_argparse_args(
        args,
        callbacks=[vis],
        terminate_on_nan=True,
        weights_summary=None,
        # accelerator="ddp",
    )

    # Training loop
    trainer.fit(model, train_loader)