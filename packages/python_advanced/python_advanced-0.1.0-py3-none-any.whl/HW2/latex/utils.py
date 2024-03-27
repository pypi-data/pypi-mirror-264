import typing as tp


def generate_latex_table(data: tp.List[tp.List[float]]) -> str:
    """
    Функция для генерации таблиц (кода .tex). 
    На вход поступает двойной список, на выходе строка с отформатированным валидным латехом.
    """
    n_columns = len(data[0])
    latex_table = "\\begin{tabular}{|" + "c|" * n_columns + "}\n\\hline\n"
    for row in data:
        latex_table += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
    latex_table += "\\end{tabular}\n"
    return latex_table


def generate_latex_image(path: str) -> str:
    """
    Функция для генерации  кода .tex 
    На вход поступает путь до png файла, на выходе строка с отформатированным валидным латехом.
    """
    latex_image = f"""
\\begin{{figure}}[ht]
\\includegraphics{{{path}}}
\\caption{{Инфографика}}
\\label{{fig:image}}
\\end{{figure}}
"""
    return latex_image


def generate_latex(
        data: tp.Optional[tp.List[tp.List[float]]]=None, 
        image_path: tp.Optional[str]=None,
        fillename:str = 'example'
        ) -> str:
    """
    Функция для генерации латех документа (кода .tex). 
    На вход поступает двойной список, путь до png файла. 
    На выходе сохраняется файл и возаращается строка с отформатированным валидным латехом.
    """
    latex_doc = """
\\documentclass{article}
\\usepackage[T2A]{fontenc}
\\usepackage{graphicx}
\\begin{document}
"""
    if data:
        latex_doc += generate_latex_table(data)

    if image_path:
        latex_doc += generate_latex_image(image_path)
    
    latex_doc += "\\end{document}"
    
    _save_latex(latex_doc, fillename)
    return latex_doc


def _save_latex(latex: str, filename: str="example"):
    with open(f"/Users/kandryukov.ma/ITMO/Python_Advanced/HW2/artifacts/{filename}.tex", "w") as f:
        f.write(latex)
