# imports
import os
import subprocess as sp 
from platform import system
import warnings
import numpy as np
import torch as tr
import pandas as pd

from sincfold.embeddings import NT_DICT
from sincfold import __path__ as sincfold_path
from sincfold.embeddings import NT_DICT, VOCABULARY


CT2DOT_CALL = f"export DATAPATH={sincfold_path[0]}/tools/RNAstructure/data_tables; {sincfold_path[0]}/tools/RNAstructure/ct2dot"
DRAW_CALL = f"export DATAPATH={sincfold_path[0]}/tools/RNAstructure/data_tables;  {sincfold_path[0]}/tools/RNAstructure/draw -c -u --svg -n 1"
VARNA_PATH = f"{sincfold_path[0]}/tools/varna/VARNAv3-93.jar"
if system() == "Windows":
    VARNA_PATH = ""
    CT2DOT_CALL = ""
    DRAW_CALL = ""

# All possible matching brackets for base pairing
MATCHING_BRACKETS = [
    ["(", ")"],
    ["[", "]"],
    ["{", "}"],
    ["<", ">"],
    ["A", "a"],
    ["B", "a"],
]
# Normalization.
BRACKET_DICT = {"!": "A", "?": "a", "C": "B", "D": "b"}


def pair_strength(pair):
    if "G" in pair and "C" in pair:
        return 3
    if "A" in pair and "U" in pair:
        return 2
    if "G" in pair and "U" in pair:
        return 0.8

    if pair[0] in NT_DICT and pair[1] in NT_DICT:
        n0, n1 = NT_DICT[pair[0]], NT_DICT[pair[1]]
        # Possible pairs with other bases
        if ("G" in n0 and "C" in n1) or ("C" in n0 and "G" in n1):
            return 3
        if ("A" in n0 and "U" in n1) or ("U" in n0 and "A" in n1):
            return 2
        if ("G" in n0 and "U" in n1) or ("U" in n0 and "G" in n1):
            return 0.8

    return 0


def prob_mat(seq):
    """Receive sequence and compute local conection probabilities (Ufold paper, optimized version)"""
    Kadd = 30
    window = 3
    N = len(seq)

    mat = np.zeros((N, N), dtype=np.float32)

    L = np.arange(N)
    pairs = np.array(np.meshgrid(L, L)).T.reshape(-1, 2)
    pairs = pairs[np.abs(pairs[:, 0] - pairs[:, 1]) > window, :]

    for i, j in pairs:
        coefficient = 0
        for add in range(Kadd):
            if (i - add >= 0) and (j + add < N):
                score = pair_strength((seq[i - add], seq[j + add]))
                if score == 0:
                    break
                else:
                    coefficient += score * np.exp(-0.5 * (add**2))
            else:
                break
        if coefficient > 0:
            for add in range(1, Kadd):
                if (i + add < N) and (j - add >= 0):
                    score = pair_strength((seq[i + add], seq[j - add]))
                    if score == 0:
                        break
                    else:
                        coefficient += score * np.exp(-0.5 * (add**2))
                else:
                    break

        mat[i, j] = coefficient

    return tr.tensor(mat)


def valid_mask(seq):
    """Create a NxN mask with valid canonic pairings."""

    seq = seq.upper().replace("T", "U")  # rna
    mask = tr.zeros((len(seq), len(seq)), dtype=tr.float32)
    for i in range(len(seq)):
        for j in range(len(seq)):
            if np.abs(i - j) > 3:  # nt that are too close are invalid
                if pair_strength([seq[i], seq[j]]) > 0:
                    mask[i, j] = 1
                    mask[j, i] = 1
    return mask


def normalize_brackets(struct):
    """Unify bracket notation"""
    for b in BRACKET_DICT:
        struct = struct.replace(b, BRACKET_DICT[b])
    return struct


def bracket_match(struct):
    match = True
    for pair in MATCHING_BRACKETS:
        match = match & (struct.count(pair[0]) == struct.count(pair[1]))
    return match


def fold2bp(struc, xop="(", xcl=")"):
    """Get base pairs from one page folding (using only one type of brackets).
    BP are 1-indexed"""
    openxs = []
    bps = []
    if struc.count(xop) != struc.count(xcl):
        return False
    for i, x in enumerate(struc):
        if x == xop:
            openxs.append(i)
        elif x == xcl:
            if len(openxs) > 0:
                bps.append([openxs.pop() + 1, i + 1])
            else:
                return False
    return bps


def dot2bp(struc):
    bp = []
    if not set(struc).issubset(
        set(["."] + [c for par in MATCHING_BRACKETS for c in par])
    ):
        return False

    for brackets in MATCHING_BRACKETS:
        if brackets[0] in struc:
            bpk = fold2bp(struc, brackets[0], brackets[1])
            if bpk:
                bp = bp + bpk
            else:
                return False
    return list(sorted(bp))


def dot2matrix(dot):
    matrix = tr.zeros((len(dot), len(dot)))
    base_pairs = dot2bp(dot)

    for bp in base_pairs:
        # base pairs are 1-based
        matrix[bp[0] - 1, bp[1] - 1] = 1
        matrix[bp[1] - 1, bp[0] - 1] = 1

    return matrix


def bp2matrix(L, base_pairs):
    matrix = tr.zeros((L, L))

    for bp in base_pairs:
        # base pairs are 1-based
        matrix[bp[0] - 1, bp[1] - 1] = 1
        matrix[bp[1] - 1, bp[0] - 1] = 1

    return matrix


def read_ct(ctfile):
    """Read ct file, return sequence and base_pairs"""
    seq, bp = [], []
    
    k = 1
    for p, line in enumerate(open(ctfile)):
        if p == 0:
            try:
                seq_len = int(line.split()[0])
            except ValueError:
                # >seq length: N extra info
                if line.split(":")[0] == ">seq length":
                    seq_len = int(line.split(":")[1].split()[0])
            
            continue 

        if line[0] == "#" or len(line.strip()) == 0:
            # comment
            continue

        line = line.split()
        if len(line) != 6 or not line[0].isnumeric() or not line[4].isnumeric:
            # header
            continue

        n1, n2 = int(line[0]), int(line[4])
        if k != n1: # add missing nucleotides as N
            seq += ["N"] * (n1-k)
        seq.append(line[1])
        k = len(seq) + 1
        if n2 > 0 and (n1 < n2):
            bp.append([n1, n2])

    assert len(seq) == seq_len, f"ct file format error\n{seq_len}\n{seq}\n{len(seq)}"
    return "".join(seq), bp


def write_ct(fname, seqid, seq, base_pairs):
    """Write ct file from sequence and base pairs. Base_pairs should be 1-based and unique per nt"""
    base_pairs_dict = {}
    for bp in base_pairs:
        base_pairs_dict[bp[0]] = bp[1]
        base_pairs_dict[bp[1]] = bp[0]

    with open(fname, "w") as fout:
        fout.write(f"{len(seq)} {seqid}\n")
        for k, n in enumerate(seq):
            fout.write(f"{k+1} {n} {k} {k+2} {base_pairs_dict.get(k+1, 0)} {k+1}\n")


def split_fasta_rec(s, mfe=True):
    """This assume the format of the fasta record is AACCGGUU((....))(-1.2), where the last 
    parenthesis part is optional (mfe)"""
    s = s.strip()
    mfe_start = s.rfind("(")

    if mfe:
        mfe = float(s[mfe_start + 1 : -1])
    s = s[:mfe_start].strip()

    seq = s[: len(s) // 2]
    struct = s[len(s) // 2 :]
    
    assert len(seq) == len(struct), "Sequence and structure have different lengths"

    return seq, struct, mfe


def mat2bp(x):
    """Get base-pairs from conection matrix [N, N]. It uses upper
    triangular matrix only, without the diagonal. Positions are 1-based. """
    ind = tr.triu_indices(x.shape[0], x.shape[1], offset=1)
    pairs_ind = tr.where(x[ind[0], ind[1]] > 0)[0]

    pairs_ind = ind[:, pairs_ind].T
    # remove multiplets pairs
    multiplets = []
    for i, j in pairs_ind:
        ind = tr.where(pairs_ind[:, 1]==i)[0]
        if len(ind)>0:
            pairs = [bp.tolist() for bp in pairs_ind[ind]] + [[i.item(), j.item()]]
            best_pair = tr.tensor([x[bp[0], bp[1]] for bp in pairs]).argmax()
                
            multiplets += [pairs[k] for k in range(len(pairs)) if k!=best_pair]   
            
    pairs_ind = [[bp[0]+1, bp[1]+1] for bp in pairs_ind.tolist() if bp not in multiplets]
 
    return pairs_ind


def postprocessing(preds, masks):
    """Postprocessing function using viable pairing mask.
    Inputs are batches of size [B, N, N]"""
    if masks is not None:
        preds = preds.multiply(masks)

    y_pred_mask_triu = tr.triu(preds)
    y_pred_mask_max = tr.zeros_like(preds)
    for k in range(preds.shape[0]):
        y_pred_mask_max_aux = tr.zeros_like(y_pred_mask_triu[k, :, :])

        val, ind = y_pred_mask_triu[k, :, :].max(dim=0)
        y_pred_mask_max[k, ind[val > 0], val > 0] = val[val > 0]

        val, ind = y_pred_mask_max[k, :, :].max(dim=1)
        y_pred_mask_max_aux[val > 0, ind[val > 0]] = val[val > 0]

        ind = tr.where(y_pred_mask_max[k, :, :] != y_pred_mask_max_aux)
        y_pred_mask_max[k, ind[0], ind[1]] = 0

        y_pred_mask_max[k] = tr.triu(y_pred_mask_max[k]) + tr.triu(
            y_pred_mask_max[k]
        ).transpose(0, 1)
    return y_pred_mask_max

def find_pseudoknots(base_pairs):
    pseudoknots = []
    for i, j in base_pairs:
        for k, l in base_pairs:
            if i < k < j < l:  # pseudoknot definition
                if [k, l] not in pseudoknots:
                    pseudoknots.append([k, l])
    return pseudoknots

def dot2png(png_file, sequence, dotbracket, resolution=10):

    try:
        sp.run("java -version", shell=True, check=True, capture_output=True)
        sp.run(f'java -cp {VARNA_PATH} fr.orsay.lri.varna.applications.VARNAcmd -sequenceDBN {sequence} -structureDBN "{dotbracket}" -o  {png_file} -resolution {resolution}', shell=True)
    except:
        warnings.warn("Java Runtime Environment failed trying to run VARNA. Check if it is installed.")
    
    
def ct2svg(ct_file, svg_file):
    
    sp.run(f'{DRAW_CALL} {ct_file} {svg_file}', shell=True, capture_output=True)


def ct2dot(ct_file):
    if not os.path.isfile(ct_file) or os.path.splitext(ct_file)[1] != ".ct":
        raise ValueError("ct2dot requires a .ct file")
    dotbracket = ""
    if CT2DOT_CALL:
        sp.run(f"{CT2DOT_CALL} {ct_file} 1 tmp.dot", shell=True, capture_output=True)
        try: 
            dotbracket = open("tmp.dot").readlines()[2].strip()
            os.remove("tmp.dot")
        except FileNotFoundError: 
            print("Error in ct2dot: check .ct file")
    else:
        print("Dotbracket conversion only available on linux")
    return dotbracket


def valid_sequence(seq):
    """Check if sequence is valid"""
    return set(seq.upper()) <= (set(NT_DICT.keys()).union(set(VOCABULARY)))

def validate_file(pred_file):
    """Validate input file fasta/csv format and return csv file"""
    if os.path.splitext(pred_file)[1] == ".fasta":
        table = []
        with open(pred_file) as f:
            row = [] # id, seq, (optionally) struct
            for line in f:
                if line.startswith(">"):
                    if row:
                        table.append(row)
                        row = []
                    row.append(line[1:].strip())
                else:
                    if len(row) == 1: # then is seq
                        row.append(line.strip())
                        if not valid_sequence(row[-1]):
                            raise ValueError(f"Sequence {row.upper()} contains invalid characters")
                    else: # struct
                        row.append(line.strip()[:len(row[1])]) # some fasta formats have extra information in the structure line
        if row:
            table.append(row)
        
        pred_file = pred_file.replace(".fasta", ".csv")
        
        if len(table[-1]) == 2:
            columns = ["id", "sequence"]
        else:
            columns = ["id", "sequence", "dotbracket"]

        pd.DataFrame(table, columns=columns).to_csv(pred_file, index=False)

    elif os.path.splitext(pred_file)[1] != ".csv":
        raise ValueError("Predicting from a file with format different from .csv or .fasta is not supported")
    
    return pred_file 

def validate_canonical(sequence, base_pairs):
    if not valid_sequence(sequence):
        return False, "Invalid sequence"

    for i, j in base_pairs:
        nt1, nt2 = sequence[i-1], sequence[j-1]
        if pair_strength((nt1, nt2))==0:
            return False, f"Invalid base pair: {nt1} {nt2}"

        for k, l in base_pairs:
            if (k, l) != (i, j):
                if i in (k, l):
                    return False, f"Nucleotide {i} is in pair {i, j} and {k, l}"
                if j in (k, l):
                    return False, f"Nucleotide {j} is in pair {i, j} and {k, l}"

    return True, ""