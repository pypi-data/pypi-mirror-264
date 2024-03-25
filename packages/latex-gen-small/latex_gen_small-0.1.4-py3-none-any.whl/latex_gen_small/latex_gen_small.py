def write_to_file(latex_code, path_to_file="main.tex"):
    """
    Writes the provided LaTeX code to a file.

    This function takes a string containing LaTeX code and writes it to a file.
    The file path is specified by the `path_to_file` parameter, which defaults to "main.tex".
    If the file does not exist, it will be created. If it does exist, its contents will be overwritten.

    Parameters:
    - latex_code (str): The LaTeX code to be written to the file.
    - path_to_file (str, optional): The path to the file where the LaTeX code will be written.
      Defaults to "main.tex".
    """
    with open(path_to_file, "w") as file:
        file.write(latex_code)


def make_latex_document(tex_code):
    """
    Generates a LaTeX document from the given TeX code.

    This function wraps the provided TeX code with the necessary LaTeX document
    structure, including the document class declaration and the document
    environment. The input TeX code is inserted between these structures.

    Parameters:
    - tex_code (str): The TeX code to be included in the document.

    Returns:
    - str: The complete LaTeX document as a string.
    """
    tex_code = [
        "\\documentclass{article}",
        "\\usepackage{graphicx}",
        "\graphicspath{ {./images/} }",
        "\\usepackage{wrapfig}",
        "\\begin{document}",
        tex_code,
        "\\end{document}",
    ]
    tex_code = "\n".join(tex_code)
    return tex_code


def create_latex_image(image_filename):
    """
    Generates LaTeX code to include an image in a LaTeX document.

    This function constructs a LaTeX command to include an image file in a LaTeX document.
    The image file name is specified by the `image_filename` parameter.

    Parameters:
    image_filename (str): The name of the image file to be included.

    Returns:
    str: A LaTeX command to include the specified image file.
    """
    latex_code = "\\includegraphics{mesh}\n"
    return latex_code


def latex_code_union(list_of_latex_code, sep="\n\n"):
    """
    Combines a list of LaTeX code snippets into a single string, separated by a specified separator.

    This function takes a list of LaTeX code snippets and concatenates them into a single string,
    with each snippet separated by a specified separator. The default separator is two newline characters.

    Parameters:
    list_of_latex_code (list): A list of LaTeX code snippets to be combined.
    sep (str, optional): The separator to use between the snippets. Defaults to "\n\n".

    Returns:
    str: A single string containing all the LaTeX code snippets, separated by the specified separator.
    """
    latex_code = f"{sep}".join(list_of_latex_code)
    return latex_code


def create_latex_table(data, table_caption="Caption for table"):
    """
    Generates a LaTeX table from the provided data.

    This function takes a list of lists (data) where the first list represents the table headers,
    and the subsequent lists represent the rows of the table. It also accepts an optional parameter
    for the table caption, which defaults to "Caption for table". The function returns a string
    containing the LaTeX code for the table, including the table environment, headers, rows,
    and a caption.

    Parameters:
    - data (list of lists): The data to be formatted into a LaTeX table. The first list should contain
      the table headers, and the subsequent lists should contain the table rows.
    - table_caption (str, optional): The caption for the table. Defaults to "Caption for table".

    Returns:
    - str: The LaTeX code for the table.

    Example:
    >>> data = [
            ["Header 1", "Header 2", "Header 3"],
            ["Data 1", "Data 2", "Data 3"],
            ["Data 4", "Data 5", "Data 6"],
        ]
    >>> generate_latex_table(data, "Caption for table")
    
    \begin{table}[ht]
    \centering
    \begin{tabular}{c|c|c}
    \hline
    Header 1 & Header 2 & Header 3 \\
    \hline
    Data 1 & Data 2 & Data 3 \\
    Data 4 & Data 5 & Data 6 \\
    \hline
    \end{tabular}
    \caption{Caption for table}
    \label{{table:your_label_here}}
    \end{table}
    
    """
    # We get the number of columnsв
    num_columns = len(data[0])

    # Forming a row with column formats for LaTeX
    column_formats = "|".join(["c"] * num_columns)

    # Forming a row with the table headers
    header = " & ".join(data[0]) + " \\\\"

    # Forming rows with table data
    rows = "\n".join([" & ".join(map(str, row)) + " \\\\" for row in data[1:]])

    # Forming the full LaTeX code of the table
    latex_table = [
        "",
        "\\begin{table}[ht]",
        "\\centering",
        f"\\begin{{tabular}}{{{column_formats}}}",
        "\\hline",
        f"{header}",
        "\\hline",
        f"{rows}",
        "\\hline",
        "\\end{tabular}",
        f"\\caption{{{table_caption}}}",
        "\\label{{table:your_label_here}}",
        "\\end{table}",
    ]

    latex_table = "\n".join(latex_table)

    return latex_table
