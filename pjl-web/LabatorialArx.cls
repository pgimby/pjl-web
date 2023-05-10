%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%																			   %
% 				     Article class for University of Calgary Labatorials						   %
% 						     Created by Sean Stotyn								   %
%							       June 2017										   %
%																			   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This is the only thing you need to change between semesters:
\def \Semester{Winter 2021}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




% The following should not be changed unless you know what you're doing:

% ---------------------------------------------------------------------		  
% Defining the article class
% ---------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{LabatorialArx}[26/06/2017, v1.0]
\AtEndOfClass{\RequirePackage{microtype}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions*
\LoadClass{article}

% ---------------------------------------------------------------------		  
% Loading packages	
% ---------------------------------------------------------------------

\RequirePackage{enumitem}
\RequirePackage{ifpdf}      % Needed to pick between latex and pdflatex
\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage{graphicx}
\RequirePackage[english]{babel}
\RequirePackage{underscore}
\RequirePackage{gensymb}
\RequirePackage{xcolor}

%\RequirePackage[utf8]{inputenc}
%\RequirePackage{marginnote}

% ---------------------------------------------------------------------		  
% Definitions for the pre-amble		  
% ---------------------------------------------------------------------

\newcommand{\LabatorialTitle}[1]{\def\@LabatorialTitle{#1}}
\newcommand{\CourseNumber}[1]{\def\@CourseNumber{#1}}
\newcommand{\LabatorialNumber}[1]{\def\@LabatorialNumber{#1}}
\newcommand{\Preparation}[1]{\def\@Preparation{#1}}
\newcommand{\Equipment}[1]{\def\@Equipment{#1}}
\newcommand{\Overview}[1]{\def\@Overview{#1}}
\newcommand{\TitleGraphicWidth}[1]{\def\@TitleGraphicWidth{#1}}
\newcommand{\TitleGraphic}[1]{\def\@TitleGraphic{#1}}
\newcommand{\TitleGraphicBoxWidth}[1]{\def\@TitleGraphicBoxWidth{#1}}
\newcommand{\OverviewBoxWidth}[1]{\def\@OverviewBoxWidth{#1}}
\newcommand{\TitleGraphicCaption}[1]{\def\@TitleGraphicCaption{#1}}
\newcommand{\url}[1]{\color{blue}{#1} \color{black}}

% ---------------------------------------------------------------------		  
% Setting the margins 
% ---------------------------------------------------------------------

\RequirePackage[left=1in, right=1in, top=1in, bottom=1in, headheight=11pt, letterpaper]{geometry}%
\RequirePackage[labelfont={bf,sf}, footnotesize, labelsep=period, justification=raggedright]{caption}
\setlength{\parskip}{11pt}
\setlength{\parindent}{0in}

% ---------------------------------------------------------------------		  
% Setting the headers and footers		  
% ---------------------------------------------------------------------

\RequirePackage{fancyhdr}  % Needed to define custom headers/footers
\RequirePackage{lastpage}  % Number of pages in the document
\pagestyle{fancy}          % Enables the custom headers/footers
\lhead{} % left header
\chead{} % center header
\rhead{\footnotesize PHYS \@CourseNumber, \@LabatorialNumber, \Semester} % right header
\lfoot{} % left footer
\cfoot{} % center footer
\rfoot{\footnotesize Page \thepage\ of \pageref{LastPage}} % right footer
\renewcommand{\headrulewidth}{0pt}% % No header rule
\renewcommand{\footrulewidth}{0pt}% % No footer rule

% ---------------------------------------------------------------------
% Question type set-up
% ---------------------------------------------------------------------  

% Add the ability to refer to a question within the document: 
\newcommand{\refques}[1]{\addtocounter{questioncounter}{-1}\refstepcounter{questioncounter}\label{#1}} 

% Formatting of a standard labatorial question:
\newcommand{\question}[2]{\textbf{Question\addtocounter{questioncounter}{1}
  	\arabic{questioncounter}}:
	#1 \par\textbf{}\vspace{#2}\\
	\begin{center}\rule{\textwidth}{0.2mm}\end{center}}

% Formatting for a figure caption
\newcommand{\figcap}[2]{\textbf{Figure\addtocounter{figurecounter}{1}
  	\arabic{figurecounter}}:
	#1 \par\textbf{}\vspace{#2}}

%\newcommand{\hrquestion}[2]{\textbf{Question\addtocounter{questioncounter}{1}
%  	\arabic{questioncounter}}:
%	#1 \par\textbf{Hypothesis:}\vspace{#2}\\ 
%	\par\textbf{Result:}\vspace{#2}\\
%	\begin{center}\rule{\textwidth}{0.2mm}\end{center}} 

% ---------------------------------------------------------------------		  
% Formatting of Itemized Lists		  
% ---------------------------------------------------------------------

 \newcommand{\step}[1]{\item[\addtocounter{itemcounter}{1}\arabic{itemcounter}.~]{#1}}
 
 \newcommand{\procedure}[1]{
 	\begin{itemize}
	{#1}
	\setcounter{itemcounter}{0}
	\end{itemize}}
	
% ---------------------------------------------------------------------
% Checkpoint set-up
% ---------------------------------------------------------------------

\newcommand{\firstcheckpoint}{
	\fbox{\begin{minipage}{0.1\textwidth} \vspace{0.25cm} B:\\[-0.2cm] \rule{\textwidth}{0.2mm} A:\\[-0.22cm]\end{minipage}}
 	\fbox{\begin{minipage}{0.2\textwidth}%\hspace{0.05cm}
 	\includegraphics[width=0.5\textwidth]{stop.png}
 	\end{minipage}\hspace{-1.5cm}
 	\begin{minipage}{0.75\textwidth}
 	{CHECKPOINT \addtocounter{checkpointcounter}{1} \arabic{checkpointcounter}: Make sure to submit the answers for Checkpoint 1 via D2L Dropbox 30 min prior to your lab at the latest.}
 	\end{minipage}}}

\newcommand{\checkpoint}{
	\fbox{\begin{minipage}{0.1\textwidth} \vspace{0.25cm} B:\\[-0.2cm] \rule{\textwidth}{0.2mm} A:\\[-0.22cm]\end{minipage}}
 	\fbox{\begin{minipage}{0.2\textwidth}%\hspace{0.05cm}
 	\includegraphics[width=0.5\textwidth]{stop.png}
 	\end{minipage}\hspace{-1.5cm}
 	\begin{minipage}{0.75\textwidth}
 	{CHECKPOINT \addtocounter{checkpointcounter}{1} \arabic{checkpointcounter}: Before moving on to the next part, discuss your results as a group, then have your TA evaluate your answers.}
 	\end{minipage}}}
	
\newcommand{\finalcheckpoint}{
	\fbox{\begin{minipage}{0.1\textwidth} \vspace{0.25cm} B:\\[-0.2cm] \rule{\textwidth}{0.2mm} A:\\[-0.22cm]\end{minipage}}
 	\fbox{\begin{minipage}{0.2\textwidth}%\hspace{0.05cm}
 	\includegraphics[width=0.5\textwidth]{stop.png}
 	\end{minipage}\hspace{-1.5cm}
 	\begin{minipage}{0.75\textwidth}
 	{Last Checkpoint! Before being dismissed from the lab, discuss your results as a group, then have your TA evaluate your answers.}
 	\end{minipage}}}

	
% ---------------------------------------------------------------------
% Title page set-up
% ---------------------------------------------------------------------

\renewcommand{\@maketitle}{%
\thispagestyle{empty}%
{\flushleft \fontsize{12}{0}\selectfont Name:~\rule{0.5\textwidth}{0.2mm}\hspace{3.3cm} Group \#:~\rule{0.1\textwidth}{0.2mm}\par \vspace{0.2cm}}


\begin{center}
{\begin{minipage}{0.16\textwidth}
{\includegraphics[width=\textwidth]{UofCLogo}}
\end{minipage}
\begin{minipage}{0.83\textwidth}
{\centering \hspace{-2.8cm}\fontsize{18}{0}\selectfont University of Calgary\\[0.3cm]
\hspace{-2.8cm}\fontsize{18}{0}\selectfont Department of Physics and Astronomy\\[0.3cm]
\hspace{-2.8cm}\fontsize{18}{0}\selectfont PHYS \@CourseNumber, \Semester\\[0.3cm]}
\end{minipage}}
\end{center}
\vspace{0.5cm}
{\centering \fontsize{18}{25}\selectfont {\bf \@LabatorialNumber: \@LabatorialTitle}\par}%
\vskip30pt%
\begin{minipage}{\@OverviewBoxWidth\textwidth}
{\fontsize{14}{0}\selectfont {\bf Overview:}\\ \vskip 5pt \fontsize{12}{14}\selectfont \@Overview\par}
\end{minipage}
\begin{minipage}{\@TitleGraphicBoxWidth \textwidth}
{\centering \includegraphics[width=\@TitleGraphicWidth \textwidth]{\@TitleGraphic} \par}
\begin{center}\begin{minipage}{\@TitleGraphicWidth \textwidth}
{\indent \fontsize{10}{0}\selectfont \@TitleGraphicCaption \par}
\end{minipage}\end{center}
\end{minipage}
\vskip 30pt%
{\fontsize{14}{0}\selectfont {\bf Pre-Lab Reading:}\\ \vskip 5pt \fontsize{12}{15}\selectfont \@Preparation\par}
\vskip 30pt%
{\fontsize{14}{0}\selectfont {\bf Equipment:}\\ \vskip 5pt \fontsize{12}{15}\selectfont \@Equipment\par}
}%

% ---------------------------------------------------------------------
% Defining the counters and initializing them to zero
% ---------------------------------------------------------------------

\newcounter{questioncounter}
\setcounter{questioncounter}{0}
\newcounter{checkpointcounter}
\setcounter{checkpointcounter}{0}
\newcounter{figurecounter}
\setcounter{figurecounter}{0}
\newcounter{itemcounter}
\setcounter{itemcounter}{0}














