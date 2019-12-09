import networkx as nx
import matplotlib.pyplot as plt


def main():

    friend_adj = 'friendship_adj_list.adjlist'
    power_adj = 'power_adj_list.adjlist'
    metadata = 'PINS_Schneider_Data.csv'

    f_adj_dictionary = read_adj_file(friend_adj)
    f_meta_dictionary = add_meta_data(metadata, f_adj_dictionary)

    p_adj_dictionary = read_adj_file(power_adj)
    p_meta_dictionary = add_meta_data(metadata, p_adj_dictionary)

    make_metadata_file(f_meta_dictionary, 'friendship')
    make_metadata_file(p_meta_dictionary, 'power')



def read_adj_file(file_name):
    adj_file = open(file_name)

    metadata_dictionary = {}
    for line in adj_file:
        A = line.rstrip().split()
        for i in range(len(A)):
            if i == 0: metadata_dictionary[A[0]] = []
            #else: metadata_dictionary[A[0]][0].append(A[i])
    adj_file.close()
    return metadata_dictionary


def add_meta_data(file_name, metadata_dictionary):

    m_file = open(file_name)
    header = None
    for line in m_file:
        A = line.rstrip().split(',')
        if header == None: header = A
        else:
            metadata_dictionary[A[0]].append(A[1])
            metadata_dictionary[A[0]].append(A[2].split()[0])
            metadata_dictionary[A[0]].append(A[3])

    return metadata_dictionary


def make_metadata_file(m_dict, title):

    meta_data_txt = open(title+'_metadata.txt', 'w')
    for m in m_dict.keys():
        meta_data_txt.write(m + '\t')
        for i in m_dict[m]:
            meta_data_txt.write(str(i) + '\t')
            #meta_data_txt.write('\t')
        meta_data_txt.write('\n')


main()