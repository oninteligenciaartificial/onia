"""Single fresh offline PANNs CPU entry; standard existing package, no auto-download."""
from pathlib import Path
import sys,json,hashlib,ctypes,os,time,wave
from unittest.mock import patch
O=Path(__file__).resolve().parent;R=O.parent;case=sys.argv[1];start=time.monotonic();S={'case':case,'stage':'validate','complete':False,'inference_calls':0}
def save():(O/(case+'-receipt.json')).write_text(json.dumps(S,indent=2)+'\n')
def no_system(cmd):raise RuntimeError('offline_autocommand_forbidden')
try:
 freeze=json.loads((O/'input-freeze.json').read_text());assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==freeze['adapter_sha256']
 entry=freeze['inputs'].get(case)
 if entry is None:entry=json.loads((O/(case+'-input.json')).read_text())
 path=Path(entry['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
 assert hashlib.sha256(Path(freeze['CSV']['installed_path']).read_bytes()).hexdigest()==freeze['CSV']['sha256']
 class Filter(ctypes.Structure):_fields_=[('code',ctypes.c_ushort),('jt',ctypes.c_ubyte),('jf',ctypes.c_ubyte),('k',ctypes.c_uint)]
 class Program(ctypes.Structure):_fields_=[('len',ctypes.c_ushort),('filter',ctypes.POINTER(Filter))]
 ins=[(0x20,0,0,4),(0x15,1,0,0xc000003e),(0x06,0,0,0x00050001),(0x20,0,0,0)]
 for nr in [41,42,44,46]:ins.extend([(0x15,0,1,nr),(0x06,0,0,0x00050001)])
 ins.append((0x06,0,0,0x7fff0000));arr=(Filter*len(ins))(*(Filter(*x) for x in ins));prog=Program(len(ins),arr);libc=ctypes.CDLL(None,use_errno=True)
 assert libc.prctl(38,1,0,0,0)==0 and libc.prctl(22,2,ctypes.byref(prog),0,0)==0
 import socket
 try:socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 except PermissionError:S['kernel_network_block']=True
 else:raise AssertionError('network_not_blocked')
 os.environ['MPLCONFIGDIR']=str(O/'matplotlib-cache');os.environ['NUMBA_CACHE_DIR']=str(O/'numba-cache')
 with patch.object(Path,'home',return_value=R/'panns-setup-v3/runtime-home'),patch('os.system',no_system):
  S['stage']='import';save();t=time.monotonic();import torch,numpy as np
  torch.set_num_threads(1);torch.set_num_interop_threads(1)
  from panns_inference import SoundEventDetection,labels
  assert len(labels)==527 and labels[freeze['CSV']['Speech_index']]=='Speech' and labels[freeze['CSV']['Music_index']]=='Music'
  S['import_seconds']=time.monotonic()-t;S['stage']='load_local_model';save();t=time.monotonic()
  model=SoundEventDetection(checkpoint_path=str(R/'panns-setup-v3/Cnn14_DecisionLevelMax_mAP=0.385.pth'),device='cpu',interpolate_mode='nearest')
  S['model_load_seconds']=time.monotonic()-t
  with wave.open(str(path),'rb') as w:
   assert w.getnchannels()==1 and w.getsampwidth()==2 and w.getframerate()==32000
   samples=w.getnframes();audio=np.frombuffer(w.readframes(samples),dtype='<i2').astype(np.float32)/32768.0
  S['input_samples']=samples;S['stage']='inference';save();t=time.monotonic();S['inference_calls']=1;save()
  frames=model.inference(audio[None,:]);S['inference_seconds']=time.monotonic()-t
  assert frames.ndim==3 and frames.shape[0]==1 and frames.shape[2]==527 and np.isfinite(frames).all()
  curves=frames[0];times=np.arange(len(curves),dtype=np.float64)*.01
  np.savez_compressed(O/(case+'-all527.npz'),framewise=curves,times_seconds=times,labels=np.asarray(labels))
  selected={name:{'max':float(curves[:,labels.index(name)].max()),'mean':float(curves[:,labels.index(name)].mean()),'argmax_seconds':float(times[curves[:,labels.index(name)].argmax()])} for name in ['Speech','Music']}
  if case=='voice':selected['Speech'].update(voice_interval_mean=float(curves[(times<.8639375),labels.index('Speech')].mean()),final_silence_mean=float(curves[(times>=1)&(times<2),labels.index('Speech')].mean()))
  with open(O/(case+'-Speech-Music.csv'),'x') as f:
   f.write('time_seconds,Speech,Music\n')
   for t,row in zip(times,curves):f.write(f'{t:.2f},{row[labels.index("Speech")]:.9g},{row[labels.index("Music")]:.9g}\n')
  S.update(complete=True,stage='complete',frame_shape=list(frames.shape),selected=selected,classes_max={label:float(curves[:,i].max()) for i,label in enumerate(labels)},time_scope='model hop10ms/interpolated nearest, not calibrated temporal resolution; last padded output frame can touch duration boundary')
except BaseException as exc:S.update(error_type=type(exc).__name__,safe_error=str(exc))
finally:S['elapsed_seconds']=time.monotonic()-start;save();print(json.dumps({k:v for k,v in S.items() if k!='classes_max'},indent=2),flush=True)
sys.exit(0 if S['complete'] else 1)
