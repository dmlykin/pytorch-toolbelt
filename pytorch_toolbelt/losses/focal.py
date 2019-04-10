from .functional import sigmoid_focal_loss
from torch.nn.modules.loss import _Loss

__all__ = ['BinaryFocalLoss', 'FocalLoss']


class BinaryFocalLoss(_Loss):
    def __init__(self, alpha=0.5, gamma=2, ignore=None):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.ignore = ignore

    def forward(self, label_input, label_target):
        """Compute focal loss for binary classification problem.
        """
        num_classes = label_input.size(1)
        label_target = label_target.view(-1)
        label_input = label_input.view(-1, num_classes)

        if self.ignore is not None:
            # Filter predictions with ignore label from loss computation
            not_ignored = label_target != self.ignore
            label_input = label_input[not_ignored]
            label_target = label_target[not_ignored]

        loss = sigmoid_focal_loss(label_input, label_target, gamma=self.gamma, alpha=self.alpha)
        return loss


class FocalLoss(_Loss):
    def __init__(self, alpha=0.5, gamma=2):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, label_input, label_target):
        """Compute focal loss for multi-class problem.
        Ignores anchors having -1 target label
        """
        num_classes = label_input.size(1)
        loss = 0
        label_target = label_target.view(-1)
        label_input = label_input.view(-1, num_classes)

        # Filter anchors with -1 label from loss computation
        not_ignored = label_target >= 0

        for cls in range(num_classes):
            cls_label_target = (label_target == (cls + 0)).long()
            cls_label_input = label_input[..., cls]

            cls_label_target = cls_label_target[not_ignored]
            cls_label_input = cls_label_input[not_ignored]

            loss += sigmoid_focal_loss(cls_label_input, cls_label_target, gamma=self.gamma, alpha=self.alpha)
        return loss
