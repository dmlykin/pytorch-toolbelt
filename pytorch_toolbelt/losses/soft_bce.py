import torch
from torch import nn
import torch.nn.functional as F

__all__ = ["SoftBCELoss"]


class SoftBCELoss(nn.Module):
    def __init__(self, smooth_factor=1e-4, ignore_index=None, reduction="mean"):
        super().__init__()
        self.smooth_factor = smooth_factor
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, label_input, label_target):
        not_ignored_mask = label_target != self.ignore_index

        label_target = (1 - label_target) * self.smooth_factor + label_target * (1 - self.smooth_factor)

        loss = F.binary_cross_entropy_with_logits(label_input, label_target, reduction="none")

        loss = loss * not_ignored_mask.float()

        if self.reduction == "mean":
            loss = loss.mean()

        if self.reduction == "sum":
            loss = loss.sum()

        return loss
