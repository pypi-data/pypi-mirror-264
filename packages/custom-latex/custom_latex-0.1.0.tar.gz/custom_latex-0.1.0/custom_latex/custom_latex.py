def custom_latex(data):
    """
    Генерирует таблицу LaTeX из списка.
    """
    latex_table = "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{" + "l" * len(data[0]) + "}\n\\hline\n"
    latex_table += " & ".join(data[0]) + " \\\\\n\\hline\n"

    for row in data[1:]:
        latex_table += " & ".join(row) + " \\\\\n"

    latex_table += "\\hline\n\\end{tabular}\n\\end{table}\n\n"

    return latex_table

def generate_latex_image(filepath, caption=""):
    """
    Генерирует LaTeX код для вставки картинки.
    """
    latex_image = "\\begin{figure}[h!]\n" \
                  "\\centering\n" \
                  "\\includegraphics[width=0.3\\textwidth]{" + filepath + "}\n" \
                  "\\caption{" + caption + "}\n" \
                  "\\end{figure}\n\n"

    return latex_image
