def generateStart():
    # Packages
    text = ("\\documentclass{article}\n"
            + "\\usepackage{graphicx}\n\\usepackage{amsmath}\n\\usepackage{color}\n"
            + "\\usepackage{cite}\n\\usepackage[russian]{babel}\n\\usepackage{longtable}\n\n")

    # Document settings
    text += ("\\setlength{\\parindent}{0pt}\n"
             + "\\linespread{1.25}\n\n")

    text += ("\\date{}\n"
             + "\\begin{document}\n"
             + "\\maketitle\n\n")

    text += "\\section{Generator}\n\n"

    return text


def generateEnd():
    text = "\\end{document}"
    return text


def generateTable(data, generate_begin=False, generate_end=False):
    table = ""

    if generate_begin:
        table += generateStart()

    num_rows = len(data)
    num_cols = len(data[0]) if data else 0

    if num_rows == 0 or num_cols == 0:
        return ""

    table += ("\\begin{table}[htbp]\n"
             + "\\centering\n"
             + "\\begin{tabular}{|" + "|".join(["c"]*num_cols) + "|}\n"
             + "\\hline\n")

    for row in data:
        table += " & ".join(str(cell) for cell in row)
        table += " \\\\\n"
        table += "\\hline\n"

    table += ("\\end{tabular}\n"
              + "\\caption{Python generated table}\n"
              + "\\end{table}\n\n")

    if generate_end:
        table += generateEnd()

    return table


def generateImage(path, generate_begin=False, generate_end=False):
    image = ""

    if generate_begin:
        image += generateStart()

    image = ("\\begin{figure}[htbp]\n"
             + "\\centering\n"
             + "\\includegraphics{" + path + "}\n"
             + "\\caption{Python generated}\n"
             + "\\end{figure}\n\n")

    if generate_end:
        image += generateEnd()

    return image
