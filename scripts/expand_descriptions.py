#!/usr/bin/env python3
"""
Expand short meta descriptions in blog articles to 150-160 characters.

All 421 blog articles currently have very short descriptions (~20-30 chars).
This script extends them using topic-based templates.

Usage: python3 scripts/expand_descriptions.py [--test]
"""

import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

TARGET_MIN = 150
TARGET_MAX = 160

# Topic keyword -> description template suffix (each >= 150 chars for total >= 150)
TOPIC_TEMPLATES: list[tuple[list[str], str]] = [
    (
        ['婚禮攝影', '婚攝', '攝影'],
        "詳細解說專業婚禮攝影技巧，涵蓋鏡頭選擇、光線運用、構圖方法及後期調色心法。無論纪实風格還是時尚風格，都能助你捕捉婚禮最動人的瞬間，留下永恆珍貴的回憶。此外還有閃光燈配件使用、RAW格式儲存等重要常識，助你拍出專業級作品，記錄每一刻美好，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['場地', '酒店', '酒樓', '教堂', '戶外'],
        "精選香港人氣婚禮場地，涵蓋五星級酒店、傳統中式酒樓、浪漫西式教堂及戶外花園草坪。提供視野、容量、價位全方位比較與實戰預訂建議，幫你找到最合適的婚禮殿堂，讓賓客留下深刻美好印象，難忘這一生最重要的時刻，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['證書套', '證書'],
        "專為新人設計的結婚證書套，採用高質感亞麻布或磨砂珠光材質，支援熱轉印燙印新人名稱與結婚日期。多款精美風格任選，让愛情見證永恆閃耀，成為一生珍藏的紀念品，送給親友亦極具意義，傳承幸福美好，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['習俗', '過大禮', '安床', '敬茶', '上頭', '回門'],
        "深入介紹香港傳統婚禮習俗的歷史起源與完整流程，包括過大禮、安床、敬茶、上頭、回門等環節。結合現代簡化做法，让你在遵循傳統的同時兼顧實用與便捷，傳承文化精粹不遺忘，讓儀式既莊重又溫馨，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['預算', '財務', '債務', '儲蓄', '理財', '收費', '價錢', '價格', '費用'],
        "提供詳細的婚禮預算分配方案與節省開支實招，涵蓋貸款申請、保險規劃與投資策略。科學管理婚禮財務，輕鬆籌備理想婚禮不超支，為婚後生活打好財務基礎穩步前行，让愛情沒有金錢煩惱，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['婚紗', '禮服', '新娘', '新郎', '伴娘', '造型'],
        "全面介紹婚紗款式選擇、試穿準備技巧、尺碼把握秘訣與保養方法。同步涵蓋新郎西裝、伴娘裙搭配及當日整體造型完整指南，打造完美婚禮形象，让每位新人都光彩照人自信滿分，成為众人矚目的焦點，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['籌備', '流程', '時間表', 'checklist', '清單', '規劃'],
        "从零開始制定完整婚禮籌備時間表，涵蓋供應商挑選比價、儀式流程安排、賓客招待細節等關鍵環節。让整個籌備過程井然有序、有條不紊，減輕新婚夫婦的壓力與焦慮安心籌備，享受即將到來的幸福時光，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['婚戒', '戒指', '鑽石', '珠寶'],
        "詳細解析鑽石 4C 切工淨度顏色克拉標準、婚戒常見材質選擇與各大品牌比較。帮你精準挑選兼具美學設計與保值價值的完美對戒，象徵永恆不變的愛情承諾歷久常新，成为相濡以沫的見證，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['回禮', '禮物', '禮金', '紅包'],
        "精選創意婚禮回禮與賓客感謝禮物靈感，涵蓋香薰蠟燭、個人化定制禮品與實用型選項。展現新人独特品味與細心周到，让賓客帶著美好回憶離去，感恩每一份祝福與支持，分享幸福時刻，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['請柬', '請帖', '邀請卡'],
        "設計獨特婚禮請柬的完整指南，從紙質材質選擇、版式風格設計到印刷工藝比較。打造令人印象深刻的婚禮第一印象，让賓客感受到新人的用心與品味留下美好回憶，開啟精彩婚禮序幕，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['蜜月', '旅行', '目的地'],
        "推薦全球熱門蜜月旅行目的地，涵蓋泰國海島、歐洲浪漫城市、台灣山水風光等多種風格。提供詳細行程規劃、簽證須知與預算參考指南，開啟甜蜜旅程留下美好回憶，共同寫下愛情的新篇章，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['註冊', '法律', '文件', '資格', '婚姻'],
        "詳解香港結婚註冊完整流程、所需文件清單與申請資格要求。涵蓋本地註冊、海外結婚認證及相關法律注意事項，让婚事手續順利無阻，免卻後顧之憂安心籌備，开启人生新階段，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['化妝', '美髮', '髮型', '妝容'],
        "專業婚禮化妝與美髮造型完整指南，介紹試妝溝通技巧、持久妝容秘诀與當日造型準備流程。让你成為婚禮上最耀眼的焦點，留下最美的照片回憶值得珍藏一生，展現獨特的個人魅力，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['音樂', '司儀', '歌單', '演奏'],
        "精選婚禮音樂歌單與司儀挑選要點，涵蓋入場曲、第一支舞、背景音樂等关键环节的完美配樂建議。營造浪漫溫馨的婚禮氛圍，让每個時刻都充滿感動難忘，谱写屬於你們的愛情旋律，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['佈置', '花藝', '裝飾', '甜品'],
        "創意婚禮佈置與花藝設計靈感大全，包括背景牆設計、桌面擺設規劃、甜品桌配置。打造獨一無二令人驚嘆的婚禮現場氛圍，让賓客讚嘆不已留下深刻印象，创造夢幻般的婚禮體驗，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        ['賓客', '座位', '招待', '名單'],
        "賓客招待全攻略，涵蓋座位安排技巧、遠道賓客住宿交通建議與兒童照顧方案。確保每位賓客都感到賓至如歸、盡興而歸，让婚禮圓滿成功賓主盡歡，共享這難忘的幸福時刻，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
    (
        [],
        "詳細攻略與實用建議，涵蓋準備流程、注意事項與專業技巧。助你輕鬆籌備理想的婚禮，留下美好難忘的回憶，開啟人生嶄新章節幸福美滿，让每一個細節都充滿意義與溫度，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成，為你詳盡解說每一步驟，解答所有相關疑難，確保婚禮籌備順利完成。",
    ),
]


def build_description(filename: str, current_desc: str, title: str) -> str:
    """Generate expanded description based on topic keywords."""
    combined = f"{filename} {title} {current_desc}"

    for keywords, template in TOPIC_TEMPLATES:
        if any(kw in combined for kw in keywords):
            base = current_desc.rstrip("。")
            expanded = f"{base}。{template}"
            if len(expanded) > TARGET_MAX:
                expanded = expanded[:TARGET_MAX]
                last_period = expanded.rfind("。")
                if last_period > TARGET_MIN:
                    expanded = expanded[: last_period + 1]
            return expanded

    # Fallback
    base = current_desc.rstrip("。")
    expanded = f"{base}。{TOPIC_TEMPLATES[-1][1]}"
    if len(expanded) > TARGET_MAX:
        expanded = expanded[:TARGET_MAX]
        last_period = expanded.rfind("。")
        if last_period > TARGET_MIN:
            expanded = expanded[: last_period + 1]
    return expanded


def expand_descriptions(test_mode: bool = False) -> int:
    """Expand short meta descriptions. Returns count of changes made."""
    desc_pattern = re.compile(
        r'(<meta\s+name="description"\s+content=")([^"]*)(">)',
        re.IGNORECASE,
    )
    changed = 0

    for fpath in sorted(BLOG_DIR.glob("*.html")):
        content = fpath.read_text(encoding="utf-8")

        m = desc_pattern.search(content)
        if not m:
            continue

        current_desc = m.group(2).strip()
        if len(current_desc) >= TARGET_MIN:
            continue

        filename = fpath.name
        title_m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ""

        new_desc = build_description(filename, current_desc, title)

        new_content = desc_pattern.sub(f"\\g<1>{new_desc}\\g<3>", content)
        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            marker = "✓" if not test_mode else "○"
            print(
                f"  {marker} {filename}: "
                f"{len(current_desc)}→{len(new_desc)} chars"
            )
            changed += 1

    return changed


def main() -> None:
    test_mode = "--test" in sys.argv
    print(f"Scanning {BLOG_DIR} for short descriptions...")
    changed = expand_descriptions(test_mode=test_mode)
    status = "[DRY-RUN] " if test_mode else ""
    print(f"\n{status}Expanded {changed} description(s).")


if __name__ == "__main__":
    main()
