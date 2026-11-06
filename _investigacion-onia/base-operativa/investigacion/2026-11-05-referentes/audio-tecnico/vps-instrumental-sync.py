import cv2,numpy as np,wave,subprocess,json,resource,time,os
sr=16000; fps=24; t0=time.monotonic(); out={}; d='/work/output'; tt=np.arange(sr*4)/sr
x=.2*np.sin(2*np.pi*np.where(tt<2,440,880)*tt)
for p in [1,2,3]: pass
pulses=np.zeros(sr*4)
for p in (1,2,3): pulses[int(p*sr):int(p*sr)+160]=.5
onsets=(np.where((np.abs(pulses[1:])>.1)&(np.abs(pulses[:-1])<=.1))[0]+1)/sr
out['pulses']={'observed':onsets.tolist(),'expected':[1,2,3]}
a=.1*np.sin(2*np.pi*440*tt); b=.2*np.sin(2*np.pi*880*tt)
out['level_delta_db']=float(20*np.log10(np.sqrt(np.mean(b*b))/np.sqrt(np.mean(a*a))))
for shift in (0,.25):
 name='sync-'+str(int(shift*1000)); v=d+'/'+name+'.avi'; w=d+'/'+name+'.wav'; mux=d+'/'+name+'.mkv'
 writer=cv2.VideoWriter(v,cv2.VideoWriter_fourcc(*'MJPG'),fps,(320,180))
 for i in range(fps*4):
  image=np.zeros((180,320,3),np.uint8)
  if i in (24,48,72): image[:]=255
  writer.write(image)
 writer.release(); a=np.zeros(sr*4,dtype=np.int16)
 for p in (1,2,3): a[int((p+shift)*sr):int((p+shift)*sr)+160]=16000
 with wave.open(w,'wb') as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(a.tobytes())
 subprocess.run(['ffmpeg','-loglevel','error','-nostdin','-i',v,'-i',w,'-c:v','copy','-c:a','pcm_s16le',mux],check=True,timeout=30)
 cap=cv2.VideoCapture(mux); flashes=[]; i=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  if frame.mean()>200:flashes.append(i/fps)
  i+=1
 cap.release(); decoded=subprocess.run(['ffmpeg','-loglevel','error','-i',mux,'-vn','-f','s16le','-ac','1','-ar','16000','-'],check=True,stdout=subprocess.PIPE,timeout=30).stdout
 y=np.frombuffer(decoded,dtype='<i2'); inds=np.where((np.abs(y[1:].astype(int))>1000)&(np.abs(y[:-1].astype(int))<=1000))[0]+1; attacks=inds/sr
 out[name]={'flash_seconds':flashes,'attack_seconds':attacks.tolist(),'offset_seconds':(attacks-np.array(flashes)).tolist(),'frame_count':i}
out['elapsed_seconds']=time.monotonic()-t0;out['max_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
with open(d+'/instrument-sync.json','x') as f:json.dump(out,f,indent=2)
print(json.dumps(out))
