import torch,json,time,resource
from conette import CoNeTTEConfig,CoNeTTEModel
torch.set_num_threads(1);torch.set_num_interop_threads(1);t=time.monotonic()
cfg=CoNeTTEConfig.from_pretrained('/work/model',local_files_only=True)
m=CoNeTTEModel.from_pretrained('/work/model',config=cfg,device='cpu',offline=True,local_files_only=True).eval()
load=time.monotonic()-t
with torch.inference_mode():out=m(torch.zeros(1,128000),sr=32000,task='audiocaps',beam_size=3,min_pred_size=3,max_pred_size=20)
print(json.dumps({'caption':out['cands'],'task':out['tasks'],'load_s':load,'elapsed_s':time.monotonic()-t,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},default=str))
