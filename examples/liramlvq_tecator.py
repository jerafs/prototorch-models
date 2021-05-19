"""Limited Rank Matrix LVQ example using the Tecator dataset."""

import prototorch as pt
import pytorch_lightning as pl
import torch

if __name__ == "__main__":
    # Dataset
    train_ds = pt.datasets.Tecator(root="~/datasets/", train=True)
    test_ds = pt.datasets.Tecator(root="~/datasets/", train=False)

    # Reproducibility
    pl.utilities.seed.seed_everything(seed=42)

    # Dataloaders
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=32)
    test_loader = torch.utils.data.DataLoader(test_ds, batch_size=32)

    # Hyperparameters
    nclasses = 2
    prototypes_per_class = 2
    hparams = dict(
        distribution=(nclasses, prototypes_per_class),
        input_dim=100,
        latent_dim=2,
        proto_lr=0.005,
        bb_lr=0.005,
    )

    # Initialize the model
    model = pt.models.GMLVQ(hparams,
                            prototype_initializer=pt.components.SMI(train_ds))

    # Callbacks
    vis = pt.models.VisSiameseGLVQ2D(train_ds, border=0.1)

    # Setup trainer
    trainer = pl.Trainer(
        gpus=0,
        max_epochs=20,
        callbacks=[vis],
        weights_summary=None,
    )

    # Training loop
    trainer.fit(model, train_loader, test_loader)

    # Save the model
    torch.save(model, "liramlvq_tecator.pt")

    # Load a saved model
    saved_model = torch.load("liramlvq_tecator.pt")

    # Display the Lambda matrix
    saved_model.show_lambda()

    # Testing
    # TODO
    # trainer.test(model, test_dataloaders=test_loader)
