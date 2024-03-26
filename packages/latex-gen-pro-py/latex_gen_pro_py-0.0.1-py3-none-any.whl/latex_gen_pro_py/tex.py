def generate(*latex_code):
    latex_template_begin = r'''\documentclass{article}
\usepackage{graphicx} % Required for inserting images

\title{ProPython_hw02}
\author{zibumzibumich }
\date{March 2024}

\begin{document}

\maketitle
'''
    latex_template_end = r'''

\section{Introduction}

\end{document}
'''
    return latex_template_begin+'\n\n'.join(latex_code)+latex_template_end
    


def table(data):
    def format_cell(cell):
        return str(cell).\
            replace('&', r'\&').\
            replace('%', r'\%').\
            replace('#', r'\#').\
            replace('_', r'\_').\
            replace('$', r'\$').\
            replace('{', r'\{').\
            replace('}', r'\}')
    
    def format_row(row):
        return ' & '.join(format_cell(cell) for cell in row) + r' \\'
    
    latex_table = r'\begin{tabular}{|' + '|'.join('c' * len(data[0])) + '|}'
    for row in data:
        latex_table += '\n\\hline\n' + format_row(row)
    latex_table += '\n\\hline\\end{tabular}'
    
    return latex_table


def image(png_path):
    return r'''
    \begin{figure}[h!]
    \centering
    \includegraphics{'''+ png_path + r'''}
    \caption{My Image}
    \label{fig:my_image}
    \end{figure}
    '''
