% Ysy风格LaTeX样式
% v1.3.0发行版
% 有很多话想写在这里，但是我太懒了，以后有机会再写吧……
% 作者：Github@pifuyuini
% 时间：2025年6月1日

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{YsyClass}[2025/06/01 YSY Universal Class]

% 基类
\LoadClass[11pt,a4paper]{article} 

% 用户接口
\input{ysy-latex/modules/YsyOptions}

% 导入必要的包
\input{ysy-latex/modules/YsyPackages}

% 字体
\input{ysy-latex/modules/YsyLanguage}

% 颜色主题
\input{ysy-latex/modules/YsyColor}

% 颜色盒子
\input{ysy-latex/modules/YsyBox}

% 主题UI
\input{ysy-latex/modules/YsyUI}

% 其它设置
\input{ysy-latex/modules/YsySettings}

% 封面
\ifdefstring{\Ysy@type}{universal}{
	\input{ysy-latex/modules/YsyCoverPage}
}{\relax}
\ifdefstring{\Ysy@type}{flab}{
	\input{ysy-latex/modules/FLCoverPage}
}{\relax}
\ifdefstring{\Ysy@type}{paper}{
	\input{ysy-latex/modules/YsyPaperCoverPage}
}{\relax}

