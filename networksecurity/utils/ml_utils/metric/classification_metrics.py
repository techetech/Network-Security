from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,)


def get_classification_metrics(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Calculate classification metrics: recall, precision, and F1 score.

    Args:
        y_true (list): True labels.
        y_pred (list): Predicted labels.

    Returns:
        ClassificationMetricArtifact: Artifact containing the calculated metrics.
    """
    try:
        recall = recall_score(y_true, y_pred, average='weighted')
        precision = precision_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')

        logging.info(f"Recall: {recall}, Precision: {precision}, F1 Score: {f1}")

        return ClassificationMetricArtifact(
            recall_score=recall,
            precision_score=precision,
            f1_score=f1
        )
    except Exception as e:
        raise NetworkSecurityException(e) from e 