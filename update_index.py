import re

index_path = r'D:\code\sparkofbible\index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

ephesians_html = """
        <h2 class="section-title">에베소서 묵상 (1~16편)</h2>
        <div class="list-group" id="ephesians-list">
            <!-- 자바스크립트로 리스트 렌더링 -->
        </div>

        <h2 class="section-title">빌립보서 묵상 (1~9편)</h2>"""

if '<h2 class="section-title">에베소서 묵상 (1~16편)</h2>' not in content:
    content = content.replace('<h2 class="section-title">빌립보서 묵상 (1~9편)</h2>', ephesians_html)

ephesians_js = """
        // 에베소서 에세이 (16개)
        const ephContainer = document.getElementById('ephesians-list');
        const ephFiles = [
            "01_성경적 사고와 인격 만들기_에베소서_1_1-14_세낱말이이백단어를진다_인격만들기_에세이.html",
            "02_성경적 사고와 인격 만들기_에베소서_1_15-23_이미밝혀진눈_인격만들기_에세이.html",
            "03_성경적 사고와 인격 만들기_에베소서_2_1-10_너희로시작해우리로닫는다_인격만들기_에세이.html",
            "04_성경적 사고와 인격 만들기_에베소서_2_11-22_가르던낱말이가름을끝낸다_인격만들기_에세이.html",
            "05_성경적 사고와 인격 만들기_에베소서_3_1-13_마지막수신자는사람이아니었다_인격만들기_에세이.html",
            "06_성경적 사고와 인격 만들기_에베소서_3_14-21_앎이종점이될수없었다_인격만들기_에세이.html",
            "07_성경적 사고와 인격 만들기_에베소서_4_1-6_만들것이아니라지킬것_인격만들기_에세이.html",
            "08_성경적 사고와 인격 만들기_에베소서_4_7-16_주신것이사람이었다_인격만들기_에세이.html",
            "09_성경적 사고와 인격 만들기_에베소서_4_17-24_명령이오지않는여덟절_인격만들기_에세이.html",
            "10_성경적 사고와 인격 만들기_에베소서_4_25-5_2_도착지가적히지않은한자리_인격만들기_에세이.html",
            "11_성경적 사고와 인격 만들기_에베소서_5_3-14_셋째명령이오지않았다_인격만들기_에세이.html",
            "12_성경적 사고와 인격 만들기_에베소서_5_15-21_명령다음에정의가없다_인격만들기_에세이.html",
            "13_성경적 사고와 인격 만들기_에베소서_5_22-33_척도가상대편이아니다_인격만들기_에세이.html",
            "14_성경적 사고와 인격 만들기_에베소서_6_1-9_같은이름에표지가붙는다_인격만들기_에세이.html",
            "15_성경적 사고와 인격 만들기_에베소서_6_10-20_무장은그분의것이다_인격만들기_에세이.html",
            "16_성경적 사고와 인격 만들기_에베소서_6_21-24_본문이잇지않은두방향_인격만들기_에세이.html"
        ];
        
        if (ephContainer) {
            ephFiles.forEach((filename, idx) => {
                const link = document.createElement('a');
                link.href = `./${filename}`;
                link.className = 'list-item';
                
                link.innerHTML = `
                    <div class="item-info">
                        <h3>인격 만들기 (${idx + 1}편)</h3>
                        <p>에베소서 묵상 에세이</p>
                    </div>
                    <div class="arrow">→</div>
                `;
                ephContainer.appendChild(link);
            });
        }

        // 갈라디아서 에세이 (14개)"""

if '에베소서 에세이' not in content:
    content = content.replace('// 갈라디아서 에세이 (14개)', ephesians_js)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully.")
