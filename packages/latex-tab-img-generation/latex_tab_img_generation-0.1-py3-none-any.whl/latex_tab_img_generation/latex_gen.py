def generate_latex_table(data):
    latex_code = "\\begin{table}[h!]\n\\centering\n"
    latex_code += "\\begin{tabular}{|" + "|".join(["c"] * len(data[0])) + "|}\n"
    latex_code += "\\hline\n"

    for row in data:
        latex_code += " & ".join(map(str, row)) + " \\\\\n"
        latex_code += "\\hline\n"

    latex_code += "\\end{tabular}\n"
    latex_code += "\\end{table}"
    return latex_code

def generate_latex_image(image_path, caption=''):
    latex_code = "\\begin{figure}[h!]\n"
    latex_code += "\\centering\n"
    latex_code += "\\includegraphics{" + image_path + "}\n"

    if caption:
        latex_code += "\\caption{" + caption + "}\n"
        
    latex_code += "\\end{figure}\n"
    return latex_code