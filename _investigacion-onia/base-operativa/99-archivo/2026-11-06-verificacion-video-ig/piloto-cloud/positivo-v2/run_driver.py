from pathlib import Path
import builtins,json
from unittest.mock import patch
R=Path('/workspace/onia-av-pilot-20261106');O=R/'positivo-v2'
old=R/'positivo-v1/model-invocation.json';new=O/'model-invocation.json'
assert not old.exists() and not new.exists()
real_open=builtins.open
def routed_open(path,*args,**kwargs):
 try: path=new if Path(path)==old else path
 except TypeError:pass
 return real_open(path,*args,**kwargs)
source=O/'model_driver.py'
with patch('builtins.open',routed_open):
 exec(compile(source.read_bytes(),str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
