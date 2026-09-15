import json
import re
import os

transcript_path = r'C:\Users\user\.gemini\antigravity-cli\brain\dd9ca71c-c9ac-49e6-8c7d-ec4f193b615b\.system_generated\logs\transcript_full.jsonl'
template_path = r'D:\code\.agents\skills\thought-essay-html\templates\essay_template.html'

with open(template_path, 'r', encoding='utf-8') as f:
    template_html = f.read()

files = [
    '01_성경적 사고와 인격 만들기_에베소서_1_1-14_세낱말이이백단어를진다_인격만들기_에세이.html',
    '02_성경적 사고와 인격 만들기_에베소서_1_15-23_이미밝혀진눈_인격만들기_에세이.html',
    '03_성경적 사고와 인격 만들기_에베소서_2_1-10_너희로시작해우리로닫는다_인격만들기_에세이.html',
    '04_성경적 사고와 인격 만들기_에베소서_2_11-22_가르던낱말이가름을끝낸다_인격만들기_에세이.html',
    '05_성경적 사고와 인격 만들기_에베소서_3_1-13_마지막수신자는사람이아니었다_인격만들기_에세이.html',
    '06_성경적 사고와 인격 만들기_에베소서_3_14-21_앎이종점이될수없었다_인격만들기_에세이.html',
    '07_성경적 사고와 인격 만들기_에베소서_4_1-6_만들것이아니라지킬것_인격만들기_에세이.html',
    '08_성경적 사고와 인격 만들기_에베소서_4_7-16_주신것이사람이었다_인격만들기_에세이.html',
    '09_성경적 사고와 인격 만들기_에베소서_4_17-24_명령이오지않는여덟절_인격만들기_에세이.html',
    '10_성경적 사고와 인격 만들기_에베소서_4_25-5_2_도착지가적히지않은한자리_인격만들기_에세이.html',
    '11_성경적 사고와 인격 만들기_에베소서_5_3-14_셋째명령이오지않았다_인격만들기_에세이.html',
    '12_성경적 사고와 인격 만들기_에베소서_5_15-21_명령다음에정의가없다_인격만들기_에세이.html',
    '13_성경적 사고와 인격 만들기_에베소서_5_22-33_척도가상대편이아니다_인격만들기_에세이.html',
    '14_성경적 사고와 인격 만들기_에베소서_6_1-9_같은이름에표지가붙는다_인격만들기_에세이.html',
    '15_성경적 사고와 인격 만들기_에베소서_6_10-20_무장은그분의것이다_인격만들기_에세이.html',
    '16_성경적 사고와 인격 만들기_에베소서_6_21-24_본문이잇지않은두방향_인격만들기_에세이.html'
]

# extract raw texts
raw_texts = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'SYSTEM_MESSAGE':
            content = data.get('content', '')
            match = re.search(r'```html\n(.*?)```', content, re.DOTALL)
            if match:
                raw_texts.append(match.group(1).strip())
        
        if 'tool_calls' in data:
            for call in data['tool_calls']:
                if call['function']['name'] == 'default_api:write_to_file':
                    args = call['function'].get('arguments', '')
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except:
                            continue
                    if 'CodeContent' in args:
                        cc = args['CodeContent']
                        if '<article id="sermon">' in cc:
                            raw_texts.append(cc)

# Deduplicate
unique_texts = []
for t in raw_texts:
    if t not in unique_texts:
        unique_texts.append(t)

print(f'Found {len(unique_texts)} unique raw texts')

# match texts with files by reading the target file or matching title
for fn in files:
    m = re.search(r'^(\d+)_.*?_([가-힣]+)_(\d+)_(\d+)-(\d+)(?:_(\d+))?', fn)
    if not m: continue
    idx = m.group(1)
    book = m.group(2)
    c = m.group(3)
    v1 = m.group(4)
    c2_v2 = m.group(5)
    v2 = m.group(6)
    
    if v2:
        ref = f'{book} {c}:{v1}~{c2_v2}:{v2}'
    else:
        ref = f'{book} {c}:{v1}-{c2_v2}'
        
    date_str = f'에베소서 제 {idx}편'
    type_label = '성경적 사고와 인격 만들기'
    
    # Read the CURRENT html to see some snippet to match
    curr_path = os.path.join(r'D:\code\sparkofbible', fn)
    if not os.path.exists(curr_path):
        continue
        
    with open(curr_path, 'r', encoding='utf-8') as f:
        curr_html = f.read()
    
    # Find the matching raw_text
    # We can match by finding a sentence inside curr_html that is also in raw_text
    import bs4
    soup = bs4.BeautifulSoup(curr_html, 'html.parser')
    sermon = soup.find(id='sermon')
    if not sermon: continue
    sermon_text = sermon.get_text(strip=True)
    if len(sermon_text) < 50: continue
    snippet = sermon_text[10:30]
    
    matched_raw = None
    for rt in unique_texts:
        rt_soup = bs4.BeautifulSoup(rt, 'html.parser')
        rt_text = rt_soup.get_text(strip=True)
        if snippet.replace(" ", "") in rt_text.replace(" ", ""):
            matched_raw = rt
            break
            
    if matched_raw:
        # Extract title from matched_raw
        title_match = re.search(r'#\s*(.+)', matched_raw)
        title = title_match.group(1).strip() if title_match else "묵상 에세이"
        
        # Extract content
        rt_soup2 = bs4.BeautifulSoup(matched_raw, 'html.parser')
        content_area = rt_soup2.find(id='sermon')
        content_html = content_area.decode_contents() if content_area else ""
        
        # Re-apply template
        final_html = template_html.replace("{TITLE}", title) \
                                  .replace("{DATE_STR}", date_str) \
                                  .replace("{TYPE_LABEL}", type_label) \
                                  .replace("{BIBLE_REF}", ref) \
                                  .replace("{CONTENT}", content_html)
                                  
        with open(curr_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Fixed: {fn} -> {title} | {ref}")
        
        # Also copy to origin
        orig_path = os.path.join(r'D:\code\300_성경\310_구문묵상\에베소서', fn)
        with open(orig_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
    else:
        print(f"Could not find raw text for {fn}")
