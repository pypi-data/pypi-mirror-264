# 具有类型注释功能的ArgParse: ArgChecker
import sys
from typing import Any, Optional, Union
    
class ArgChecker:
    @staticmethod
    def __cast(v:str)->'Union[None,bool,int,float,str]':
        if v=="True": return True
        if v=="False": return False
        if v=="None": return None
        try:
            return int(v)
        except:
            pass
        try:
            return float(v)
        except:
            return v.strip('"')
    @staticmethod
    def get_dict()->'dict[str,Union[str,Any]]':
        '''将输入参数以字典的形式返回'''
        cur_key=None
        ret={}
        for v in sys.argv[1:]:                
            if v.startswith('-'):
                if cur_key!=None:
                    ret[cur_key]=True
                cur_key=v.strip('-')
            elif cur_key!=None:
                ret[cur_key]=ArgChecker.__cast(v)
                cur_key=None
            else:
                raise ValueError(f"无效参数'{v}'")
        if cur_key!=None: ret[cur_key]=True
        return ret
    
    def __init__(self,pars: 'Optional[dict[str,Any]]'=None):
        self.__args=self.get_dict() if pars is None else pars
    
    def pop_bool(self, key: str) -> bool:
        if self.__args.pop(key, False): return True
        return False
    
    def pop_int(self, key: str, default: Optional[int] = None) -> int:
        val = self.__args.pop(key, default)
        if val is None: raise ValueError(f"必须指定'{key}'参数")
        return int(val)
    
    def pop_str(self, key: str, default: Optional[str]=None) -> str:
        val = self.__args.pop(key, default)
        if val is None: raise ValueError(f"必须指定'{key}'参数")
        return str(val)
   
    def pop_float(self, key: str, default: Optional[float] = None) -> float:
        val = self.__args.pop(key, default)
        if val is None: raise ValueError(f"必须指定'{key}'参数")
        return float(val)
    
    def empty(self) -> bool:
        return len(self.__args) == 0
    
    def keys(self): return self.__args.keys()
    def values(self): return self.__args.values()
    def items(self): return self.__args.items()

    def __str__(self):
        return str(self.__args)