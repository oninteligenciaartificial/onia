import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cases=[('a','01',[450,1800,650,150],'subtitle opening'),('b','02',[340,1800,700,140],'subtitle desktop'),('c','03',[360,870,650,130],'repository title'),('d','02',[875,737,370,50],'small dictionary title'),('e','05',[330,1800,800,140],'subtitle later'),('f','01',[850,20,500,220],'negative no text')]
rows=[]
for case,frame,rect,purpose in cases:
    x,y,w,h=rect;source=ROOT/f'frame-{frame}.png';dest=ROOT/f'crop-{case}.png'
    command=['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-threads','1','-filter_threads','1','-i',str(source),'-vf',f'crop={w}:{h}:{x}:{y}','-frames:v','1','-threads','1',str(dest)]
    subprocess.run(command,check=True)
    rows.append({'case':case,'source':source.name,'rect_xywh':rect,'crop':dest.name,'purpose':purpose,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
log=(ROOT/'stages/reference_frames/stderr.log').read_text()
pts=re.findall(r'n:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([\d.]+)',log)
(ROOT/'crop-selection.json').write_text(json.dumps({'selection_before_ocr':True,'source_frame_indices':[30,270,510,780,1710],'showinfo_pts':pts,'cases':rows},indent=2)+'\n')
print(json.dumps(rows))
