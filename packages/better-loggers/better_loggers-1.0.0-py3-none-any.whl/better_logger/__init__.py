
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
import pprint
import shutil
import textwrap
import traceback
from typing import Callable, Optional, Tuple, Union
from logging import Logger, getLogger
from wcwidth import wcswidth


class Color:
    BLACK          = '\033[30m'#(文字)黒
    RED            = '\033[31m'#(文字)赤
    GREEN          = '\033[32m'#(文字)緑
    YELLOW         = '\033[33m'#(文字)黄
    BLUE           = '\033[34m'#(文字)青
    MAGENTA        = '\033[35m'#(文字)マゼンタ
    PURPLE         = '\033[35m'#(文字)パープル
    CYAN           = '\033[36m'#(文字)シアン
    WHITE          = '\033[37m'#(文字)白
    COLOR_DEFAULT  = '\033[39m'#文字色をデフォルトに戻す
    BOLD           = '\033[1m'#太字
    UNDERLINE      = '\033[4m'#下線
    INVISIBLE      = '\033[08m'#不可視
    REVERCE        = '\033[07m'#文字色と背景色を反転
    BG_BLACK       = '\033[40m'#(背景)黒
    BG_RED         = '\033[41m'#(背景)赤
    BG_GREEN       = '\033[42m'#(背景)緑
    BG_YELLOW      = '\033[43m'#(背景)黄
    BG_BLUE        = '\033[44m'#(背景)青
    BG_MAGENTA     = '\033[45m'#(背景)マゼンタ
    BG_CYAN        = '\033[46m'#(背景)シアン
    BG_WHITE       = '\033[47m'#(背景)白
    BG_DEFAULT     = '\033[49m'#背景色をデフォルトに戻す
    RESET          = '\033[0m'#全てリセット
    


#シングルトンロガー
@dataclass
class LogColors:
    ERROR=Color.RED
    INFO=Color.BLUE
    WARNING=Color.YELLOW
    DEBUG=Color.GREEN
    WTF=Color.PURPLE
    CRITICAL=Color.BG_BLUE+Color.WHITE
@dataclass
class LogEmojis:
    ERROR='🚫'
    INFO='📝'
    WARNING='🚨'
    DEBUG='🐛'
    WTF='🛸'
    CRITICAL='🔥'
@dataclass
class LogKanji(LogEmojis):
    ERROR=Color.RESET+Color.RED+'危'+Color.RESET+LogColors.ERROR
    INFO=Color.RESET+Color.BLUE+'情'+Color.RESET+LogColors.INFO
    WARNING=Color.RESET+Color.RED+'警'+Color.RESET+LogColors.WARNING
    DEBUG=Color.RESET+Color.GREEN+'調'+Color.RESET+LogColors.DEBUG
    WTF=Color.RESET+Color.BLUE+'驚'+Color.RESET+LogColors.WTF
    CRITICAL=Color.RESET+Color.RED+'死'+Color.RESET+LogColors.CRITICAL

@dataclass
class BetterLogArgs:
    messages: Tuple
    color:str
    project_root:Union[str,Path]
    width:int
    emoji:str
    header_text:Optional[object]
    tb:Optional[traceback.StackSummary]=None

def get_text_width(text):
    width = sum(wcswidth(char) for char in text)
    return width


class BetterLog:
    def __init__(self,messages: Tuple[object],color:str,project_root,width,emoji='',header_text:Optional[object]=None,tb:Optional[traceback.StackSummary]=None,formatter:Callable[[object],str]=pprint.pformat) -> None:
        self.width=width-2
        if self.width<=0:
            logger=getLogger(__name__)
            logger.warning('width is too small\n width is set to 3')
            self.width=1
        self.header_text=header_text
        filled_massages=[]
        for message in messages:
            w=width
            if emoji:
                w-=get_text_width(emoji)+2
            filled_massage=formatter(message)
            if get_text_width(filled_massage)>w:
                filled_massage='\n'+filled_massage+'\n'
            # filled_massage=textwrap.fill(filled_massage,width=self.width)
            filled_massages.append(filled_massage)
        self.emoji=emoji
        self.messages=filled_massages
        self.color=color
        self.tb=tb
        self.project_root=project_root
    def _top(self):
        output=''
        output+='┌'
        output+='─'*self.width
        output+='┐'
        output+='\n'
        return output
    def _text_center(self,text:str,width:int):
        remain_space=width-get_text_width(text)
        if remain_space<=0:
            return text
        left_space=remain_space//2
        right_space=remain_space-left_space
        return ' '*left_space+text+' '*right_space
    def _header(self):
        output=''
        output+=self._top()
        if self.header_text:
            header_texts=textwrap.fill(self.header_text.__str__(),width=self.width).split('\n')
            header_text=''
            for text in header_texts:
                header_text+='│'+self._text_center(text,self.width)+'│\n'
            output+=header_text
            output+='├'
            output+='─'*self.width
            output+='┤'
            output+='\n'
        return output
    def _traceback(self):
        output=''
        if not self.tb:
            return output
        for i,tb in enumerate(self.tb):
            trace=''
            trace+=f' #{i+1}'
            trace+='    '
            trace+=tb.name
            file=self._cut_file_path(tb.filename)
            file+=f':{tb.lineno} '
            for i in range(self.width-get_text_width(trace)-get_text_width(file)):
                trace+=' '
            trace+=file
            output+='│'+trace+'│\n'
        output+='├'
        output+='─'*self.width
        output+='┤'
        output+='\n'
        return output
    def _footer(self):
        output=''
        output+='└'
        output+='─'*self.width
        output+='┘'
        return output
    def _cut_file_path(self,file_path:str)->str:
        return os.path.relpath(file_path, start=self.project_root)
    def _left(self,text:str,emoji:str,width:int):
        width-=get_text_width(emoji)+2
        for i in range(get_text_width(text),width):
            text+=' '
        return ' '+emoji+' '+text
    def output(self):
        output=''
        output+=self.color
        output+=self._header()
        output+=self._traceback()
        for message in self.messages:
            output+='│'+self._left(message,self.emoji,self.width )+'│'
            output+='\n'
        output+=self._footer()
        output+=Color.RESET
        output+='\n'
        return output
    @staticmethod
    def from_args(args:BetterLogArgs):
        return BetterLog(args.messages,args.color,args.project_root,args.width,args.emoji,args.header_text,args.tb)


class BetterLogger:
    logo_colors=LogColors
    logo_emojis=LogEmojis
    def __init__(self,logger:Logger,fix_width:Optional[int]=None) -> None:
        self.logger=logger
        self.project_root_dir=os.getcwd()
        self.project_root_dir=Path(self.project_root_dir)
        self.fix_width=fix_width
    
    def _get_width(self):
        if self.fix_width:
            return self.fix_width
        return shutil.get_terminal_size().columns
    
    def _make_log(self,log_args:BetterLogArgs,use_traceback:bool):
        tb=log_args.tb
        if use_traceback and not tb:
            tb=traceback.extract_stack()[:-2]
        log_args.tb=tb#type:ignore because stack_summary is list[FrameSummary]
        log=BetterLog.from_args(log_args)
        return log.output()


    def debug(self,*messages,header_text:object='',use_traceback=False):
        args=BetterLogArgs(messages=messages,
                           color=self.logo_colors.DEBUG,
                           project_root=self.project_root_dir,
                           width=self._get_width(),
                           emoji=self.logo_emojis.DEBUG,
                           header_text=header_text,
                           )
        self.logger.debug(self._make_log(args,use_traceback))
    
    def info(self,*messages,header_text:object='',use_traceback=False):
        args=BetterLogArgs(messages=messages,
                           color=self.logo_colors.INFO,
                           project_root=self.project_root_dir,
                           width=self._get_width(),
                           emoji=self.logo_emojis.INFO,
                           header_text=header_text,
                           )
        self.logger.info(self._make_log(args,use_traceback))
    
    def warning(self,*messages,header_text:object='',use_traceback=True):
        args=BetterLogArgs(messages=messages,
                           color=self.logo_colors.WARNING,
                           project_root=self.project_root_dir,
                           width=self._get_width(),
                           emoji=self.logo_emojis.WARNING,
                           header_text=header_text,
                           )
        self.logger.warning(self._make_log(args,use_traceback))
    
    def error(self,*messages,header_text:object='',exception:Optional[Exception]=None,use_traceback=True):
        args=BetterLogArgs(messages=messages,
                           color=self.logo_colors.ERROR,
                           project_root=self.project_root_dir,
                           width=self._get_width(),
                           emoji=self.logo_emojis.ERROR,
                           header_text=header_text,
                           tb=traceback.extract_tb(exception.__traceback__) if exception else None
                           )
        self.logger.error(self._make_log(args,use_traceback))
    
    def wtf(self,*messages,header_text:object='',use_traceback=True):
        args=BetterLogArgs(messages=messages,
                           color=self.logo_colors.WTF,
                           project_root=self.project_root_dir,
                           width=self._get_width(),
                           emoji=self.logo_emojis.WTF,
                           header_text=header_text,
                           )
        self.logger.info(self._make_log(args,use_traceback))
    def critical(self,*messages,header_text:object='',exception:Optional[Exception]=None,use_traceback=True):
        args=BetterLogArgs(messages=messages,
                           color=self.logo_colors.CRITICAL,
                           project_root=self.project_root_dir,
                           width=self._get_width(),
                           emoji=self.logo_emojis.CRITICAL,
                           header_text=header_text,
                           tb=traceback.extract_tb(exception.__traceback__) if exception else None
                           )
        self.logger.critical(self._make_log(args,use_traceback))
def get_better_logger(name:Optional[str]=None,fix_width:Optional[int]=None):
    logger=getLogger(name)
    return BetterLogger(logger,fix_width)
