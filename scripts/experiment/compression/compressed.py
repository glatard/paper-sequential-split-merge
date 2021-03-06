#!/usr/bin/env python
# Ref: imageutils.py from
# https://github.com/big-data-lab-team/sam/blob/master/imageutils.py
import imageutils as img_utils
import numpy as np
from time import time
import argparse
import random
import os

# example
# ./compressed.py -m 3221225472 6442450944 9663676416 12884901888 17179869184 -r 2 -d ssd
# ./compressed.py -m 3221225472 9663676416 -r 5 -d hdd


# on the consider
reconstructed_hdd = "/data/gao/new_image.nii.gz"
legend_hdd = "/data/gao/blocks_split/legend.txt"

reconstructed_ssd = "/home/gao/new_image.nii.gz"
legend_ssd = "/home/gao/blocks125/legend.txt"


csv_file_hdd_mreads = "./mreads_hdd_compressed.dat"
csv_file_hdd_creads = "./creads_hdd_compressed.dat"
csv_file_ssd_mreads = "./mreads_ssd_compressed.dat"
csv_file_ssd_creads = "./creads_ssd_compressed.dat"


first_dim=3850
second_dim=3025
third_dim=3500

files = {
    "hdd": (reconstructed_hdd, legend_hdd, csv_file_hdd_mreads, csv_file_hdd_creads),
    "ssd": (reconstructed_ssd, legend_ssd, csv_file_ssd_mreads, csv_file_ssd_creads)
}

def benchmark_mreads(mem, reconstructed, legend):
    img = img_utils.ImageUtils(reconstructed, first_dim, second_dim, third_dim, np.uint16)
    s_time = time()
    total_read_time, total_write_time, total_seek_time, total_seek_number = img.reconstruct_img(legend, "multiple", mem, input_compressed=True, benchmark=True)
    total_time = time() - s_time
    print total_read_time, total_write_time, total_seek_time, total_seek_number, total_time
    return (total_read_time, total_write_time, total_seek_time, total_seek_number, total_time)


def benchmark_creads(mem, reconstructed, legend):
    img = img_utils.ImageUtils(reconstructed, first_dim, second_dim, third_dim, np.uint16)
    s_time = time()
    total_read_time, total_write_time, total_seek_time, total_seek_number = img.reconstruct_img(legend, "clustered", mem, input_compressed=True, benchmark=True)
    total_time = time() - s_time
    print total_read_time, total_write_time, total_seek_time, total_seek_number, total_time
    return (total_read_time, total_write_time, total_seek_time, total_seek_number, total_time)

def write_to_file(data_dict, dat_file):
    # (total_read_time, total_write_time, total_seek_time, total_seek_number, total_time)
    print "saved to ", dat_file
    with open(dat_file, "a") as f:
        for k in sorted(data_dict.keys()):
            for e in data_dict[k]:
                f.write(str(e) + " ")
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description='Bechmark for mulitiple reads')
    parser.add_argument('-m', '--mem', nargs='+', type=int, help="mem in bytes. A list of mems is required", required=True)
    parser.add_argument('-r', '--rep', type=int, help="how many repetitions on each mem", required=True)
    parser.add_argument('-d', '--disk', choices=['ssd', 'hdd'], help="running on hdd or ssd", required=True)
    args = parser.parse_args()

    mem_list = args.mem
    rep = args.rep
    disk = args.disk

    ## MREADS:
    for i in range(0, rep):
        data_dict = {}
        print "Repetition: {}".format(i)
        random.shuffle(mem_list)
        for mem in mem_list:
            print "mem = {}".format(mem)
            os.system("echo 3 | sudo tee /proc/sys/vm/drop_caches")
            os.system("rm {}".format(files[disk][0]))
            data = benchmark_mreads(mem=mem, reconstructed=files[disk][0], legend=files[disk][1])
            data_dict[mem] = data
        write_to_file(data_dict, files[disk][2])



    ## CREADS:
    for i in range(0, rep):
        data_dict = {}
        print "Repetition: {}".format(i)
        random.shuffle(mem_list)
        for mem in mem_list:
            print "mem = {}".format(mem)
            os.system("echo 3 | sudo tee /proc/sys/vm/drop_caches")
            os.system("rm {}".format(files[disk][0]))
            data = benchmark_creads(mem=mem, reconstructed=files[disk][0], legend=files[disk][1])
            data_dict[mem] = data
        write_to_file(data_dict, files[disk][3])

if __name__ == '__main__':
    main()
