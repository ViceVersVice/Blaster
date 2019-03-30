from pyunpack import Archive
import os
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import subprocess
import re
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast import NCBIXML
from Bio import SearchIO
from contextlib import redirect_stdout
import xlsxwriter
from Bio import Entrez
import magic

class blaster_tool():

    def __init__(self, id_num=None, query_name=None, task="megablast",
                 sort_by="query_start", sort_horizontal=None, min_coverage=0,
                 min_identity=0, max_leng=999999999999999, min_leng=0):
        self.id_num = id_num
        self.query_name = query_name
        self.min_coverage = min_coverage
        self.min_identity = min_identity
        self.max_leng = max_leng
        self.min_leng = min_leng
        self.task = task
        self.sort_by = sort_by
        self.sort_horizontal = sort_horizontal

    def create_id_folder(self):
        os.mkdir("{0}\\subfolder".format(self.id_num))

    def db_blast(self):
        for root, dirs, files in os.walk("{0}\\sequences".format(self.id_num)):
            for name in files:
                if name.endswith('.fna') or name.endswith('.fasta') or name.endswith('.ffn'):
                    pathname = os.path.join(root, name)
                    file_name = os.path.splitext(name)[0]

                    blastdb_cmd = 'makeblastdb -in {0} -dbtype nucl -title {1}'.format(pathname, file_name)
                    process = subprocess.Popen(blastdb_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=False)
                    (out, err) = process.communicate()
                    #print(out, err)
                    blast_cmd = "blastn -db {0} -query {1} -task {2} -outfmt 5 -out {3}".format(pathname, "{0}\\{1}".format(self.id_num, self.query_name),
                                                                                                self.task, "{0}\\subfolder\\{1}.xml".format(self.id_num, file_name))
                    processblast = subprocess.Popen(blast_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=False)
                    (out, err) = processblast.communicate()
                    #print(out, err)
    ##Check extension, mimetype and unpack+check
    def unpack_sequences(self):
        allowed_mimes = ["text/plain", "application/zip",
                         "application/x-tar", "application/x-gzip"]
        allowed_extensions = [".zip", ".tar", ".gz", ".fasta", ".ffn", ".fna"]
        for root, dirs, files in os.walk("{0}\\sequences".format(self.id_num)):
            for name in files:
                pathname = os.path.join(root, name)
                extension = os.path.splitext(name)[1]
                tested_file_mime = magic.from_file(pathname, mime=True)
                #print(name)
                if extension in allowed_extensions and tested_file_mime in allowed_mimes:
                    if extension in [".zip", ".tar", ".gz"]:
                        Archive(pathname, backend="patool").extractall(root)
                        os.remove(pathname)
                        self.unpack_sequences()
                        break
                else:
                    os.remove(pathname)
                    continue

    def multi_multi(self, path_record=None):
        x = 0
        workbook = xlsxwriter.Workbook('{0}\\output.xlsx'.format(self.id_num))
        worksheet = workbook.add_worksheet()
        second_sequence = SeqIO.parse(path_record, "fasta")
        col = 0
        for sequence in second_sequence:
            with open('{0}\subfolder\sequence.fasta'.format(self.id_num), 'w+') as f:
                f.write(">%s \n" % sequence.description)
                f.write(str(sequence.seq))

            blastdb_cmd = 'makeblastdb -in {0} -dbtype nucl -title {1}'.format("{0}\\subfolder\\sequence.fasta".format(self.id_num),  "sequence")
            process = subprocess.Popen(blastdb_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=False)
            (out, err) = process.communicate()
            #print(out, err)
            b1 = NcbiblastnCommandline(query="{0}\\{1}".format(self.id_num, self.query_name),
                                       task=self.task,
                                       db='{0}\subfolder\sequence.fasta'.format(self.id_num),
                                       outfmt=5,
                                       out="{0}\\subfolder\\out.xml".format(self.id_num))
            stdout, stderr = b1()
            #print(stdout, stderr)
            col += 1
            worksheet.write(0, col, sequence.description)
            result = SearchIO.parse("{0}\\subfolder\\out.xml".format(self.id_num), "blast-xml")
            row = 1
            for hits in result:
                hit_names = []
                # if len(hits) < 1:
                #     hit_names.append(0)
                #     continue
                worksheet.write(row, 0, hits.id)

                for hit in hits:
                    for data in hit:
                        score = data.bitscore
                        query_start = data.query_start
                        subject_start = data.hit_start
                        e_value = data.evalue
                        if data.aln_span/hits.seq_len > 1:
                            coverage = 100
                        else:
                            coverage = "%.2f" % ((data.aln_span/hits.seq_len) * 100)
                        identity = "%.2f" % ((data.ident_num/data.aln_span) * 100)

                        position = str(data.hit_start + 1) + ":" + str(data.hit_end)
                        leng = data.hit_end - data.hit_start
                        if float(coverage) < self.min_coverage or float(identity) < self.min_identity or leng < self.min_leng or leng > self.max_leng:
                            continue
                        else:
                            hit_description = "COV {0}%, IDENT {1}%, SCORE {2}, POSITION {3}, LENGTH {4}".format(coverage, identity, score, position, leng)
                            hit_values = {"score": score, "e_value": e_value, "coverage": coverage, "identity": identity, "query_start": query_start, "subject_start": subject_start}
                            hit_data = [hit_description, hit_values]
                            hit_names.append(hit_data)
                #print(len(hit_names))
                if len(hit_names) < 1:
                    worksheet.write(row, col, 0)
                    row +=1
                    continue
                    #sorted_hit_names = [[0, 0]]
                elif self.sort_by == "query_start" or self.sort_by == "subject_start":
                    sorted_hit_names = sorted(hit_names, key=self.by_value, reverse=False)
                else:
                    sorted_hit_names = sorted(hit_names, key=self.by_value, reverse=True)
                    #print(sorted_hit_names)
                #num = 0
                cell_output = ""
                for count, hit_data in enumerate(sorted_hit_names, start=1):
                    hit_description = hit_data[0]
                    hit_output = str(count) + ")" + hit_description + "\n"
                    cell_output += hit_output
                worksheet.write(row, col, cell_output)
                row += 1
        workbook.close()

    def by_value(self, value):
        if value != 0:
            hit_value = value[1]
            return float(hit_value[self.sort_by])
        else:
            return 0

    def by_value_points(self, value):
        return float(value[1])

    def make_excel(self):
        file_count = 0
        for root, dirs, files in os.walk("{0}\\sequences".format(self.id_num)):
            for name in files:
                if name.endswith('.ffn') or name.endswith('.fasta') or name.endswith('.fna'):
                    file_count += 1
                    pathname = os.path.join(root, name)
        if file_count == 1:
            self.multi_multi(path_record=pathname)
        else:

            workbook = xlsxwriter.Workbook('{0}\\output.xlsx'.format(self.id_num))
            worksheet = workbook.add_worksheet()
            x = 0
            d = 0
            ##
            unsorted_result = []
            col = 1
            worksheet.write(0, 0, "Query")
            for root, dirs, files in os.walk("{0}\\subfolder".format(self.id_num)):
                for name in files:
                    if name.endswith('.xml'):
                    #if name == "GCA_900492555.1.xml":
                        file_name = os.path.splitext(name)[0]
                        pathname = os.path.join(root, name)
                        result = SearchIO.parse("{0}\\subfolder\\{1}".format(self.id_num, name), "blast-xml")
                        value_points = 0
                        row = 1
                        all_hit_names = []
                        count = 0
                        for hits in result:
                            count += 1
                            if len(hits) < 1:
                                all_hit_names.append(0)
                                continue
                            hit_names = []
                            for hit in hits:
                                des = hit.description
                                for data in hit:
                                    score = data.bitscore
                                    query_start = data.query_start
                                    subject_start = data.hit_start
                                    e_value = data.evalue
                                    if data.aln_span/hits.seq_len > 1:
                                        coverage = 100
                                    else:
                                        coverage = "%.2f" % ((data.aln_span/hits.seq_len) * 100)
                                    identity = "%.2f" % ((data.ident_num/data.aln_span) * 100)
                                    position = str(data.hit_start + 1) + ":" + str(data.hit_end)
                                    leng = data.hit_end - data.hit_start
                                    if float(coverage) < self.min_coverage or float(identity) < self.min_identity or leng < self.min_leng or leng > self.max_leng:
                                        #hit_names.append("not")
                                        continue
                                    else:
                                        hit_description = "COV {0}%, IDENT {1}%, SCORE {2}, POSITION {3}, LENGTH {4}".format(coverage, identity, score, position, leng)
                                        hit_values = {"score": score, "e_value": e_value, "coverage": coverage, "identity": identity, "query_start": query_start, "subject_start": subject_start}
                                        hit_data = [hit_description, hit_values]
                                        hit_names.append(hit_data)
                                        if self.sort_horizontal != "without sorting":
                                            value_points += float(hit_values[self.sort_horizontal])


                            if len(hit_names) < 1:
                                sorted_hit_names = 0
                            elif self.sort_by == "query_start" or self.sort_by == "subject_start":
                                sorted_hit_names = sorted(hit_names, key=self.by_value, reverse=False)
                            else:
                                sorted_hit_names = sorted(hit_names, key=self.by_value, reverse=True)
                            all_hit_names.append(sorted_hit_names)
                        unsorted_result.append((file_name, value_points, all_hit_names))
            if self.sort_horizontal != "without sorting":
                sorted_result = sorted(unsorted_result, key=self.by_value_points, reverse=True)
            sorted_result = unsorted_result

            for records in sorted_result:
                sequence_name = records[0]
                total_value = records[1]
                all_hit_names = records[2]
                description = "{0}, {1}".format(sequence_name, total_value)
                worksheet.write(0, col, description)
                row = 1
                for hit_names in all_hit_names:
                    if hit_names == 0:
                        worksheet.write(row, col, "0")
                        row += 1
                        continue
                    cell_output = ""
                    for count, hit_data in enumerate(hit_names, start=1):
                        hit_description = str(hit_data[0])
                        hit_output = str(count) + ")" + hit_description + "\n"
                        cell_output += hit_output
                    worksheet.write(row, col, cell_output)
                    row += 1
                if x < 1:
                    c = 0
                    r = 1
                    res = SeqIO.parse("{0}\\{1}".format(self.id_num, self.query_name), "fasta")
                    for h in res:
                        worksheet.write(r, c, h.id)
                        r += 1
                x += 1
                col += 1
            workbook.close()
            return "Succes"
