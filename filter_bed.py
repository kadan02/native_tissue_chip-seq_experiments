import csv
import os


srx_ids = set()
ignored_lines = [] # debug

with open('chip_atlas/native_chip_atlas_experiments.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        srx_ids.add(row['Experiment ID'])

input_dir = "bed/"
input_bed_file = input("Input bed file: ")
tissue = input_bed_file[4:7]

if not os.path.exists("bed/" + tissue):
    os.makedirs("bed/" + tissue)

output_path = "bed/" + tissue + "/filtered_" + tissue + ".bed"

id_counter = {}
with open(input_dir + input_bed_file, 'r', encoding="UTF-8") as input_path, open(output_path, 'w') as output:
    for line in input_path:
        id_start = line.find('ID=') + 3
        id_end = line.find(';', id_start)
        srx_id = line[id_start:id_end]

        if srx_id in srx_ids:
            # addicionális ID generálása az SRA ID után (run-onként eggyel növekvő szám)
            if srx_id not in id_counter:
                id_counter[srx_id] = 1
            else:
                id_counter[srx_id] += 1
            unique_id = f"{srx_id}_{id_counter[srx_id]}"

            # oszlopok: chr start end id
            columns = line.split('\t')
            chr_info = f"{columns[0]}\t{columns[1]}\t{columns[2]}\t{unique_id}"
            output.write(chr_info + '\n')
        else:
            ignored_lines.append(srx_id)

with open('log/ignored_lines_' + tissue + ".log", 'w') as log_file:
    log_file.write('\n'.join(ignored_lines))