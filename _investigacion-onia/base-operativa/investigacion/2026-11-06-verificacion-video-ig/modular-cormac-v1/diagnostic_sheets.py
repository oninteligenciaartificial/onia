import json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
points=[598,710,790,870,1082,1780,2096]
for i,frame in enumerate(points):
    args=['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-filter_complex_threads','1']
    for n in [i*2+1,i*2+2]:args+=['-threads','1','-i',str(R/f'diagnostic-{n:02d}.png')]
    args+=['-filter_complex','[0:v]scale=540:-1[a];[1:v]scale=540:-1[b];[a][b]hstack=inputs=2','-frames:v','1','-threads','1',str(R/f'low-{frame}.png')]
    subprocess.run(args,check=True)
print(json.dumps({'points':points,'pair_order':['frame-1','frame'],'purpose':'diagnostic subthreshold points, same all-frame scan; not rerun detector'}))
