import json
import hydra
import subprocess
import torch
from omegaconf import omegaconf
from maverick.common.util import *
from maverick.common.metrics import *
from tqdm import tqdm
from data.pl_data_modules import BasePLDataModule
from models.pl_modules import BasePLModule


@torch.no_grad()
def evaluate(conf: omegaconf.DictConfig):
    device = conf.evaluation.device
    hydra.utils.log.info("Using {} as device".format(device))
    pl_data_module: BasePLDataModule = hydra.utils.instantiate(conf.data.datamodule, _recursive_=False)

    pl_data_module.prepare_data()
    pl_data_module.setup("test")

    model = BasePLModule.load_from_checkpoint(conf.evaluation.checkpoint, _recursive_=False, map_location=device)

    predictions = model_predictions_with_dataloader(model, pl_data_module.test_dataloader(), device)
    with open("data/gap/gap-test-ontoformat.jsonl", "r") as fr:
        with open("data/gap/gap-test-output.tsv", "w") as fw:
            for line, pred in zip(fr.readlines(), predictions):
                doc = json.loads(line)
                A, B = A_and_B_corefs(pred, doc["gap_pronoun_offsets"], doc["gap_A_offsets"], doc["gap_B_offsets"])
                fw.write(doc["doc_key"] + "\t" + str(A) + "\t" + str(B) + "\n")


def A_and_B_corefs(clusters, pronoun_offsets, A_offsets, B_offsets):
    A_Coref = False
    B_Coref = False
    pronoun_in_clusters = find_offsets_in_clusters(clusters, pronoun_offsets)
    A_in_clusters = find_offsets_in_clusters(clusters, A_offsets)
    B_in_clusters = find_offsets_in_clusters(clusters, B_offsets)
    # pronoun is in clusters
    if pronoun_in_clusters != None:
        # A is in clusters
        if A_in_clusters != None and A_in_clusters != B_in_clusters:
            A_Coref = candidate_pronoun_clustered(clusters, pronoun_in_clusters, A_in_clusters)
        if B_in_clusters != None and B_in_clusters != A_in_clusters:
            B_Coref = candidate_pronoun_clustered(clusters, pronoun_in_clusters, B_in_clusters)
    return A_Coref, B_Coref


def candidate_pronoun_clustered(clusters, pronoun, candidate):
    clustered = False
    for cluster in clusters:
        if pronoun in cluster and candidate in cluster:
            clustered = True
    return clustered


def find_offsets_in_clusters(clusters, offsets):
    clusters = [list(item) for item in clusters]
    mentions = [item for sublist in clusters for item in sublist]
    result = None
    for mention in mentions:
        if offsets[0] >= mention[0] and offsets[1] <= mention[1]:
            if result == None:
                result = mention
            else:
                if result[1] - result[0] > mention[1] - mention[0]:
                    result = mention
    return result


def model_predictions_with_dataloader(model, test_dataloader, device):
    model.to(device)
    model.eval()
    predictions = []

    for batch in tqdm(test_dataloader, desc="Test", total=test_dataloader.__len__()):
        output = model.model(
            stage="test",
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
            eos_mask=batch["eos_mask"].to(device),
            tokens=batch["tokens"],
            subtoken_map=batch["subtoken_map"],
            new_token_map=batch["new_token_map"],
        )

        clusters_predicted = original_token_offsets(
            clusters=output["pred_dict"]["clusters"],
            subtoken_map=batch["subtoken_map"][0],
            new_token_map=batch["new_token_map"][0],
        )
        predictions.append(clusters_predicted)
    return predictions


@hydra.main(config_path="../conf", config_name="root")
def main(conf: omegaconf.DictConfig):
    evaluate(conf)


if __name__ == "__main__":
    main()
