input_file = "annotation.csv"
output_file = "annotation_spaced.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        # Replace every comma with comma + space
        new_line = line.replace(",", ", ")
        outfile.write(new_line)