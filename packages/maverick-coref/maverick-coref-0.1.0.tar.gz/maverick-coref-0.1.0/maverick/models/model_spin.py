import torch
import numpy as np
import random

from transformers import (
    AutoModel,
    AutoConfig,
    DistilBertForSequenceClassification,
    DistilBertConfig,
)

from maverick.common.util import *
from maverick.common.constants import *


class MentionClusterClassifier(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
        # self.softmax_dummy = torch.tensor([0.0], requires_grad=True).unsqueeze(0)

    def forward(self, mention_hidden_states, cluster_hidden_states, attention_mask, labels=None):
        # repreated tensor of mention_hs, to append in first position for each possible mention cluster pair
        repeated_mention_hs = mention_hidden_states.unsqueeze(0).repeat(cluster_hidden_states.shape[0], 1, 1)

        # mention cluste pairs by contatenating mention vectors to cluster padded matrix
        mention_cluster_pairs = torch.cat((repeated_mention_hs, cluster_hidden_states), dim=1)
        attention_mask = torch.cat(
            (
                torch.ones(cluster_hidden_states.shape[0], 1, device=self.model.device),
                attention_mask,
            ),
            dim=1,
        )

        logits = self.model(inputs_embeds=mention_cluster_pairs, attention_mask=attention_mask).logits
        """logits = torch.cat([self.softmax_dummy.to(self.model.device), logits], dim=0)  # debug
        logits = logits.squeeze(1).unsqueeze(0)"""

        loss = None
        if labels is not None:
            """labels = (
                torch.tensor([0], device=self.model.device)
                if torch.sum(labels) == 0
                else torch.arange(labels.size(0), device=self.model.device)[labels > 0] + 1
            )  # debug
            loss = torch.nn.functional.cross_entropy(logits, labels)"""
            loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels.unsqueeze(1).to(self.model.device))
        return loss, logits


class Model(torch.nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # document transformer encoder
        self.encoder_hf_model_name = kwargs["huggingface_model_name"]
        self.encoder = AutoModel.from_pretrained(self.encoder_hf_model_name)
        self.encoder_config = AutoConfig.from_pretrained(self.encoder_hf_model_name)
        # self.encoder_config.attention_window = 1024
        self.encoder.resize_token_embeddings(self.encoder.embeddings.word_embeddings.num_embeddings + 3)

        # freeze
        if kwargs["freeze_encoder"]:
            for param in self.encoder.parameters():
                param.requires_grad = False

        # span representation, now is concat_start_end
        self.span_representation = kwargs["span_representation"]
        # type of representation layer in 'Linear, FC, LSTM-left, LSTM-right, Conv1d'
        self.representation_layer_type = "FC"  # fullyconnected
        # span hidden dimension
        self.token_hidden_size = self.encoder_config.hidden_size

        # if span representation method is to concatenate start and end, a mention hidden size will be 2*token_hidden_size
        if self.span_representation == "concat_start_end":
            self.mention_hidden_size = self.token_hidden_size * 2

        # incremental transformer classifier (as slim as possible!)
        self.incremental_model_hidden_size = kwargs.get("incremental_model_hidden_size", 384)  # 768/2
        self.incremental_model_num_layers = kwargs.get("incremental_model_num_layers", 1)
        self.incremental_model_config = DistilBertConfig(num_labels=1, hidden_size=self.incremental_model_hidden_size)
        self.incremental_model = DistilBertForSequenceClassification(self.incremental_model_config).to(self.encoder.device)
        self.incremental_model.distilbert.transformer.layer = self.incremental_model.distilbert.transformer.layer[
            : self.incremental_model_num_layers
        ]
        self.incremental_model.distilbert.embeddings.word_embeddings = None
        self.incremental_transformer = MentionClusterClassifier(model=self.incremental_model)

        # encodes mentions for incremental clustering
        self.incremental_span_encoder = RepresentationLayer(
            type=self.representation_layer_type,  # fullyconnected
            input_dim=self.mention_hidden_size,
            output_dim=self.incremental_model_hidden_size,
            hidden_dim=int(self.mention_hidden_size / 2),
        )

        # # example
        # self.representation_ment_start = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=self.mention_hidden_size,
        #     output_dim=self.incremental_model_hidden_size * 4,
        #     hidden_dim=self.mention_hidden_size,
        # )

        # # example
        # self.repr_ment_end = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=self.mention_hidden_size,
        #     output_dim=self.incremental_model_hidden_size * 4,
        #     hidden_dim=self.mention_hidden_size,
        # )

        # self.antecedent_s2s_classifier = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=self.token_hidden_size,
        #     output_dim=self.token_hidden_size,
        #     hidden_dim=self.token_hidden_size,
        # )
        # self.antecedent_e2e_classifier = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=self.token_hidden_size,
        #     output_dim=self.token_hidden_size,
        #     hidden_dim=self.token_hidden_size,
        # )

        # self.antecedent_s2e_classifier = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=self.token_hidden_size,
        #     output_dim=self.token_hidden_size,
        #     hidden_dim=self.token_hidden_size,
        # )
        # self.antecedent_e2s_classifier = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=self.token_hidden_size,
        #     output_dim=self.token_hidden_size,
        #     hidden_dim=self.token_hidden_size,
        # )

        # # example
        # self.incremental_mention_cluster_encoder = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=2 * self.incremental_model_hidden_size,
        #     output_dim=self.incremental_model_hidden_size,
        #     hidden_dim=2 * self.incremental_model_hidden_size,
        # )

        # # example
        # self.incremental_mention_cluster_discriminator = RepresentationLayer(
        #     type=self.representation_layer_type,  # fullyconnected
        #     input_dim=3 * self.incremental_model_hidden_size,
        #     output_dim=1,
        #     hidden_dim=self.incremental_model_hidden_size,
        # )

        # mention extraction layers
        # representation of start token
        self.start_token_representation = RepresentationLayer(
            type=self.representation_layer_type,
            input_dim=self.token_hidden_size,
            output_dim=self.token_hidden_size,
            hidden_dim=self.token_hidden_size,
        )

        # representation of end token
        self.end_token_representation = RepresentationLayer(
            type=self.representation_layer_type,
            input_dim=self.token_hidden_size,
            output_dim=self.token_hidden_size,
            hidden_dim=self.token_hidden_size,
        )

        # models probability to be the start of a mention
        self.start_token_classifier = RepresentationLayer(
            type=self.representation_layer_type,
            input_dim=self.token_hidden_size,
            output_dim=1,
            hidden_dim=self.token_hidden_size,
        )

        # model mention probability from start and end representations
        self.start_end_classifier = RepresentationLayer(
            type=self.representation_layer_type,
            input_dim=self.mention_hidden_size,
            output_dim=1,
            hidden_dim=self.token_hidden_size,
        )

    # takes last_hidden_states, eos_mask, ground truth and stage
    # check if mention_mask deletes some good gold mentions!
    def squad_mention_extraction_forloop(self, lhs, eos_mask, gold_mentions, gold_starts, stage):
        start_idxs = []
        mention_idxs = []
        start_loss = torch.tensor([0.0], requires_grad=True, device=self.encoder.device)
        mention_loss = torch.tensor([0.0], requires_grad=True, device=self.encoder.device)

        for bidx in range(0, lhs.shape[0]):
            lhs_batch = lhs[bidx]  # SEQ_LEN X HIDD_DIM
            eos_mask_batch = eos_mask[bidx]  # SEQ_LEN X SEQ_LEN

            # compute start logits
            start_logits_batch = self.start_token_classifier(lhs_batch).squeeze(-1)  # SEQ_LEN

            if gold_starts != None:
                loss = torch.nn.functional.binary_cross_entropy_with_logits(start_logits_batch, gold_starts[bidx])

                # accumulate loss
                start_loss = start_loss + loss

            # compute start positions
            start_idxs_batch = ((torch.sigmoid(start_logits_batch) > 0.5)).nonzero(as_tuple=False).squeeze(-1)

            start_idxs.append(start_idxs_batch.detach().clone())
            # in training, use gold starts to learn to extract mentions, inference use predicted ones
            if stage == "train":
                start_idxs_batch = (
                    ((torch.sigmoid(gold_starts[bidx]) > 0.5)).nonzero(as_tuple=False).squeeze(-1)
                )  # NUM_GOLD_STARTS

            # contains all possible start end indices pairs, i.e. for all starts, all possible ends looking at EOS index
            possibles_start_end_idxs = (eos_mask_batch[start_idxs_batch] == 1).nonzero(as_tuple=False)  # STARTS x 2

            # this is to have reference respect to original positions
            possibles_start_end_idxs[:, 0] = start_idxs_batch[possibles_start_end_idxs[:, 0]]

            possible_start_idxs = possibles_start_end_idxs[:, 0]
            possible_end_idxs = possibles_start_end_idxs[:, 1]

            # extract start and end hidden states
            starts_hidden_states = lhs_batch[possible_end_idxs]  # start
            ends_hidden_states = lhs_batch[possible_start_idxs]  # end

            # concatenation of start to end representations created using a representation layer
            s2e_representations = torch.cat(
                (
                    self.start_token_representation(starts_hidden_states),
                    self.end_token_representation(ends_hidden_states),
                ),
                dim=-1,
            )

            # classification of mentions
            s2e_logits = self.start_end_classifier(s2e_representations).squeeze(-1)

            # mention_start_idxs and mention_end_idxs
            mention_idxs.append(possibles_start_end_idxs[torch.sigmoid(s2e_logits) > 0.5].detach().clone())

            if s2e_logits.shape[0] != 0:
                if gold_mentions != None:
                    mention_loss_batch = torch.nn.functional.binary_cross_entropy_with_logits(
                        s2e_logits,
                        gold_mentions[bidx][possible_start_idxs, possible_end_idxs],
                    )
                    mention_loss = mention_loss + mention_loss_batch

        return (start_idxs, mention_idxs, start_loss, mention_loss)

    def incremental_span_clustering(self, mentions_hidden_states, mentions_idxs, gold_clusters, stage):
        # debug_edo_local = {}
        # debug_edo_count_local = {}
        # debug_clustering_errors = 0
        # debug_clustering_count = 0
        # debug_erroneous_local = {}
        # debug_err_erroneous_local = {}
        # debug_err_count_local = {}
        pred_cluster_idxs = []  # cluster_idxs = list of list of tuple of offsets (also output) up to mention_idx
        if gold_clusters != None:
            gold_cluster_idxs = unpad_gold_clusters(gold_clusters)  # gold_cluster_idxs, but padded
            # mention_to_gold_mentions = extract_mentions_to_clusters(gold_cluster_idxs)
            # erroneous = set(list(mention_to_gold_mentions.keys()))
        coreference_loss = torch.tensor([0.0], requires_grad=True, device=self.incremental_model.device)
        mentions_hidden_states = mentions_hidden_states[0]
        idx_to_hs = dict(zip([tuple(m) for m in mentions_idxs.tolist()], mentions_hidden_states))
        # for each mention
        for idx, (
            mention_hidden_states,
            (mention_start_idx, mention_end_idx),
        ) in enumerate(zip(mentions_hidden_states, mentions_idxs)):
            if idx == 0:
                # if first create singleton cluster
                pred_cluster_idxs.append([(mention_start_idx.item(), mention_end_idx.item())])
            else:
                if stage == "train":
                    # if we are in training, retrieve use gold cluster idx to induce loss.
                    cluster_idx, labels = self.new_cluster_idxs_labels(
                        (mention_start_idx, mention_end_idx), gold_cluster_idxs
                    )  # can be used using only tensors
                else:
                    cluster_idx, labels = pred_cluster_idxs, None

                # debug, non ricreare ogni volta, ma usa lsolo quelle encodate, non devi ogni volta reincodarle!
                # get cluster padded matrix matrix and attention mask (excludes padding)
                if cluster_idx == []:
                    print("wtf", str((mention_start_idx, mention_end_idx)))
                cluster_hs, cluster_am = self.get_cluster_states_matrix(idx_to_hs, cluster_idx, stage)

                # produce logits for each possible cluster mention pair
                mention_cluster_loss, logits = self.incremental_transformer(
                    mention_hidden_states=mention_hidden_states,
                    cluster_hidden_states=cluster_hs,
                    attention_mask=cluster_am,
                    labels=labels,
                )

                if mention_cluster_loss != None:
                    coreference_loss = coreference_loss + mention_cluster_loss

                if stage != "train":
                    """predicted_cluster = logits.argmax(axis=1)
                    if predicted_cluster == 0:
                        pred_cluster_idxs.append([(mention_start_idx.item(), mention_end_idx.item())])
                    else:
                        pred_cluster_idxs[predicted_cluster.item() - 1].append((mention_start_idx.item(), mention_end_idx.item()))
                    """
                    # only in inference
                    num_possible_clustering = torch.sum(torch.sigmoid(logits) > 0.5, dim=0).bool().float()

                    if num_possible_clustering == 0:
                        # if no clustering, create new singleton cluster
                        pred_cluster_idxs.append([(mention_start_idx.item(), mention_end_idx.item())])
                        # debug_clustering_count += 1
                    else:
                        # debug_clustering_count += 1
                        # otherwise, take most probabile clustering predicted by the model and assign this mention to that cluster
                        assigned_idx = logits.argmax(axis=0).detach().cpu()
                        pred_cluster_idxs[assigned_idx.item()].append((mention_start_idx.item(), mention_end_idx.item()))
        #                 if gold_clusters != None:
        #                     sim = 0
        #                     mention = (mention_start_idx.item(), mention_end_idx.item())
        #                     assigned = pred_cluster_idxs[assigned_idx.item()]

        #                     if mention in mention_to_gold_mentions:
        #                         gold_of_mention = mention_to_gold_mentions[mention]
        #                         if len(set(assigned)) in debug_edo_local:
        #                             debug_edo_local[len(set(assigned))] += 1 - len(set(assigned) & set(gold_of_mention)) / len(
        #                                 set(assigned)
        #                             )
        #                             debug_erroneous_local[len(set(assigned))] += 1 - len(set(assigned) & erroneous) / len(
        #                                 set(assigned)
        #                             )
        #                             debug_edo_count_local[len(set(assigned))] += 1
        #                         else:
        #                             debug_edo_local[len(set(assigned))] = 1 - len(set(assigned) & set(gold_of_mention)) / len(
        #                                 set(assigned)
        #                             )
        #                             debug_erroneous_local[len(set(assigned))] = 1 - len(set(assigned) & erroneous) / len(
        #                                 set(assigned)
        #                             )
        #                             debug_edo_count_local[len(set(assigned))] = 1
        #                     else:
        #                         if len(set(assigned)) in debug_err_erroneous_local:
        #                             debug_err_erroneous_local[len(set(assigned))] += 1 - len(set(assigned) & erroneous) / len(
        #                                 set(assigned)
        #                             )
        #                             debug_err_count_local[len(set(assigned))] += 1
        #                         else:
        #                             debug_err_erroneous_local[len(set(assigned))] = 1 - len(set(assigned) & erroneous) / len(
        #                                 set(assigned)
        #                             )
        #                             debug_err_count_local[len(set(assigned))] = 1

        # for key, val in debug_edo_local.items():
        #     if key not in self.debug_edo:
        #         self.debug_edo[key] = val
        #         self.debug_erroneous[key] = debug_erroneous_local[key]
        #         self.debug_edo_count[key] = debug_edo_count_local[key]
        #     else:
        #         self.debug_edo[key] += val
        #         self.debug_erroneous[key] += val
        #         self.debug_edo_count[key] += debug_edo_count_local[key]
        # for key, val in sorted(self.debug_edo.items()):
        #     print(
        #         "edo-global"
        #         + ","
        #         + str(key)
        #         + ","
        #         + str(int((val / self.debug_edo_count[key]) * 100))
        #         + ","
        #         + str(int((self.debug_erroneous[key] / self.debug_edo_count[key]) * 100))
        #         + ","
        #         + str(self.debug_edo_count[key]),
        #     )
        # for key, val in debug_err_erroneous_local.items():
        #     if key not in self.debug_err_erroneous:
        #         self.debug_err_erroneous[key] = val
        #         self.debug_err_count[key] = debug_err_count_local[key]
        #     else:
        #         self.debug_err_erroneous[key] += val
        #         self.debug_err_count[key] += debug_err_count_local[key]

        # for key, val in sorted(self.debug_err_erroneous.items()):
        #     print(
        #         "err-global"
        #         + ","
        #         + str(key)
        #         + ","
        #         + str(int((val / self.debug_err_count[key]) * 100))
        #         + ","
        #         + str(self.debug_err_count[key])
        #     )
        # if debug_clustering_count != 0:
        #     print("clustering erroneous", str((debug_clustering_errors / debug_clustering_count) * 100))
        # normalize loss debug
        if gold_clusters != None:
            coreference_loss = coreference_loss / (mentions_hidden_states.shape[0] if mentions_hidden_states.shape[0] != 0 else 1)

            # coreference_loss = coreference_loss / (len(gold_cluster_idxs) if len(gold_cluster_idxs) != 0 else 1)
        coreferences_pred = [tuple(item) for item in pred_cluster_idxs]  # if len(item) > 1]
        return coreference_loss, coreferences_pred

    # def cluster_refinement(self, lhs, pred_clusters, gold_clusters, stage):
    #     cluster_hs, cluster_am = self.get_cluster_states_matrix_lhs(self, lhs, gold_clusters)
    #     for clust_hs in cluster_hs:

    #         cluster_document_pairs = torch.cat((clust_hs, lhs), dim=0)
    #         attention_mask = torch.cat((torch.ones(lhs.shape[0], 1, device=self.model.device), cluster_am), dim=1)

    #         self.refinement_model(input_embeds= torch.cat(), attention_mask= ).logits
    #         refinement_hs = append_cluter_hs_to_lhs()

    def incremental_fixed_clustering(self, lhs, mentions_hidden_states, mentions_idxs, gold_clusters, stage):
        pred_cluster_idxs = []  # cluster_idxs = list of list of tuple of offsets (also output) up to mention_idx
        pred_cluster_hs = []
        if gold_clusters != None:
            gold_cluster_idxs = unpad_gold_clusters(gold_clusters)  # gold_cluster_idxs, but padded
        coreference_loss = torch.tensor([0.0], requires_grad=True, device=self.incremental_model.device)
        lhs = lhs[0]
        mentions_hidden_states = mentions_hidden_states[0]

        # for each mention
        for idx, (
            mention_hidden_states,
            (mention_start_idx, mention_end_idx),
        ) in enumerate(zip(mentions_hidden_states, mentions_idxs)):
            if idx == 0:
                # if first create singleton cluster
                pred_cluster_idxs.append([(mention_start_idx.item(), mention_end_idx.item())])
                pred_cluster_hs.append(mention_hidden_states.repeat(2))
                continue
            else:
                _, labels = (
                    self.new_cluster_idxs_labels((mention_start_idx, mention_end_idx), gold_cluster_idxs)
                    if stage == "train"
                    else (None, None)
                )

            loss, logits = self.fun(mention_hidden_states, pred_cluster_hs, labels)

            if stage == "train":
                logits = labels
                coreference_loss = coreference_loss + loss

            num_possible_clustering = torch.sum(torch.sigmoid(logits) > 0.5, dim=0).bool().float()

            if num_possible_clustering == 0:
                # if no clustering, create new singleton cluster
                pred_cluster_idxs.append([(mention_start_idx.item(), mention_end_idx.item())])
                pred_cluster_hs.append(mention_hidden_states.repeat(2))
            else:
                # otherwise, take most probabile clustering predicted by the model and assign this mention to that cluster
                assigned_idx = logits.argmax(axis=0).detach().cpu()
                pred_cluster_idxs[assigned_idx.item()].append((mention_start_idx.item(), mention_end_idx.item()))
                history_vector = self.fun2(mention_hidden_states, pred_cluster_hs[assigned_idx.item()])
                pred_cluster_hs[assigned_idx.item()] = torch.cat((mention_hidden_states, history_vector), dim=0)

        # normalize loss debug
        if gold_clusters != None:
            coreference_loss = coreference_loss / (len(gold_cluster_idxs) if len(gold_cluster_idxs) != 0 else 1)
        coreferences_pred = [tuple(item) for item in pred_cluster_idxs if len(item) > 1]
        return coreference_loss, coreferences_pred

    def fun(self, mention_hs, pred_cluster_hs, labels):
        loss, logits = None, None
        # repreated tensor of mention_hs, to append in first position for each possible mention cluster pair
        repeated_mention_hs = mention_hs.unsqueeze(0).repeat(len(pred_cluster_hs), 1)

        # mention cluste pairs by contatenating mention vectors to cluster padded matrix
        mention_cluster_pairs = torch.cat((repeated_mention_hs, torch.stack(pred_cluster_hs)), dim=1)

        logits = self.incremental_mention_cluster_discriminator(mention_cluster_pairs)
        """logits = torch.cat([self.softmax_dummy.to(self.model.device), logits], dim=0)  # debug
        logits = logits.squeeze(1).unsqueeze(0)"""

        loss = None
        if labels is not None:
            """labels = (
                torch.tensor([0], device=self.model.device)
                if torch.sum(labels) == 0
                else torch.arange(labels.size(0), device=self.model.device)[labels > 0] + 1
            )  # debug
            loss = torch.nn.functional.cross_entropy(logits, labels)"""
            loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels.unsqueeze(1).to(self.encoder.device))
        return loss, logits

    def fun2(self, mention_hidden_states, cluster_hidden_states):
        return self.incremental_mention_cluster_encoder(
            torch.cat(
                (
                    mention_hidden_states,
                    cluster_hidden_states[self.incremental_model_hidden_size :],
                ),
                dim=0,
            )
        )

    def get_cluster_states_matrix_lhs(self, lhs, cluster_idxs):
        # create padded matrix of encoded mentions
        max_length = max([len(x) for x in cluster_idxs])
        forward_matrix = torch.zeros(
            (len(cluster_idxs), max_length, self.incremental_model_hidden_size),
            device=self.encoder.device,
        )
        forward_am = torch.zeros((len(cluster_idxs), max_length), device=self.encoder.device)

        # for each cluster
        for idx, span_idxs in enumerate(cluster_idxs):
            # start and end idxs as tensors
            starts = torch.tensor(
                [span_idx[0] for span_idx in span_idxs],
                device=self.incremental_model.device,
            )
            ends = torch.tensor(
                [span_idx[1] for span_idx in span_idxs],
                device=self.incremental_model.device,
            )

            # start and end hidden states
            vector_starts = torch.index_select(lhs, 0, starts)
            vector_ends = torch.index_select(lhs, 0, ends)

            encoded_cluster_mentions = self.incremental_span_encoder(torch.cat((vector_starts, vector_ends), dim=-1))

            forward_matrix[idx][: len(starts)] = encoded_cluster_mentions
            forward_am[idx][: len(starts)] = torch.ones((len(starts)), device=self.encoder.device)

        return forward_matrix, forward_am

    def get_cluster_states_matrix(self, idx_to_hs, cluster_idxs, stage):
        # create padded matrix of encoded mentions
        max_length = max([len(x) for x in cluster_idxs])
        if stage == "train":
            max_length = max_length if max_length < 31 else 30
        forward_matrix = torch.zeros(
            (len(cluster_idxs), max_length, self.incremental_model_hidden_size),
            device=self.encoder.device,
        )
        forward_am = torch.zeros((len(cluster_idxs), max_length), device=self.encoder.device)

        for cluster_idx, span_idxs in enumerate(cluster_idxs):
            if stage == "train":
                if len(span_idxs) > 30:
                    # sub_list = span_idxs[1:-1]
                    span_idxs = sorted(span_idxs)
                    new_idxs = [span_idxs[0]]
                    # idx = np.round(np.linspace(0, len(sub_list) - 1, 28)).astype(int)
                    # new_idxs.extend([sub_list[i] for i in idx])
                    new_idxs.extend(random.sample(span_idxs, 28))
                    new_idxs.append(span_idxs[-1])
                    span_idxs = new_idxs

                # if len(span_idxs) > 10 and len(cluster_idxs) != 1:
                #     if random.randint(0, 99) < 5:
                #         copy = [
                #             x
                #             for idx, x in enumerate(cluster_idxs)
                #             if idx != cluster_idx
                #         ]
                #         wrong_cluster = random.sample(copy, 1)
                #         wrong_span = random.sample(wrong_cluster[0], 1)
                #         random_idx = random.randint(0, 9)
                #         span_idxs[random_idx] = wrong_span[0]
            hs = torch.stack([idx_to_hs[span_idx] for span_idx in span_idxs])

            forward_matrix[cluster_idx][: hs.shape[0]] = hs
            forward_am[cluster_idx][: hs.shape[0]] = torch.ones((hs.shape[0]), device=self.encoder.device)

        return forward_matrix, forward_am

    # takes the index of the mention (mention_start, mention_end) and gold coreferences, returns filtered indices (up to mention idx) and labels
    def new_cluster_idxs_labels(self, mention_idxs, gold_coreference_idxs):
        res_coreference_idxs = []
        # list of length number of clusters in gold, and 1.0 where the mention is laying
        labels = [
            1.0 if (mention_idxs[0].item(), mention_idxs[1].item()) in span_idx else 0.0 for span_idx in gold_coreference_idxs
        ]
        # filter cluster up to the mention you are evaluating
        for cluster_idxs in gold_coreference_idxs:
            idxs = []
            for span_idx in cluster_idxs:
                # if span is antecedent to current mention, stay in possible clusters
                if span_idx[0] < mention_idxs[0].item() or (
                    span_idx[0] == mention_idxs[0].item() and span_idx[1] < mention_idxs[1].item()
                ):
                    idxs.append((span_idx[0], span_idx[1]))
            # idxs = sorted(idxs, reverse=True)
            res_coreference_idxs.append(idxs)

        labels = torch.tensor(
            [lab for lab, idx in zip(labels, res_coreference_idxs) if len(idx) != 0],
            device=self.encoder.device,
        )
        res_coreference_idxs = [idx for idx in res_coreference_idxs if len(idx) != 0]
        return res_coreference_idxs, labels

    def forward(
        self,
        stage,
        input_ids,
        attention_mask,
        eos_mask,
        eos_indices=None,
        gold_starts=None,
        gold_mentions=None,
        gold_clusters=None,
        tokens=None,
        subtoken_map=None,
        new_token_map=None,
    ):
        last_hidden_states = self.encoder(input_ids=input_ids, attention_mask=attention_mask)["last_hidden_state"]  # B x S x TH

        lhs = last_hidden_states

        loss = torch.tensor([0.0], requires_grad=True, device=self.encoder.device)
        loss_dict = {}
        preds = {}

        (
            start_idxs,
            mention_idxs,
            start_loss,
            mention_loss,
        ) = self.squad_mention_extraction_forloop(
            lhs=last_hidden_states,
            eos_mask=eos_mask,
            gold_mentions=gold_mentions,
            gold_starts=gold_starts,
            stage=stage,
        )

        loss_dict["start_loss"] = start_loss
        preds["start_idxs"] = [start.detach().cpu() for start in start_idxs]

        loss_dict["mention_loss"] = mention_loss
        preds["mention_idxs"] = [mention.detach().cpu() for mention in mention_idxs]

        loss = loss + start_loss + mention_loss

        if stage == "train":
            mention_idxs = (gold_mentions[0] == 1).nonzero(as_tuple=False)
        else:
            mention_idxs = mention_idxs[0]

        mention_start_idxs = mention_idxs[:, 0]
        mention_end_idxs = mention_idxs[:, 1]

        mentions_start_hidden_states = torch.index_select(lhs, 1, mention_start_idxs)
        mentions_end_hidden_states = torch.index_select(lhs, 1, mention_end_idxs)

        mentions_hidden_states = torch.cat((mentions_start_hidden_states, mentions_end_hidden_states), dim=2)

        mentions_hidden_states = self.incremental_span_encoder(mentions_hidden_states)

        coreference_loss, coreferences = self.incremental_span_clustering(
            mentions_hidden_states, mention_idxs, gold_clusters, stage
        )

        loss = loss + coreference_loss
        loss_dict["coreference_loss"] = coreference_loss

        if stage != "train":
            preds["clusters"] = coreferences

        loss_dict["full_loss"] = loss
        output = {"pred_dict": preds, "loss_dict": loss_dict, "loss": loss}

        return output


def create_mention_to_antecedent(span_starts, span_ends, coref_logits):
    span_starts = span_starts.unsqueeze(0)
    span_ends = span_ends.unsqueeze(0)
    bs, n_spans, _ = coref_logits.shape

    no_ant = 1 - torch.sum(torch.sigmoid(coref_logits) > 0.5, dim=-1).bool().float()
    # [batch_size, max_k, max_k + 1]
    coref_logits = torch.cat((coref_logits, no_ant.unsqueeze(-1)), dim=-1)

    span_starts = span_starts.detach().cpu()
    span_ends = span_ends.detach().cpu()
    max_antecedents = coref_logits.argmax(axis=-1).detach().cpu()
    doc_indices = np.nonzero(max_antecedents < n_spans)[:, 0]
    # indices where antecedent is not null.
    mention_indices = np.nonzero(max_antecedents < n_spans)[:, 1]
    antecedent_indices = max_antecedents[max_antecedents < n_spans]
    span_indices = np.stack([span_starts.detach().cpu(), span_ends.detach().cpu()], axis=-1)

    mentions = span_indices[doc_indices, mention_indices]
    antecedents = span_indices[doc_indices, antecedent_indices]
    mention_to_antecedent = np.stack([mentions, antecedents], axis=1)

    if len(mentions.shape) == 1:
        mention_to_antecedent = [mention_to_antecedent]

    return doc_indices, mention_to_antecedent


def create_mention_to_antecedent_singletons(span_starts, span_ends, coref_logits):
    span_starts = span_starts.unsqueeze(0)
    span_ends = span_ends.unsqueeze(0)
    bs, n_spans, _ = coref_logits.shape

    no_ant = 1 - torch.sum(torch.sigmoid(coref_logits) > 0.5, dim=-1).bool().float()
    # [batch_size, max_k, max_k + 1]
    coref_logits = torch.cat((coref_logits, no_ant.unsqueeze(-1)), dim=-1)

    span_starts = span_starts.detach().cpu()
    span_ends = span_ends.detach().cpu()
    max_antecedents = coref_logits.argmax(axis=-1).detach().cpu()
    doc_indices = np.nonzero(max_antecedents < n_spans)[:, 0]
    # indices where antecedent is not null.
    mention_indices = np.nonzero(max_antecedents < n_spans)[:, 1]

    antecedent_indices = max_antecedents[max_antecedents < n_spans]
    span_indices = np.stack([span_starts.detach().cpu(), span_ends.detach().cpu()], axis=-1)

    mentions = span_indices[doc_indices, mention_indices]
    antecedents = span_indices[doc_indices, antecedent_indices]
    non_mentions = np.nonzero(max_antecedents == n_spans)[:, 1]

    sing_indices = np.zeros_like(len(np.setdiff1d(non_mentions, antecedent_indices)))
    singletons = span_indices[sing_indices, np.setdiff1d(non_mentions, antecedent_indices)]

    # mention_to_antecedent = np.stack([mentions, antecedents], axis=1)

    if len(mentions.shape) == 1 and len(antecedents.shape) == 1:
        mention_to_antecedent = np.stack([mentions, antecedents], axis=0)
    else:
        mention_to_antecedent = np.stack([mentions, antecedents], axis=1)

    if len(mentions.shape) == 1:
        mention_to_antecedent = [mention_to_antecedent]

    if len(singletons.shape) == 1:
        singletons = [singletons]

    return doc_indices, mention_to_antecedent, singletons


def create_clusters(m2a, singletons):
    # Note: mention_to_antecedent is a numpy array

    clusters, mention_to_cluster = [], {}
    for mention, antecedent in m2a:
        mention, antecedent = tuple(mention), tuple(antecedent)
        if antecedent in mention_to_cluster:
            cluster_idx = mention_to_cluster[antecedent]
            if mention not in clusters[cluster_idx]:
                clusters[cluster_idx].append(mention)
                mention_to_cluster[mention] = cluster_idx
        elif mention in mention_to_cluster:
            cluster_idx = mention_to_cluster[mention]
            if antecedent not in clusters[cluster_idx]:
                clusters[cluster_idx].append(antecedent)
                mention_to_cluster[antecedent] = cluster_idx
        else:
            cluster_idx = len(clusters)
            mention_to_cluster[mention] = cluster_idx
            mention_to_cluster[antecedent] = cluster_idx
            clusters.append([antecedent, mention])

    clusters = [tuple(cluster) for cluster in clusters]
    if len(singletons) != 0:
        clust = []
        while len(clusters) != 0 and len(singletons) != 0:
            if len(singletons) == 0:
                clust.append(clusters[0])
                clusters = clusters[1:]
            elif len(clusters) == 0:
                clust.append(tuple([tuple(singletons[0])]))
                singletons = singletons[1:]
            elif singletons[0][0] < sorted(clusters[0], key=lambda x: x[0])[0][0]:
                clust.append(tuple([tuple(singletons[0])]))
                singletons = singletons[1:]
            else:
                clust.append(clusters[0])
                clusters = clusters[1:]
        return clust
    return clusters


def extract_clusters(gold_clusters):
    gold_clusters = [tuple(tuple(m) for m in cluster if (-1) not in m) for cluster in gold_clusters]
    gold_clusters = [cluster for cluster in gold_clusters if len(cluster) > 0]
    return gold_clusters
