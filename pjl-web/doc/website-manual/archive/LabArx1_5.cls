% ---------------------------------------------------------------------
% Article class for University of Calgary Labs
% Created by Peter Gimby
% Jun 10, 2019
% Based off of Artical Class LabatorialArc.cls Created by Sean Sotyn
%
% version 1.5
% last revision Aug 26, 2019
% ---------------------------------------------------------------------


% This file is should not be edited. If there are extra packages required for 
% new documents please contact Peter Gimby (pgimby@ucalgary.ca)

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{LabArx1_5}[20/08/2019, v1.5]
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
\RequirePackage{tikz}
\RequirePackage{lipsum}
\RequirePackage{comment}		% Allows for large comments
\RequirePackage{siunitx}
\RequirePackage{multirow}		% Allows text wrapping in tables
\RequirePackage{anyfontsize} 	% Allows customized font sizes
\RequirePackage{xcolor}
\RequirePackage{colortbl}
\RequirePackage{physics}
\RequirePackage{dirtree}
\RequirePackage{float}
% \RequirePackage{hyperref}
% \RequirePackage{cleveref}

% ---------------------------------------------------------------------		  
% configure margins		  
% ---------------------------------------------------------------------

\RequirePackage[left=1in, right=1in, top=1in, bottom=1in, headheight=14.5pt, letterpaper]{geometry}%
\RequirePackage[width=.8\textwidth,labelfont={bf,sf}, footnotesize, labelsep=period, justification=raggedright]{caption}
\RequirePackage[width=.8\textwidth]{subcaption}
\setlength{\parskip}{12pt}
\setlength{\parindent}{0in}

% ---------------------------------------------------------------------		  
% new commands for generating titlepaged and header/footers
% ---------------------------------------------------------------------

% booleans to make title page components optional
\newif\ifLogo
\newif\ifCourseNumber
\newif\ifSemester
\newif\ifYear
\newif\ifLabTitle
\newif\ifTitleVar
%\newif\ifTitle
\newif\ifLabId
\newif\ifGoals
\newif\ifEquipment
\newif\ifPreperation
\newif\ifSetupPhoto
\newif\ifAuthor
\newif\ifVersion

% set a default size for the setup photo
\def\@SetupSize{0.8}

% input of document specifics from author
\newcommand{\Logo}[1]{\def\@Logo{#1} \Logotrue}
\newcommand{\CourseNumber}[1]{\def\@CourseNumber{#1}\CourseNumbertrue}
\newcommand{\Semester}[1]{\def\@Semester{#1}\Semestertrue}
\newcommand{\Year}[1]{\def\@Year{#1}\Yeartrue}
\newcommand{\LabTitle}[1]{\def\@LabTitle{#1}\LabTitletrue}
\newcommand{\TitleVar}[3]{\def\@TitleVar{#1} \def\@TitleSize{#2} \def\@TitleSkip{#3} \TitleVartrue}
%\newcommand{\Title}[3]{\def\@Title{#1} \def\@TitleSize{#2} \def\@TitleSkip{#3} \Titletrue}
\newcommand{\LabId}[1]{\makeatletter \def\@LabId{#1}\LabIdtrue\makeatother}
\newcommand{\Goals}[1]{\def\@Goals{#1} \Goalstrue}
\newcommand{\Equipment}[1]{\def\@Equipment{#1}\Equipmenttrue}
\newcommand{\Preparation}[1]{\def\@Preparation{#1}\Preperationtrue}
\newcommand{\SetupPhoto}[2]{\def\@SetupPhoto{#1} \def\@Caption{#2} \SetupPhototrue}
\newcommand{\SetupRef}[1]{\def\@SetupRef{#1}}
\newcommand{\SetupSize}[1]{\def\@SetupSize{#1}}
\newcommand{\Setup}[1]{%
	\begin{figure}[h!]
		\centering
		\includegraphics[width=\@SetupSize\textwidth,height=\@SetupSize\textheight,keepaspectratio]{#1}
		\caption{\@Caption}
		\label{setup}
	\end{figure}
}
\newcommand{\Author}[1]{\def\@Author{#1} \Authortrue}
\newcommand{\Version}[1]{\def\@Version{#1} \Versiontrue}


% ---------------------------------------------------------------------		  
% commands for main body of document. Ensures that unique references 
% will remain even if documents are combined.
% ---------------------------------------------------------------------

\let\origLabel\label
\renewcommand{\label}[1]{\origLabel{\ifLabId\@LabId#1\else#1\fi}}
\let\origRef\ref
\renewcommand{\ref}[1]{\origRef{\ifLabId\@LabId#1\else#1\fi}}
\let\origBibitem\bibitem
\renewcommand{\bibitem}[1]{\origBibitem{\ifLabId\@LabId#1\else#1\fi}}
\let\origCite\cite
\renewcommand{\cite}[1]{\origCite{\ifLabId\@LabId#1\else #1\fi}}
\newcommand{\eqlabel}[1]{\origLabel{\ifLabId\@LabId#1\else #1\fi}}

% ---------------------------------------------------------------------
% configure table of contents	
% ---------------------------------------------------------------------

% ---------------------------------------------------------------------		  
% configure table of contents and section labels
% ---------------------------------------------------------------------

\RequirePackage{titlesec}
\RequirePackage{tocloft}
%\renewcommand{\cftchapafterpnum}{\vspace{10pt}}
\titleformat{\chapter}[hang] 
{\normalfont\huge\bfseries}{\thechapter}{1em}{}


%\setcounter{tocdepth}{0}
%\renewcommand{\thesection}{}
%\renewcommand{\thechapter}{}
%\renewcommand{\thesubsection}{}
%\renewcommand{\thebibliography}{}

% ---------------------------------------------------------------------		  
% configure titlepages
% ---------------------------------------------------------------------

% main lab title page
\renewcommand{\maketitle}{%
\thispagestyle{fancy}%
\ifLogo {\begin{flushleft} \includegraphics[scale=0.5]{\@Logo} \end{flushleft}} \fi
\ifLabTitle {\begin{center} \bf \scshape\large \@LabTitle \end{center} } \fi
\ifTitleVar {\begin{center} \fontsize{\@TitleSize}{\@TitleSkip}\selectfont \bf \scshape \@TitleVar \end{center}\refstepcounter{chapter}} \fi
\ifAuthor {\begin{center}{\bf Author:} \@Author \par \end{center}} \fi
\ifVersion {\begin{center}{\bf Version:} \@Version \par \end{center}} \fi
{\makeatletter}
\ifLabTitle {\addcontentsline{toc}{chapter}{\@LabTitle{}}\refstepcounter{chapter}} \fi
%\ifTitleVar {\addcontentsline{toc}{chapter}{\@TitleVar{}}} \fi
{\makeatother}
\ifSetupPhoto {\Setup{\@SetupPhoto}} \fi
\ifEquipment {{\bf Equipment:} \@Equipment \par} \fi
\ifGoals {{\bf Goals of the Experiment:} \@Goals \par} \fi
\ifPreperation {{\bf Preparation:} \@Preparation \par} \fi
}%

%\} \fi
% companion guide title page
\newcommand{\cgtitle}{%
\ifLabTitle {\begin{center} \bf \scshape\large \@LabTitle\ - Companion Guide \end{center}} \fi
{\makeatletter}
\ifLabTitle {\addcontentsline{toc}{chapter}{\@LabTitle{} - Companion Guide}} \fi
{\makeatother}
}%

% ---------------------------------------------------------------------		  
% bibliography			  
% ---------------------------------------------------------------------

% ---------------------------------------------------------------------		  
% headers and footers		  
% ---------------------------------------------------------------------

\RequirePackage{fancyhdr}  % Needed to define custom headers/footers
\RequirePackage{lastpage}  % Number of pages in the document
\RequirePackage{datetime2}
\renewcommand{\headrulewidth}{0pt}% % No header rule
\renewcommand{\footrulewidth}{0pt}% % No footer rule
\fancyhead{}
\fancyfoot{}
\pagestyle{fancy}
\fancyhead[OR]{\footnotesize 
	\ifCourseNumber Physics\ \@CourseNumber:\ \fi
	\ifSemester \@Semester\ \fi
	\ifYear  \@Year \fi}
\fancyhead[EL]{\footnotesize
	\ifCourseNumber Physics\ \@CourseNumber:\ \fi
	\ifSemester \@Semester\ \fi
	\ifYear \@Year \fi}
\fancyfoot[OR]{\footnotesize Page \thepage\ of \pageref{LastPage}}
\fancyfoot[EL]{\footnotesize Page \thepage\ of \pageref{LastPage}}
\fancyfoot[ER]{\footnotesize 
	\ifLabId LabID\ \@LabId \fi}
\fancyfoot[OL]{\footnotesize
	\ifLabId LabID\ \@LabId \fi}

% ---------------------------------------------------------------------		  
% define environment for questions
% ---------------------------------------------------------------------


\newcounter{questionCounter}
\setcounter{questionCounter}{0}
\newcommand{\question}[1]{\refstepcounter{questionCounter}
	% first column
	\begin{minipage}[t]{0.15\textwidth}
   	\textbf{Question \arabic{questionCounter}:}
	\end{minipage}
	% %second column
	\begin{minipage}[t]{0.85\textwidth}
 	#1
 	\end{minipage}\\
 	\\
 	\\
 	}
\newcommand{\questionReset}{\setcounter{questionCounter}{0}}

% ---------------------------------------------------------------------
% define environment for procedure steps
% ---------------------------------------------------------------------

\newcounter{procedureCounter}
\setcounter{procedureCounter}{0}
\newcommand{\procedure}[1]{\refstepcounter{procedureCounter}
	% first column
	\begin{minipage}[t]{0.1\textwidth}
   	\textbf{Step \arabic{procedureCounter}:}
	\end{minipage}
	% %second column
	\begin{minipage}[t]{0.9\textwidth}
 	#1
 	\end{minipage}\\
 	\\
 	\\
	}
\newcommand{\procedureReset}{\setcounter{procedureCounter}{0}}

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
