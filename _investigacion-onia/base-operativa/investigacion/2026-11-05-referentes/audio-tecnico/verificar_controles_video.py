"""QA local de los cuatro probes; sólo lectura de medios, sin ASR/modelos/red."""
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
RATE=48000
FRAMES=6*RATE

def command(args):
    return subprocess.check_output(args)

def pcm(args):
    raw=command(['ffmpeg','-nostdin','-v','error',*args,'-c:a','pcm_f32le','-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4').reshape(-1,2).astype(np.float64)

def levels(x):
    rms=np.sqrt(np.mean(x*x,axis=0))
    return {'rms_per_channel':rms.tolist(),
            'rms_dbfs_per_channel':[float(20*np.log10(v)) if v else None for v in rms],
            'peak_per_channel':np.max(np.abs(x),axis=0).tolist()}

manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
previous={r['file']:r['sha256'] for r in manifest['files']}
controls=json.loads((OUT/'controles-video.json').read_text(encoding='utf-8'))
checks={}
rows=[]
decoded={}
mono_reference_equal=[]
for case in controls['cases']:
    path=BASE/case['file']
    key=path.stem[-1]
    p=json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    a=next(s for s in p['streams'] if s['codec_type']=='audio')
    v=next(s for s in p['streams'] if s['codec_type']=='video')
    full=pcm(['-i',str(path),'-map','0:a:0'])
    x=full[:FRAMES]
    decoded[key]=full
    source=MEDIA/case['source_audio']
    source_probe=json.loads(command(['ffprobe','-v','error','-show_streams','-of','json',str(source)]))
    source_channels=source_probe['streams'][0]['channels']
    filters=['aresample=48000']
    if source_channels==1:
        filters.append('pan=stereo|c0=c0|c1=c0')
    filters.append('apad')
    reference=pcm(['-ss',str(case['source_start_s']),'-i',str(source),'-af',','.join(filters),'-t','6'])
    if source_channels==1:
        mono_reference_equal.append(bool(np.array_equal(reference[:,0],reference[:,1])))
    actual_levels=levels(x)
    reference_levels=levels(reference)
    delta=[None if b is None else a-b for a,b in zip(actual_levels['rms_dbfs_per_channel'],reference_levels['rms_dbfs_per_channel'])]
    checks[key+'_encoding']=(a['codec_name']=='aac' and int(a['sample_rate'])==RATE and a['channels']==2
                              and a.get('channel_layout')=='stereo' and case['target_bitrate_bps']==128000)
    checks[key+'_six_seconds']=(float(p['format']['duration'])==6.0 and float(a['duration'])==6.0
                                and float(v['duration'])==6.0 and x.shape==(FRAMES,2))
    checks[key+'_video']=(v['codec_name']=='h264' and v['width']==320 and v['height']==180
                          and v['pix_fmt']=='yuv420p' and v['avg_frame_rate']=='1/1' and int(v['nb_frames'])==6)
    checks[key+'_no_unexpected_gain']=all(d is None or abs(d)<0.3 for d in delta)
    checks[key+'_source_unchanged']=(hashlib.sha256(source.read_bytes()).hexdigest()
                                    ==previous[source.relative_to(BASE).as_posix()])
    video_hash=command(['ffmpeg','-nostdin','-v','error','-i',str(path),'-map','0:v:0','-f','hash','-hash','sha256','-']).decode().strip()
    rows.append({'probe':path.name,'audio_codec':a['codec_name'],'sample_rate':int(a['sample_rate']),
                 'channels':a['channels'],'channel_layout':a['channel_layout'],
                 'target_bitrate_bps':128000,'reported_bitrate_bps':int(a['bit_rate']),
                 'container_duration_s':float(p['format']['duration']),
                 'full_decoded_audio_frames_per_channel':len(full),'evaluated_frames_per_channel':len(x),
                 'trailing_codec_padding_frames_excluded':len(full)-FRAMES,
                 'decoded_video_hash':video_hash,'decoded_aac_first6s':actual_levels,
                 'reference_resampled_pcm_first6s':reference_levels,
                 'decoded_lr_difference_peak':float(np.max(np.abs(x[:,0]-x[:,1]))),
                 'decoded_lr_difference_rms':float(np.sqrt(np.mean((x[:,0]-x[:,1])**2))),
                 'rms_delta_db_per_channel':delta})

checks['identical_video_decoded']=len({r['decoded_video_hash'] for r in rows})==1
checks['original_gray_video_preserved']=all(r['decoded_video_hash']=='SHA256=fa9492bcd213ea4a8af1b636b383acd03e8651595bdb5ef86f91ecae97a5c4d0' for r in rows)
checks['silence_decodes_to_exact_zero']=bool(np.count_nonzero(decoded['a'])==0)
tone=decoded['b'][RATE//4:FRAMES-RATE//4]
frequencies=np.fft.rfftfreq(len(tone),d=1/RATE)
peaks=[]
for channel in range(2):
    spectrum=np.abs(np.fft.rfft(tone[:,channel]*np.hanning(len(tone))))
    peaks.append(float(frequencies[np.argmax(spectrum)]))
checks['tone_approximately_440hz']=all(abs(f-440)<0.2 for f in peaks)
checks['mono_duplicated_exactly_before_lossy_aac']=len(mono_reference_equal)==3 and all(mono_reference_equal)
checks['other_media_unchanged']=controls['unchanged_other_media'] and all(
    hashlib.sha256((MEDIA/name).read_bytes()).hexdigest()==sha
    for name,sha in controls['unchanged_other_media_sha256'].items())

result={'scope':'Local codec/container/waveform QA only; no external submission, model or acoustic perception test.',
        'checks':checks,'pass':all(checks.values()),'tone_fft_peak_hz_per_channel':peaks,'cases':rows,
        'level_method':'No loudness/peak normalization, compressor, volume or limiter. Mono is copied at unity gain to each channel; stereo stays stereo. Per-channel RMS is compared to uncompressed resampling, before AAC. Small encoding/resampling changes are measured, not gain adjustments.',
        'stereo_power_note':'Duplicating mono adds a second equal channel; summed two-channel power is twice mono (+3.01dB), while each channel retains its original amplitude. Do not compare channel-summed power to mono as if normalization were applied.',
        'lossy_channel_note':'An initial sample-exact L/R check after AAC failed (25/26 checks). That expectation is not valid for lossy AAC. Exact duplication is now checked in the uncompressed reference; decoded channel differences are measured explicitly, not concealed or treated as perception.',
        'duration_limit':'Evaluate only [0,6) container seconds; exclude trailing AAC decoding padding from timed questions.',
        'blind_protocol':'Three known controls plus one real sample without validated semantic ground truth. Future submission: same neutral instruction for every clip, varied order, anonymous filenames only; do not send expectations, source identities, scripts or manifests. Accept continuous tone without demanding an exact 440Hz estimate.',
        'acceptance_limit':'Passing controls does not certify prosody, specific SFX, music accuracy or fine audiovisual sync; external authorization remains pending.'}
(OUT/'qa-controles-video.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pass':result['pass'],'checks_passed':sum(checks.values()),'checks_total':len(checks),
                  'tone_hz':peaks,'rms_delta_db':{r['probe']:r['rms_delta_db_per_channel'] for r in rows}},indent=2))
raise SystemExit(0 if result['pass'] else 1)
