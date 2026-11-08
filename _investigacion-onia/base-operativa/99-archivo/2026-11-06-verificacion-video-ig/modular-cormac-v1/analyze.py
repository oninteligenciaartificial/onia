import hashlib,json,os,re,subprocess
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parent
BASE=R.parents[2]
source=BASE/'operacion/reels-e-ideas/DfWLWspIruU/DfWLWspIruU.mp4'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e'
probe=json.loads((R/'stages/probe/stdout.log').read_bytes());stream=probe['streams'][0]
rows=json.loads((R/'all-frame-scores.json').read_bytes())['frames']
assert len(rows)==int(stream['nb_frames'])==2264
assert [r['frame']for r in rows]==list(range(2264))
assert all(r['pts']==r['frame']*256 for r in rows)
assert all('score'in r and 'mafd'in r for r in rows)
tb=Fraction(stream['time_base']);end=Fraction(2264,60)
native_checks={}
expected={'reference_frames':[30,270,510,780,1710],'neighbors':[j for n in [208,432,568,880,1300]for j in range(n-2,n+3)],'diagnostic_neighbors':[j for n in [598,710,790,870,1082,1780,2096]for j in [n-1,n]]}
for stage,indices in expected.items():
    log=(R/'stages'/stage/'stderr.log').read_text()
    observed=re.findall(r'n:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([\d.]+)',log)
    assert len(observed)==len(indices),(stage,len(observed))
    assert all(int(o[1])==n*256 for o,n in zip(observed,indices)),stage
    native_checks[stage]={'frames':indices,'pts_verified':True,'time_base':str(tb)}
boundaries=[]
annotations=[(208,'content_cut','presenter to desktop'),(432,'content_cut','desktop to repository'),(568,'abrupt_reframe','same repository, abrupt framing/finger discontinuity'),(880,'content_cut','repository to presenter'),(1082,'subthreshold_pose_or_reframe','same presenter; pose/framing discontinuity, edit versus fast movement not independently proven'),(1300,'abrupt_reframe','presenter close framing to wider framing'),(1780,'subthreshold_pose_or_reframe','same presenter, hand/pose discontinuity; edit provenance uncertain'),(2096,'subthreshold_pose_or_reframe','same presenter, head/pose discontinuity; edit provenance uncertain')]
for n,kind,note in annotations:
    boundaries.append({'frame':n,'pts':n*256,'pts_seconds':float(n*256*tb),'previous_frame_seconds':float((n-1)*256*tb),'score':rows[n]['score'],'threshold_candidate':rows[n]['score']>=10,'kind':kind,'visual_annotation':note,'one_native_frame_seconds':1/60})
macro=[]
for a,b,label in [(0,208,'presenter hook'),(208,432,'desktop insert'),(432,880,'repository/documentation'),(880,2264,'presenter explanation and closing')]:
    macro.append({'start_frame':a,'end_frame_exclusive':b,'start_s':a/60,'end_s':b/60,'duration_s':(b-a)/60,'label':label})
fine=[];limits=[0]+[x[0]for x in annotations]+[2264]
for a,b in zip(limits,limits[1:]):fine.append({'start_frame':a,'end_frame_exclusive':b,'duration_s':(b-a)/60})
cut_report={'all_frames_processed':2264,'video_duration_s':float(end),'container_duration_s':float(probe['format']['duration']),'time_base':str(tb),'frame_duration_s':1/60,'detection_scale':[720,1280],'native_source_scale':[1440,2560],'threshold':10,'threshold_candidates':[r for r in rows if r['score']>=10],'manual_boundaries':boundaries,'macro_blocks':macro,'fine_visual_segments_not_proven_distinct_camera_takes':fine,'diagnostic_non_cuts':{'598':'finger gesture, same monitor content','710':'camera/content drift, same repository','790':'scroll with source-image ghosting','870':'scroll with source-image ghosting'},'screening_scope':'Five primary candidates and seven diagnostic subthreshold points reviewed. Does not prove exhaustive recall of all low-contrast edits.','hard_content_cuts_confirmed':3,'primary_abrupt_reframes':2,'subthreshold_discontinuities':3,'subthreshold_discontinuities_not_all_certified_hard_edits':True,'native_pts_checks':native_checks}
(R/'cuts-reviewed.json').write_text(json.dumps(cut_report,indent=2)+'\n')
P=BASE/'operacion/modular-cormac-v1/tesseract';packages=[]
for archive in sorted((P/'packages').glob('*.deb')):
    package=subprocess.check_output(['dpkg-deb','-f',str(archive),'Package'],text=True).strip()
    raw=subprocess.check_output(['apt-cache','show','--no-all-versions',package],text=True)
    fields=dict(line.split(': ',1)for line in raw.splitlines()if ': 'in line and not line.startswith(' '))
    sha=hashlib.sha256(archive.read_bytes()).hexdigest();assert sha==fields['SHA256']
    packages.append({'package':package,'version':fields['Version'],'bytes':archive.stat().st_size,'sha256':sha,'APT_expected_sha256':fields['SHA256']})
tools={'packages':packages,'downloaded_package_bytes':sum(p['bytes']for p in packages),'effective_uid':os.geteuid(),'global_install':False,'sudo_or_privilege_escalation':False,'isolated_prefix':str(P),'engine_sha256':hashlib.sha256((P/'usr/bin/tesseract').read_bytes()).hexdigest(),'eng_traineddata_sha256':hashlib.sha256(next(P.rglob('eng.traineddata')).read_bytes()).hexdigest(),'copyright_files':[str(x.relative_to(P))for x in (P/'usr/share/doc').rglob('copyright')]}
(R/'tools-verified.json').write_text(json.dumps(tools,indent=2)+'\n')
ocr=json.loads((R/'ocr-results.json').read_bytes())
summary={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cuts':{'content':3,'primary_reframes':2,'subthreshold_discontinuities':3},'ocr_cases':6,'ocr_exact_matches':sum(x['literal_match_whitespace_collapsed']for x in ocr['results']),'ocr_negative_empty':ocr['results'][-1]['text']=='','reference_hash':hashlib.sha256((R/'ocr-reference.json').read_bytes()).hexdigest(),'reference_before_ocr':True,'new_asr_or_av_inferences':0,'exact_typeface_unknown':True,'speech_music_prosody_sync_not_evaluated':True}
(R/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
