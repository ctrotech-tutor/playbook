"""Run after the private Orca session exits, to avoid buffered-trace attribution errors."""
from pathlib import Path
import json,re,gzip,hashlib,wave
R=Path.cwd();src=R/'.cache/orca';out=Path(__file__).resolve().parent/'orca-evidence';out.mkdir(exist_ok=True)
r=json.loads((src/'report.json').read_text());raw=(src/'orca-debug.log').read_bytes();text=raw.decode(errors='replace')
starts=list(re.finditer(r'^\d{2}:\d{2}:\d{2}\.\d{6} - ',text,re.M));utterances=[]
for i,m in enumerate(starts):
    block=text[m.start():starts[i+1].start() if i+1<len(starts) else len(text)].rstrip()
    if ' - SPEECH OUTPUT: ' in block:utterances.append({'clock':block[:15],'text':block})
expected=[['Skip to main content'],['main content'],['Find a page or feature dialog','Search chapters and reference entries'],['2 matches'],['Search button'],['expanded'],['collapsed'],['Try the markup','Close example button'],['Try the markup button']]
findings=[]
for case,tokens in zip(r['cases'],expected):
    selected=[u['text'] for u in utterances if case['trace_window_start_local']<=u['clock']<=case['trace_window_end_local']]
    case['orca_speech_lines']=selected;case['expected_trace_fragments']=tokens
    case['trace_result']='EXPECTED_FRAGMENTS_OBSERVED' if all(any(token in s for s in selected) for token in tokens) else 'NEEDS_TRIAGE_EXPECTED_FRAGMENT_NOT_OBSERVED'
    if case['trace_result'].startswith('NEEDS_TRIAGE'):findings.append({'id':'AT-01','case':case['id'],'status':'NEEDS_TRIAGE','observation':'Keyboard focus reached the skip link, but its expected link label was not observed in this bounded Orca speech window. Determine whether page-load timing, browser focus events or Orca presentation explain this before attributing a site defect.','independent_review':False})
    if case['id']=='practice-lab-opens-with-native-keyboard' and any('<!doctype html>' in s for s in selected):
        findings.append({'id':'AT-02','case':case['id'],'status':'NEEDS_HUMAN_REVIEW','observation':'Orca submitted the example source as part of its opening-dialog utterance before announcing Close example. The dialog has an explicit label. Assess interruption, verbosity and editor navigation with actual listeners before deciding whether a presentation change is needed. This is not an established WCAG failure.'})
r.pop('orca_speech_line_count',None);r['orca_speech_utterance_count']=len(utterances);r['trace_assignment']='Complete multiline utterances parsed after session teardown and assigned by local-clock start/end windows; not by live buffered-file offsets. Session did not cross midnight.'
r['raw_trace_sha256']=hashlib.sha256(raw).hexdigest();r['open_observations']=findings;r['result']='BOUNDED_KEYBOARD_AND_ORCA_TRACE_WITH_OPEN_OBSERVATIONS' if findings else 'BOUNDED_KEYBOARD_AND_ORCA_TRACE_PENDING_HUMAN_REVIEW'
r['human_listener']=False;r['independent']=False
(out/'assessment.json').write_text(json.dumps(r,indent=2)+'\n');(out/'speech-output.txt').write_text('\n\n'.join(u['text'] for u in utterances)+'\n')
(out/'orca-debug.log.gz').write_bytes(gzip.compress(raw,mtime=0));pcm=(src/'speech.raw').read_bytes();(out/'speech-s16le-16000hz-mono.pcm.gz').write_bytes(gzip.compress(pcm,mtime=0))
(out/'audio.json').write_text(json.dumps({'format':'signed 16-bit little-endian PCM','rate':16000,'channels':1,'seconds':len(pcm)/32000,'pcm_sha256':hashlib.sha256(pcm).hexdigest(),'origin':'Actual private PulseAudio monitor recording of the Orca/speech-dispatcher/eSpeak session, not generated narration.','human_listened':False},indent=2)+'\n')
for name in ['session.log','at-spi-applications.txt','orca-console.log']:
    if (src/name).exists():(out/name).write_bytes((src/name).read_bytes())
print(r['result'],len(r['cases']),'keyboard checks;',len(utterances),'speech utterances;',len(findings),'open observations')
for c in r['cases']:print(c['id'],c['trace_result'])
