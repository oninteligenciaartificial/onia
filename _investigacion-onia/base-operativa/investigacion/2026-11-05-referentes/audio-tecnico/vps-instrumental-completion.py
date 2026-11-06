import av,cv2,numpy as np,librosa,json,time,resource,subprocess,wave
cv2.setNumThreads(1);cv2.ocl.setUseOpenCL(False); sr=16000;t=time.monotonic();out={};tt=np.arange(sr*4)/sr
x=np.concatenate((.2*np.sin(2*np.pi*440*tt[:2*sr]),.2*np.sin(2*np.pi*880*tt[:2*sr])))
out['step_hz']=[float(np.median(librosa.yin(y,sr=sr,fmin=80,fmax=1000,frame_length=1024,hop_length=160,center=False))) for y in (x[sr//2:sr*3//2],x[sr*5//2:sr*7//2])]
a=.1*np.sin(2*np.pi*440*tt);b=.2*np.sin(2*np.pi*880*tt); mix=a+b
spec=np.abs(np.fft.rfft(mix));f=np.fft.rfftfreq(len(mix),1/sr);powers=[float(spec[np.argmin(abs(f-q))]) for q in (440,880)];out['mix_delta_db']=20*np.log10(powers[1]/powers[0])
for name in ['probe-a','probe-b']:
 cap=cv2.VideoCapture('/work/input/'+name+'.mp4'); prev=None;vals=[];excluded=0;seq=[];n=0
 while True:
  ok,fr=cap.read()
  if not ok:break
  h=cv2.cvtColor(fr,cv2.COLOR_BGR2HSV);g=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY);mask=cv2.inRange(h,(20,150,100),(35,255,255));yellow=cv2.countNonZero(mask)>100
  if prev is not None:
   cut=np.mean(cv2.absdiff(prev[0],g))>5
   if yellow and prev[1] and not cut:
    flow=cv2.calcOpticalFlowFarneback(prev[0],g,None,.5,3,15,3,5,1.2,0);vals.append(float(np.median(flow[...,0][mask>0])))
   else:excluded+=1
  prev=(g,yellow);n+=1
 cap.release();out[name]={'frames':n,'flow_pairs':len(vals),'excluded_pairs':excluded,'positive':sum(v>0 for v in vals),'negative':sum(v<0 for v in vals)}
for offset in (0,.25):
 v=f'/work/output/pts-{offset}.avi';w=f'/work/output/pts-{offset}.wav';m=f'/work/output/pts-{offset}.mkv';writer=cv2.VideoWriter(v,cv2.VideoWriter_fourcc(*'MJPG'),24,(320,180))
 for i in range(240):
  fr=np.zeros((180,320,3),np.uint8)
  if i in (24,72,120,168,216):fr[:]=255
  writer.write(fr)
 writer.release();y=np.zeros(sr*10,dtype=np.int16)
 for p in (1,3,5,7,9):y[int((p+offset)*sr):int((p+offset)*sr)+160]=16000
 with wave.open(w,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(y.tobytes())
 subprocess.run(['ffmpeg','-loglevel','error','-nostdin','-i',v,'-i',w,'-c:v','copy','-c:a','pcm_s16le',m],check=True,timeout=30)
 c=av.open(m); flashes=[]; attacks=[];last=False
 for frame in c.decode(video=0):
  if frame.to_ndarray(format='gray').mean()>200:flashes.append(float(frame.pts*frame.time_base))
 c.close();c=av.open(m)
 for frame in c.decode(audio=0):
  z=frame.to_ndarray().reshape(-1);active=np.abs(z.astype(int))>1000
  inds=np.flatnonzero(active & ~np.r_[last,active[:-1]])
  attacks.extend(float(frame.pts*frame.time_base)+float(i)/frame.sample_rate for i in inds);last=bool(active[-1])
 c.close();out[str(offset)]={'flash_pts':flashes,'attack_pts':attacks,'offsets':[round(a-b,6) for a,b in zip(attacks,flashes)]}
out['elapsed']=time.monotonic()-t;out['max_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
with open('/work/output/instrument-completion.json','x') as f:json.dump(out,f,indent=2)
print(json.dumps(out))
