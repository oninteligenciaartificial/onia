"""Lectura local BF16 por numpy para evitar slicing de torch storage en offload.

Sólo reemplaza la ruta safetensors de Accelerate; mantiene el fallback original.
No modifica pesos ni paquetes instalados. Rechaza dtypes no examinados.
"""
import json
import struct
import numpy as np
import torch
from accelerate.utils.offload import OffloadedWeightsLoader

_original=OffloadedWeightsLoader.__getitem__
_headers={}

def _get(self,key):
    if key in self.state_dict:
        return self.state_dict[key]
    info=self.index[key]
    filename=info.get('safetensors_file')
    if filename is None:
        return _original(self,key)
    if filename not in _headers:
        with open(filename,'rb') as f:
            header_size=struct.unpack('<Q',f.read(8))[0]
            header=json.loads(f.read(header_size))
        _headers[filename]=(8+header_size,header)
    start,header=_headers[filename]
    entry=header[info.get('weight_name',key)]
    if entry['dtype']!='BF16':
        raise ValueError('dtype de offload no examinado: '+entry['dtype'])
    off0,off1=entry['data_offsets']
    mapping=np.memmap(filename,dtype='<u2',mode='r',offset=start+off0,shape=tuple(entry['shape']))
    tensor=torch.from_numpy(np.array(mapping,copy=True)).view(torch.bfloat16)
    if 'dtype' in info:
        tensor=tensor.to(getattr(torch,info['dtype']))
    device='cpu' if self.device is None else self.device
    return tensor.to(device) if tensor.device!=torch.device(device) else tensor

def install():
    OffloadedWeightsLoader.__getitem__=_get
