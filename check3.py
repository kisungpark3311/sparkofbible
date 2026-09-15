import json
import re
import os
import bs4

template_path = r'D:\code\.agents\skills\thought-essay-html\templates\essay_template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template_html = f.read()

subagents = {
    '01_성경적 사고와 인격 만들기_에베소서_1_1-14_세낱말이이백단어를진다_인격만들기_에세이.html': r'C:\Users\user\.gemini\antigravity-cli\brain\752b4f10-f4a2-446b-9e46-2a9b64b7c6e4\.system_generated\logs\transcript_full.jsonl',
    '06_성경적 사고와 인격 만들기_에베소서_3_14-21_앎이종점이될수없었다_인격만들기_에세이.html': r'C:\Users\user\.gemini\antigravity-cli\brain\88c63594-77fc-4a28-aa2f-1eab0ca6b01d\.system_generated\logs\transcript_full.jsonl',
    '14_성경적 사고와 인격 만들기_에베소서_6_1-9_같은이름에표지가붙는다_인격만들기_에세이.html': r'C:\Users\user\.gemini\antigravity-cli\brain\fb19ad8b-2aa4-4fdf-b75b-11e5d9febefe\.system_generated\logs\transcript_full.jsonl'
}

for fn, tpath in subagents.items():
    raw_text = None
    if os.path.exists(tpath):
        with open(tpath, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if 'tool_calls' in data:
                    for call in data['tool_calls']:
                        name = call.get('name') or call.get('function', {}).get('name')
                        if name and 'write_to_file' in name:
                            args = call.get('args') or call.get('function', {}).get('arguments')
                            if isinstance(args, str):
                                try: args = json.loads(args)
                                except: continue
                            if isinstance(args, dict) and 'CodeContent' in args:
                                cc = args['CodeContent']
                                if 'article' in cc or '<h1>' in cc or '#' in cc:
                                    if raw_text is None or len(cc) > len(raw_text):
                                        raw_text = cc
                                        
    if raw_text:
        m = re.search(r'^(\d+)_.*?_([가-힣]+)_(\d+)_(\d+)-(\d+)(?:_(\d+))?', fn)
        idx = m.group(1)
        book = m.group(2)
        c = m.group(3)
        v1 = m.group(4)
        c2_v2 = m.group(5)
        v2 = m.group(6)
        if v2: ref = f'{book} {c}:{v1}~{c2_v2}:{v2}'
        else: ref = f'{book} {c}:{v1}-{c2_v2}'
        date_str = f'에베소서 제 {idx}편'
        type_label = '성경적 사고와 인격 만들기'
        
        title_match = re.search(r'#\s*(.+)', raw_text)
        title = title_match.group(1).strip() if title_match else '묵상 에세이'
        
        rt_soup2 = bs4.BeautifulSoup(raw_text, 'html.parser')
        content_area = rt_soup2.find(id='sermon')
        content_html = content_area.decode_contents() if content_area else raw_text
        
        final_html = template_html.replace('{TITLE}', title).replace('{DATE_STR}', date_str).replace('{TYPE_LABEL}', type_label).replace('{BIBLE_REF}', ref).replace('{CONTENT}', content_html)
        
        curr_path = os.path.join(r'D:\code\sparkofbible', fn)
        with open(curr_path, 'w', encoding='utf-8') as f: f.write(final_html)
        orig_path = os.path.join(r'D:\code\300_성경\310_구문묵상\에베소서', fn)
        with open(orig_path, 'w', encoding='utf-8') as f: f.write(final_html)
        print(f"Fixed from transcript: {fn} -> {title} | {ref}")
    else:
        print(f"Could not find raw text for {fn} in transcript")
