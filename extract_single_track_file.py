import argparse
import os

import numpy as np


def extract_single_track_file(
        in_filename: str,
        out_filename: str,
        track_number: int):
    """特定のトラックのファイルの一覧を作成する．

    Args:
        in_filename (str): input file path(npy path for each line)
        out_filename (str): output file path
        track_number (int): target track number
    """
    with open(in_filename, 'r') as f:
        files = f.readlines()
    # remove "\n"
    files = tuple(map(lambda x: x.replace('\n', ""), files))

    # check out_filename exist
    if (os.path.exists(out_filename)):
        while True:
            answer = input("output file is already exists. overwrite? (y/n): ")
            if (answer == "y"):
                break
            elif (answer == "n"):
                print("exit")
                exit()
            else:
                print("type y/n")
    f = open(out_filename, "w")
    for file in files:
        npy = np.load(file)

        target_pianoroll = npy[..., track_number]
        target_pianoroll = target_pianoroll != 0
        # check whether pianoroll is suitable for single track dataset
        # conditions:
        # - each measures contains N different pitches
        # - percentage of rest duration in all measures is less than N
        n_different_pitches = 4
        n_percentage__rest = 0.5
        condition = True
        if (
            # condition 1
            np.any(n_different_pitches > np.count_nonzero(
                np.sum(target_pianoroll, axis=1), axis=1)) or
            # condition 2
            np.any(n_percentage__rest > np.mean(
                np.sum(target_pianoroll, axis=2) != 0, axis=1))
        ):
            condition = False

        if (condition):
            f.write(file)
            f.write("\n")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True)
    parser.add_argument("-t", "--track_number", type=int, required=True)
    args = parser.parse_args()

    extract_single_track_file(args.input, args.output, args.track_number)
