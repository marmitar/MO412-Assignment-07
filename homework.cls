% aga-homework.cls
%
% A LaTeX2e document class for preparing homework solutions.

% --- METADATA -----------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{homework}

% --- OPTION PROCESSSING -------------------------------------------------------
\RequirePackage{kvoptions}
\SetupKeyvalOptions{
    family = homework,
    prefix = homework@
}

\DeclareStringOption[1]{assignment}

% pass unrecognized options to `article` class
\DeclareDefaultOption{%
    \PassOptionsToClass{\CurrentOption}{article}%
}

% process all options
\ProcessKeyvalOptions{homework}

% load parent class with some default options
\LoadClass[a4paper, 11pt]{article}

\RequirePackage[english]{babel}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
% --- PACKAGES AND SETUP -------------------------------------------------------
\RequirePackage[
    a4paper,
    headheight = 20pt,
    margin = 1in,
    top = \dimexpr 1in - 10pt \relax,
    bottom = \dimexpr 1in - 20pt \relax,
    footskip = 0pt,
]{geometry} % set up nicer margins
\addtolength{\footskip}{20pt}
\RequirePackage{fancyhdr} % for headers and footers
\RequirePackage{graphicx} % for including figures
\RequirePackage{mathpazo} % use Palation font
\RequirePackage{amsmath} % use AMS math package
\RequirePackage{amssymb} % use AMS symbols
\RequirePackage{amsthm} % for writing proofs
\RequirePackage{array} % for setting up arguments to columns
\RequirePackage{booktabs} % for professional tables
\RequirePackage{xcolor} % for colored text (comments in algorithms)
\RequirePackage{trimspaces, xstring} % for multiple author parsing
\RequirePackage[bottom]{footmisc}
\RequirePackage[hidelinks]{hyperref}

% problemas com o ambiente 'proof' do thmbox
\LetLtxMacro\ams@proof\proof
\LetLtxMacro\ams@end@proof\endproof

\RequirePackage{thmtools}
\RequirePackage{framed}

\AtBeginDocument{%
    \LetLtxMacro\proof\ams@proof
    \LetLtxMacro\endproof\ams@end@proof
}

\let\leftbar\@undefined
\let\endleftbar\@undefined
\declaretheorem[thmbox=M]{theorem}
\declaretheorem[thmbox=M, numberlike=theorem]{proposition}

% look for figures in the figures directory
% \graphicspath{{figures/}}

% set up headers and footers; same for all pages
\setlength{\headheight}{14pt}
\fancyhf{}
% \fancyhead[L]{\sffamily Universidade Estadual de Campinas}
\fancyhead[L]{\sffamily%
    \href{https://www.unicamp.br/unicamp/}
        {University of Campinas}}
\fancyhead[R]{\sffamily%
    \href{https://www.ic.unicamp.br/~meidanis/courses/mo412/2022s1/}
        {MC908 Graph Algorithms, 2022 T1}}
\fancyfoot[L]{\sffamily%
    \href{https://ic.unicamp.br/}
        {IC Institute of Computing}}
\fancyfoot[R]{\sffamily%
    \bfseries\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\pagestyle{fancy}

\fancypagestyle{footnotes}{%
    \setlength{\footskip}{20pt}
}
\setlength{\skip\footins}{24pt plus 3pt minus 3pt}
\fancypagestyle{main}{%
    \setlength{\footskip}{44pt plus 3pt minus 3pt}
}
\renewcommand{\footnotelayout}{%
    \thispagestyle{footnotes}
}

% ensure that the title is inserted in the document
\title{%
    \vspace{-2\baselineskip}%
    \ifdefined\homeworkname%
        {\normalsize Assignment \homework@assignment} \\
        \homeworkname
    \else%
        Assignment \homework@assignment
    \fi%
}
% \author{\aga@authorsProcessed}
\author{%
    Tiago de Paula Alves ~(187679) \\
    \href{mailto:tiagodepalves@gmail.com}{\texttt{tiagodepalves@gmail.com}}
}
\AtBeginDocument{\maketitle\thispagestyle{fancy}}
