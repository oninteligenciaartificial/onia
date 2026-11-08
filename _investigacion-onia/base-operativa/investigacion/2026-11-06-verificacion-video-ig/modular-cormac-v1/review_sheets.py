import json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
for i,frame in enumerate([208,432,568,880,1300]):
    sources=[R/f'neighbor-{n:02d}.png' for n in [i*5+2,i*5+3,i*5+4]]
    args=['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-filter_complex_threads','1']
    for p in sources:args+=['-threads','1','-i',str(p)]
    args+=['-filter_complex','[0:v]scale=480:-1[a];[1:v]scale=480:-1[b];[2:v]scale=480:-1[c];[a][b][c]hstack=inputs=3','-frames:v','1','-threads','1',str(R/f'cut-{frame}.png')]
    subprocess.run(args,check=True)
print(json.dumps({'sheets':5,'each_order':['candidate-1','candidate','candidate+1'],'source_native_neighbors_retained':True}))
