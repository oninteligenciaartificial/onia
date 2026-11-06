import cv2, numpy as np, librosa, json, time, resource, hashlib
cv2.setNumThreads(1); cv2.ocl.setUseOpenCL(False)
t=time.monotonic(); sr=16000; n=sr*4; x=np.arange(n)/sr
r={'audio':{},'video':{}}
def f0(y):
 rms=np.sqrt(np.mean(y*y)); return None if rms<0.001 else float(np.median(librosa.yin(y,sr=sr,fmin=80,fmax=1000,frame_length=1024,hop_length=160,center=False)))
for name,y in [('silence',np.zeros(n)),('440',.2*np.sin(2*np.pi*440*x)),('880',.2*np.sin(2*np.pi*880*x))]: r['audio'][name]={'rms':float(np.sqrt(np.mean(y*y))),'f0':f0(y)}
for name in ['probe-a','probe-b']:
 p='/work/input/'+name+'.mp4'; cap=cv2.VideoCapture(p); prev=None; seq=[]; dirs=[]; count=0
 while True:
  ok,frame=cap.read()
  if not ok: break
  hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV); gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  masks={'red':cv2.inRange(hsv,(0,150,100),(10,255,255)),'green':cv2.inRange(hsv,(35,150,100),(85,255,255)),'blue':cv2.inRange(hsv,(100,150,100),(140,255,255)),'yellow':cv2.inRange(hsv,(20,150,100),(35,255,255))}
  counts={k:cv2.countNonZero(v) for k,v in masks.items()}; lab=max(counts,key=counts.get) if max(counts.values())>100 else 'gray'
  if not seq or seq[-1]!=lab: seq.append(lab)
  if prev is not None and lab=='yellow' and prev[1]=='yellow':
   flow=cv2.calcOpticalFlowFarneback(prev[0],gray,None,.5,3,15,3,5,1.2,0); vals=flow[...,0][masks['yellow']>0]; dirs.append(float(np.median(vals)))
  prev=(gray,lab); count+=1
 cap.release(); r['video'][name]={'frames':count,'sequence':seq,'flow_pairs':len(dirs),'positive':sum(v>0 for v in dirs),'negative':sum(v<0 for v in dirs)}
r['elapsed_seconds']=time.monotonic()-t; r['max_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
with open('/work/output/instrument-partial.json','x') as f:json.dump(r,f,indent=2)
print(json.dumps(r))
