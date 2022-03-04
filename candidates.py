"""
Submit a position weight matirx of peptide binders of any peptide recognition modules
to scan it against a given protein database.

The signature sequences and the number of results are displayed in the terminal. A CSV
file consists of names, Uniprot id and the position of signature sequences of the
protein candiates is exported.

To achieve a unique code for your database, submit it on Scanprosite Tool (https://prosite.expasy.org/scanprosite/).
The code lasts for a month.

To customize the script, replace userdbcode in scanprosite_request (line 31) with your own and the Position Weight
Matrix name in candidates (line 87)

"""

import pandas as pd
import numpy as np
import importlib
import scanprosite_request
importlib.reload(scanprosite_request)
from scanprosite_request import rrrrequest

"""
Generate signature sequence by significance

"""


def generate_sigseq(start, end, max_ids, new_max=0):
    if new_max != 0:
        new_max = min([4, new_max])
        sigseq = ''
        for z in z_score[start:end + 1]:
            if z >= new_max:
                sigseq += max_ids[z_score.index(z)] + '-'
                z_score_tmp[z_score.index(z)] = 0
            else:
                sigseq += 'x-'
        sigseq = sigseq[:-1]
    else:
        sigseq = ''
        for z in z_score[start:end + 1]:
            if z >= 4:
                sigseq += max_ids[z_score.index(z)] + '-'
                z_score_tmp[z_score.index(z)] = 0
            else:
                sigseq += 'x-'
        sigseq = sigseq[:-1]
    return sigseq


def save_csv(table, name):
    with open(name, 'w') as csv:
        # species = []
        table.sort(key=lambda x: x[x.index('_') + 1:x.index('_') + 10])
        for line in table:
            line = line.replace('\t', ',')
            # sp = line[line.index('_')+1:line.index(',')]
            # if sp not in species:
            # species.append(sp)
            # csv.writelines(f'{sp}\n')
            csv.writelines(f'{line}\n')


# save_csv(table,name)

def mod_csv(name, s, e, l):
    df = pd.read_csv(name, names=['Candiates', 'Left', 'Right', 'Userpat', 'E', 'F', 'G', 'Signature Sequence'])
    del df['Userpat'], df['E'], df['F'], df['G']
    df['Start'] = [s for index in range(len(df))]
    df['End'] = [e for index in range(len(df))]
    df['Binder length'] = [l for index in range(len(df))]
    df['Species'] = df['Candiates']
    for i in range(len(df)):
        df['Species'][i] = df['Species'][i].split('_')[1]
    df.set_index(['Species'])
    df.to_csv(f'{name[0:-4]} EXPORT.csv')


"""
Using pandas to read CSV files

"""
# Replace PRM_0226_1.dat with your position weight matrix file

dat_file_name = 'PRM_0206.dat'

with open(dat_file_name, 'r') as f:
    raw_file_lines = f.readlines()
    with open('temp.dat', 'w') as f2:
        f2.writelines(raw_file_lines[1:])

df = pd.read_csv('temp.dat', header=None, sep='\t')
df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
df = df.set_index(0, drop=True, append=False, inplace=False, verify_integrity=False)  # Set the aacs as index in CSV

"""
Calculation

"""
# The maximum weight at each position and the corresponding amino acid.
maxs = list(df.max())
max_ids = list(df.idxmax())

# The standard deviation of each column
stds = []
for col in df.columns:
    stds.append(
        df[col].std(ddof=0))  # In pandas, ddof must be set at 0, or the index col will be included in std processing

# Z-score of the maximum at each position, which is used to compare the significance of each position
z_score = []
for flag in range(len(stds)):
    z_score.append((maxs[flag] - 1) / stds[flag])

z_score_tmp = z_score.copy()


def first(the_iterable, condition=lambda x: True):
    for i in the_iterable:
        if condition(i):
            return i


start = z_score.index(first(z_score, lambda i: i > 4))

for data in z_score:
    if data > 4:
        end = z_score.index(data)

SigSeq = generate_sigseq(start, end, max_ids)
remark, hits, table = rrrrequest(SigSeq)

print(f'{remark} {hits}\n')
n_search = 1

species = []
save_csv(table, f'{dat_file_name[:-4]} #{n_search} {SigSeq}.csv')
mod_csv(f'{dat_file_name[:-4]} #{n_search} {SigSeq}.csv', start + 1, end + 1, len(df.columns))

while hits > 5 and hits != 0:
    new_max = max(z_score_tmp)
    if z_score.index(max(z_score_tmp)) < start:
        start = z_score.index(max(z_score_tmp))
    if z_score.index(max(z_score_tmp)) > end:
        end = z_score.index(max(z_score_tmp))
    SigSeq = generate_sigseq(start, end, max_ids, new_max)
    remark, hits, table = rrrrequest(SigSeq)
    if hits != 0:
        print(f'{remark} {hits}\n')
        n_search += 1
        save_csv(table, f'{dat_file_name[:-4]} #{n_search} {SigSeq}.csv')
        mod_csv(f'{dat_file_name[:-4]} #{n_search} {SigSeq}.csv', start + 1, end + 1, len(df.columns))
print(f'--End of Search--')
