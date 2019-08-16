% ---------------------------------------------------------------------
% Article class for PJL Process Documents
% Created by Peter Gimby
% May 2019
% Based off of Artical Class LabatorialArc.cls Created by Sean Sotyn
%
% version 1.0
% ---------------------------------------------------------------------


% This file is should not be edited. If there are extra packages required for 
% new documents please contact Peter Gimby (pgimby@ucalgary.ca)

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pjlProcessDocs}[14/05/2019, v1.0]
\AtEndOfClass{\RequirePackage{microtype}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions*
\LoadClass[twoside]{report}

% ---------------------------------------------------------------------		  
% Loading packages	
% ---------------------------------------------------------------------

\RequirePackage{enumitem}	% Extended options for enumerated environment
\RequirePackage{ifpdf}      % Needed to pick between latex and pdflatex
\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage{graphicx}
\RequirePackage[english]{babel}
\RequirePackage{underscore}
\RequirePackage{gensymb}
\RequirePackage{siunitx}
\RequirePackage{tikz}
\RequirePackage{lipsum}
\RequirePackage{comment}		% Allows for large comments
\RequirePackage{siunitx}
\RequirePackage{layout}
\RequirePackage{dirtree}
\RequirePackage{xcolor}

% ---------------------------------------------------------------------		  
% configure package for showing sample code
% ---------------------------------------------------------------------

\RequirePackage{listings,lstautogobble}
\definecolor{light-gray}{gray}{0.98}
\lstset{
	backgroundcolor = \color{light-gray},
	autogobble=true,
	columns=fullflexible,
	%frame=single,
	breaklines=true,
	postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
}



% ---------------------------------------------------------------------		  
% margins		  
% ---------------------------------------------------------------------

\RequirePackage[left=1in, right=1in, top=1in, bottom=1in, headheight=14.5pt, letterpaper]{geometry}%
\RequirePackage[labelfont={bf,sf}, footnotesize, labelsep=period, justification=raggedright]{caption}
\setlength{\parskip}{12pt}
\setlength{\parindent}{0in}


% ---------------------------------------------------------------------		  
% headers and footers		  
% ---------------------------------------------------------------------

\RequirePackage{fancyhdr}  % Needed to define custom headers/footers
% \RequirePackage{lastpage}  % Number of pages in the document
% \RequirePackage{datetime2}
% \renewcommand{\headrulewidth}{0pt}% % No header rule
% \renewcommand{\footrulewidth}{0pt}% % No footer rule
% \fancyhead{}
% \fancyfoot{}
% \pagestyle{fancy}
% % %\fancyfoot[RO,LE]{\footnotesize  \thepage\ of \pageref{LastPage}}
% % %\fancyfoot[RE,LO]{\footnotesize \thepage\ of \pageref{LastPage}}
% \fancyfoot[C]{\footnotesize Page \thepage\ of \pageref{LastPage}}
% % % \fancyfoot[R]{\footnotesize Physics \@CourseNumber \ \@Semester \ \@Year}
% % % \fancyfoot[L]{\footnotesize LabID\ \@LabId: \DTMtoday}

% ---------------------------------------------------------------------		  
% configure table of contents and section labels
% ---------------------------------------------------------------------

\RequirePackage{titlesec}
\RequirePackage{tocloft}
\renewcommand{\cftchapafterpnum}{\vspace{10pt}}
%\renewcommand{\cftsecafterpnum}{\vspace{8pt}}
%\renewcommand{\cftsubsecafterpnum}{\vspace{5pt}}
\titleformat{\chapter}[hang] 
{\normalfont\huge\bfseries}{\thechapter:}{1em}{}


% ---------------------------------------------------------------------		  
% new commands for generating titlepage		  
% ---------------------------------------------------------------------

\newcommand{\Logo}[1]{\def\@Logo{#1}}
% \newcommand{\CourseNumber}[1]{\def\@CourseNumber{#1}}
\newcommand{\Title}[1]{\def\@Title{#1}}
\newcommand{\Author}[1]{\def\@Author{#1}}
\newcommand{\Version}[1]{\def\@Version{#1}}


% \RequirePackage{tocloft}
% \RequirePackage{titlesec}
% \titleformat{\chapter}[hang] 
% {\normalfont\huge\bfseries}{\thechapter}{1em}{} 
% \renewcommand{\cftsecafterpnum}{\vspace{10pt}}
% \renewcommand{\cftchapafterpnum}{\vspace{10pt}}

% \newcommand{\LabId}[1]{\makeatletter \def\@LabId{#1} \makeatother}
% \newcommand{\Goals}[1]{\def\@Goals{#1}}
% \newcommand{\Equipment}[1]{\def\@Equipment{#1}}
% \newcommand{\Preparation}[1]{\def\@Preparation{#1}}
% \newcommand{\SetupPhoto}[2]{\def\@SetupPhoto{#1} \def\@Caption{#2}}
% \newcommand{\SetupRef}[1]{\def\@SetupRef{#1}}
% \newcommand{\SetupSize}[1]{\def\@SetupSize{#1}}
% \newcommand{\Setup}[1]{%
% 	\begin{figure}[h!]
% 		\centering
% 		\includegraphics[width=\@SetupSize\textwidth,height=\@SetupSize\textheight,keepaspectratio]{#1}
% 		\caption{\@Caption}
% 		\label{setup}
% 	\end{figure}
% }

% ---------------------------------------------------------------------		  
% commands for main body of document. Ensures that unique references 
% will remain even if documents are combined.
% ---------------------------------------------------------------------

% \let\origLabel\label
% \renewcommand{\label}[1]{\origLabel{\@LabId#1}}
% \let\origRef\ref
% \renewcommand{\ref}[1]{\origRef{\@LabId#1}}
% \let\origBibitem\bibitem
% \renewcommand{\bibitem}[1]{\origBibitem{\@LabId#1}}
% \let\origCite\cite
% \renewcommand{\cite}[1]{\origCite{\@LabId#1}}


% ---------------------------------------------------------------------		  
% configure titlepage		  
% ---------------------------------------------------------------------

\renewcommand{\maketitle}{%
\thispagestyle{fancy}%
{\begin{flushleft} \includegraphics[scale=0.5]{\@Logo} \end{flushleft}}
{\begin{center} \bf \scshape\Large \@Title \end{center}}
{\begin{center} \scshape\large \@Author \end{center}}
{\begin{center} \scshape\footnotesize Version \@Version \end{center}}

% {{\bf Equipment:} \@Equipment \par}
% {{\bf Goals of the Experiment:} \@Goals \par}
% {{\bf Preparation:} \@Preparation \par}
}%
