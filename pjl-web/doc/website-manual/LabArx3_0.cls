% ---------------------------------------------------------------------
% Article class for University of Calgary Physics Labs
% Created by Peter Gimby
% Jun 10, 2019
% Based off of Artical Class LabatorialArc.cls Created by Sean Sotyn
%
% version 3.0  -- Development version for WI 2021
% last revision Feb 12, 2021
% 
% ---------------------------------------------------------------------


% This file is should not be edited. If there are extra packages required for 
% new documents please contact Peter Gimby (pgimby@ucalgary.ca)

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{LabArx3_0}[11/05/2020, v3.0]
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
\RequirePackage[usenames,dvipsnames,svgnames]{xcolor}	% must be loaded before tikz
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
\RequirePackage{xstring}       % used for conditional statements - see checkpoint command
\RequirePackage{pdfpages}	   % insert full page pdfs
\usepackage[toc]{appendix} % Used to add pdf appendix

%\RequirePackage{xparse}
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
\newif\ifCourseTitle
\newif\ifLabId
\newif\ifGoals
\newif\ifEquipment
\newif\ifPreperation
\newif\ifSetupPhoto
\newif\ifAuthor
\newif\ifVersion
\newif\ifSafety
\newif\ifSubtitle
\newif\ifCG

% set a default size for the setup photo
\def\@SetupSize{0.8}

% input of document specifics from author
\newcommand{\Logo}[1]{\def\@Logo{#1} \Logotrue}
\newcommand{\CourseNumber}[1]{\def\@CourseNumber{#1}\CourseNumbertrue}
\newcommand{\Semester}[1]{\def\@Semester{#1}\Semestertrue}
\newcommand{\Year}[1]{\def\@Year{#1}\Yeartrue}
\newcommand{\LabTitle}[1]{\def\@LabTitle{#1}\LabTitletrue}
\newcommand{\TitleVar}[3]{\def\@TitleVar{#1} \def\@TitleSize{#2} \def\@TitleSkip{#3} \TitleVartrue}
\newcommand{\CourseTitle}[3]{\def\@CourseTitle{#1} \def\@TitleSize{#2} \def\@TitleSkip{#3} \CourseTitletrue}
\newcommand{\Subtitle}[1]{\def\@Subtitle{#1} \Subtitletrue}
\newcommand{\LabId}[1]{\makeatletter \def\@LabId{#1}\LabIdtrue\makeatother}
\newcommand{\Goals}[1]{\def\@Goals{#1} \Goalstrue}
\newcommand{\Equipment}[1]{\def\@Equipment{#1}\Equipmenttrue}
\newcommand{\Preparation}[1]{\def\@Preparation{#1}\Preperationtrue}
\newcommand{\SetupPhoto}[2]{\def\@SetupPhoto{#1} \def\@Caption{#2} \SetupPhototrue}
\newcommand{\SetupRef}[1]{\def\@SetupRef{#1}}
\newcommand{\SetupSize}[1]{\def\@SetupSize{#1}}
\newcommand{\CG}{\CGtrue}
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
\newcommand{\Safety}[1]{\def\@Safety{#1} \Safetytrue}

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
\renewcommand{\cftchapafterpnum}{\vspace{10pt}}
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
\ifSafety{\Large{\bf Safety Concerns:} \@Safety \par} \fi
\ifEquipment {{\bf Equipment:} \@Equipment \par} \fi
\ifGoals {{\bf Goals of the Experiment:} \@Goals \par } \fi
\ifPreperation {{\bf Preparation:} \@Preparation \par} \fi

% unset booleans in case there are multiple uses of \maketitle
\setboolean{LabTitle}{false}
\setboolean{TitleVar}{false}
\setboolean{Author}{false}
\setboolean{Version}{false}
\setboolean{SetupPhoto}{false}
\setboolean{Safety}{false}
\setboolean{Equipment}{false}
\setboolean{Goals}{false}
\setboolean{Preperation}{false}
}%

%\} \fi
% companion guide title page
\newcommand{\cgtitle}{%
\ifLabTitle {\begin{center} \bf \scshape\large \@LabTitle\ - Companion Guide \end{center}} \fi
{\makeatletter}
\ifLabTitle {\addcontentsline{toc}{chapter}{\@LabTitle{} - Companion Guide}} \fi
{\makeatother}
}%

% main lab manual title
\newcommand{\coursetitle}{%
\ifLogo {\begin{flushleft} \includegraphics[scale=0.5]{\@Logo} \end{flushleft}} \fi
\begin{center} 
\ifCourseTitle{\bf \scshape\huge \@CourseTitle\ \fi}\\
\vspace{1ex}
{\bf \huge Laboratory Manual} \\
\ifSubtitle{\vspace{1ex} \bf \large \@Subtitle \\} \fi
\vspace{2ex}
\ifSemester{\bf \large \@Semester} \fi 
\ifYear{\bf \large \@Year} \fi \\
\ifVersion{\bf Version: \@Version \\ } \fi
\ifCG{\bf \vspace{1em} \ \large with Companion Guide \\} \fi
\end{center}
\newpage
\tableofcontents
\newpage

%{\makeatletter}
%\ifCourseTitle {\addcontentsline{toc}{part}{\@CourseTitle{}}} \fi
%{\makeatother}
}%

% ---------------------------------------------------------------------		  
% Configure adding full pdfs as an appendix at end of document
% ---------------------------------------------------------------------

% pdfs added to the end of documents currently and an toc entry for each
% page of the pdf. Would like to make this entry only once


\newcommand{\pjlAppendix}[4]{
\includepdf[scale=#4,pages={#3},pagecommand={\phantomsection\addcontentsline{toc}{section}{#2}}]{#1}
%\includepdf[scale=0.9,pagecommand={\phantomsection\addcontentsline{toc}{section}{LF351 Single Operational Amplifier (JFET)}}]{LF351.pdf}
}


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
	\ifnum\value{questionCounter} < 10
	\hangindent=2.2cm \textbf{Question \arabic{questionCounter}:} #1\fi
	\ifnum\value{questionCounter} > 9
	\hangindent=2.4cm \textbf{Question \arabic{questionCounter}:} #1\fi
 	}
\newcommand{\questionReset}{\setcounter{questionCounter}{0}}

% ---------------------------------------------------------------------
% define environment for procedure steps
% ---------------------------------------------------------------------

\newcounter{procedureCounter}
\setcounter{procedureCounter}{0}
\newcommand{\procedure}[1]{\refstepcounter{procedureCounter}
	\ifnum\value{procedureCounter} < 10
	\hangindent=1.4cm \textbf{Step \arabic{procedureCounter}:} #1\fi
	\ifnum\value{procedureCounter} > 9
	\hangindent=1.6cm \textbf{Step \arabic{procedureCounter}:} #1\fi
	}
	
\newcommand{\procedureReset}{\setcounter{procedureCounter}{0}}


% ---------------------------------------------------------------------
% define environment for checkpoints
% ---------------------------------------------------------------------

\newcounter{checkpointCounter}
\setcounter{checkpointCounter}{0}
\newcommand{\checkpoint}[3]{\refstepcounter{checkpointCounter}
	%\rule{\textwidth}{0.2mm}
	\fbox{
	%first column
	\begin{minipage}{0.15\textwidth}%\hspace{0.05cm}
	\tikz{\node[regular polygon, regular polygon sides=8, minimum width=2cm, draw=white,fill=red,label=center:\color{white}{\bfseries \Large STOP}]at(0,0){};}
	\end{minipage}
	%second column
	\begin{minipage}{0.85\textwidth}
		\IfEqCase{#1}{%
        	{due}{CHECKPOINT \arabic{checkpointCounter}: SUBMIT ANSWERS TO THIS PART TOGETHER WITH YOUR VIDEO AND/OR PHOTOS TO ``#3" Dropbox on D2L \textbf{by #2}. This portion of the Lab will marked INDIVIDUALLY.}%
        	{middle}{CHECKPOINT \arabic{checkpointCounter}: Before moving on to the next part, have your TA evaluate your results.}
        	{end}{FINAL CHECKPOINT! Before being dismissed from the lab, discuss your results as a group, then have your TA evaluate your answers.}%
        % you can add more cases here as desired
    }[\PackageError{checkpoint}{Undefined option to checkpoint: #1. expecting "due", "middle", or "end"}{}]%
 	\end{minipage}
	}
}
\newcommand{\checkpointReset}{\setcounter{checkpointCounter}{0}}

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



