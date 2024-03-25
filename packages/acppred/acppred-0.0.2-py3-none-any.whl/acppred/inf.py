import json
import torch

from torch import nn
from torch.utils.data import DataLoader
from .util import data as Data

import copy
from attrdict import AttrDict


def predict(fasta_file, model_type="ACP_Mixed_80", device="cpu", batch_size=64):
    """
    Predict anticancer peptides for a given fasta file using a specified model.

    Parameters:
    fasta_file (str): Path to the fasta file for which the prediction is to be made.
    model_type (str, optional): Type of the model to be used for prediction. Options include "ACP_Mixed_80", "ACP2_main", "ACP2_alter", "ACP500_ACP164", "ACP500_ACP2710", and "LEE_Indep". Default is "ACP_Mixed_80".
    device (str, optional): Device to be used for prediction. It can be either "cpu" or "gpu". Default is "cpu".
    batch_size (int, optional): Number of samples per prediction. Default is 64.

    Returns:
    list: A list of lists. Each inner list contains the id, probability of ACPs, and prediction for a sample (ACP or -). For prediction "ACP", the peptide is predicted to be an anticancer peptide. For prediction "-", the peptide is predicted to be a non-anticancer peptide.
    """
    assert model_type in [
        "ACP_Mixed_80",
        "ACP2_main",
        "ACP2_alter",
        "ACP500_ACP164",
        "ACP500_ACP2710",
        "LEE_Indep",
    ], "The provided model_type is not supported."
    assert device in ["cpu", "gpu"], "The provided device is not supported."
    assert batch_size > 0, "The batch size should be greater than 0."

    args = AttrDict(
        {
            "model_type": model_type,
            "device": device,
            "batch_size": batch_size,
            "input": fasta_file,
        }
    )

    # args = arg_parser()
    model_id = f"./acppred/ckpt/{args.model_type}"
    with open(f"{model_id}_best.json", "rt") as f:
        args += json.load(f)

    if args.model_type == "ACP2_main":
        from .model_old import load_model, head, model_tot, contrastive_model
    else:
        from .model import load_model, head, model_tot, contrastive_model

    args.device = torch.device("cpu") if args.device == "cpu" else torch.device("gpu")
    args.original_AA_tok_len = copy.deepcopy(args.AA_tok_len)

    start_token = (
        True
        if ((args.model == "encoder") & (args.dataset != "ACP2_main"))
        | (args.dataset == "ACP2_alter")
        else False
    )

    if args.model_type == "ACP2_main":
        tr_file = "./acppred/dataset/ACPred-LAF/ACP2_main_train.csv"
        test_file = "./acppred/dataset/ACPred-LAF/ACP2_main_test.csv"
        max_len = (51, 50)
    elif args.model_type == "ACP2_alter":
        tr_file = "./acppred/dataset/ACPred-LAF/ACP2_alternate_train.csv"
        test_file = "./acppred/dataset/ACPred-LAF/ACP2_alternate_test.csv"
        max_len = (51, 50)
    elif args.model_type == "LEE_Indep":
        tr_file = "./acppred/dataset/ACPred-LAF/LEE_Dataset.csv"
        test_file = "./acppred/dataset/ACPred-LAF/Independent dataset.csv"
        max_len = (96, 95)
    elif args.model_type == "ACP500_ACP164":
        tr_file = "./acppred/dataset/ACPred-LAF/ACP_FL_train_500.csv"
        test_file = "./acppred/dataset/ACPred-LAF/ACP_FL_test_164.csv"
        max_len = (207, 206)
    elif args.model_type == "ACP500_ACP2710":
        tr_file = "./acppred/dataset/ACPred-LAF/ACPred-Fuse_ACP_Train500.csv"
        test_file = "./acppred/dataset/ACPred-LAF/ACPred-Fuse_ACP_Test2710.csv"
        max_len = (207, 206)
    elif args.model_type == "ACP_Mixed_80":
        tr_file = "./acppred/dataset/ACPred-LAF/ACP-Mixed-80-train.csv"
        test_file = "./acppred/dataset/ACPred-LAF/ACP-Mixed-80-test.csv"
        max_len = (208, 207)
    else:
        raise ValueError("Correct model type is not provided.")

    x_tr, y_tr, x_val, y_val = Data.raw_data_read(
        tr_file, args.val_fold, seed=args.seed
    )
    x_test, y_test = Data.raw_data_read(test_file)
    start_token = (
        True
        if ((args.model == "encoder") & (args.dataset != "ACP2_main"))
        | (args.dataset == "ACP2_alter")
        else False
    )

    data_t1 = Data.dataset((x_tr, y_tr), 1, start_token=start_token)
    data_t2 = Data.dataset((x_tr, y_tr), 2, start_token=start_token)
    data_train = Data.pretrain_dataset(data_t1, data_t2)

    data_v1 = Data.dataset((x_val, y_val), 1, start_token=start_token)
    data_v2 = Data.dataset((x_val, y_val), 2, start_token=start_token)
    data_valid = Data.pretrain_dataset(data_v1, data_v2)

    data_te1 = Data.dataset((x_test, y_test), 1, start_token=start_token)
    data_te2 = Data.dataset((x_test, y_test), 2, start_token=start_token)
    data_test = Data.pretrain_dataset(data_te1, data_te2)

    if args.model == "lstm":
        collate_fn = Data.collate_fn_lstm(args.contrastive)
        head_inp_size = args.n_hidden * 2 if args.bidirectional else args.n_hidden
    elif args.model == "encoder":
        collate_fn = Data.collate_fn_encoder(args.contrastive)
        head_inp_size = args.emb_dim
    elif args.model == "cnn1d":
        collate_fn = Data.collate_fn_cnn(max_len, args.contrastive)
        head_inp_size = args.channels[-1]

    ## inference fasta read
    inf_data = Data.raw_data_read_fasta(args.input)

    # sequence length check
    for seq, id in zip(inf_data[0], inf_data[2]):
        assert (
            len(seq) < max_len[0]
        ), f"Sequence {id} exceeds maximum input sequence length (Maximum sequence length is {max_len[0]-1})"

    data_inf1 = Data.dataset((inf_data[0], inf_data[1]), 1, start_token=start_token)
    data_inf2 = Data.dataset((inf_data[0], inf_data[1]), 2, start_token=start_token)
    data_inf = Data.pretrain_dataset(data_inf1, data_inf2)
    inference_loader = DataLoader(
        data_inf, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn
    )
    inference_loader = Data.device_DataLoader(
        inference_loader, args.device, args.contrastive
    )

    ## model load
    if args.original_AA_tok_len == 1:
        args.AA_tok_len = 1
        args.vocab_size = data_t1.vocab_size()
        l_feature1 = load_model(args.model)(**args)
        l_proj1 = head(
            inp_size=head_inp_size,
            output_size=head_inp_size / 4,
            hidden=[head_inp_size / 2],
        )
        l_lin_head1 = head(inp_size=head_inp_size, output_size=2)
        classifier = model_tot(
            feat=l_feature1, linear_head=l_lin_head1, projector=l_proj1
        )

        classifier.load_state_dict(
            torch.load(f"{model_id}_best.pt", map_location=args.device)
        )
        args.model_id = 0
    else:
        args.AA_tok_len = 2
        args.vocab_size = data_t2.vocab_size()
        l_feature2 = load_model(args.model)(**args)
        l_proj2 = head(
            inp_size=head_inp_size,
            output_size=head_inp_size / 4,
            hidden=[head_inp_size / 2],
        )
        l_lin_head2 = head(inp_size=head_inp_size, output_size=2)
        classifier = model_tot(
            feat=l_feature2, linear_head=l_lin_head2, projector=l_proj2
        )

        classifier.load_state_dict(
            torch.load(f"{model_id}_best.pt", map_location=args.device)
        )
        args.model_id = 1

    classifier.eval()
    with torch.no_grad():
        for i, batch in enumerate(inference_loader):
            logit = classifier(batch[args.model_id])["lin_head"].squeeze()
            pred = torch.argmax(logit, dim=1).squeeze()

            if i == 0:
                pred_total = torch.argmax(logit, dim=1).squeeze()
                logit_prob = nn.Softmax(1)(logit)[:, 1]
            else:
                pred_total = torch.concat(
                    [pred_total, torch.argmax(logit, dim=1).squeeze()]
                )
                logit_prob = torch.concat([logit_prob, nn.Softmax(1)(logit)[:, 1]])
    return_res = []
    for id, logit, pred in zip(inf_data[2], logit_prob, pred_total):
        _pred = "ACP" if pred == 1 else "-"
        return_res.append([id, logit.item(), _pred])
    return return_res
