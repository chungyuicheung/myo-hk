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

# Topic keyword -> description template suffix (each ~80-100 chars for total ~150-160)
TOPIC_TEMPLATES: list[tuple[list[str], str]] = [
    (
        ['婚禮攝影', '婚攝', '攝影'],
        "詳細解說婚禮攝影技巧，涵蓋鏡頭選擇、光線運用、構圖方法及後期調色，助你拍出專業級作品，記錄每一刻美好。",
    ),
    (
        ['場地', '酒店', '酒樓', '教堂', '戶外'],
        "精選香港人氣婚禮場地，涵蓋五星級酒店、傳統酒樓、教堂及戶外草坪，提供全方位比較與預訂建議，幫你找到最合適的婚禮殿堂。",
    ),
    (
        ['證書套', '證書'],
        "專為新人設計的結婚證書套，採用高質感亞麻布或磨砂珠光材質，支援熱轉印燙印，讓愛情見證永恆閃耀。",
    ),
    (
        ['習俗', '過大禮', '安床', '敬茶', '上頭', '回門'],
        "深入介紹香港傳統婚禮習俗，涵蓋過大禮、安床、敬茶、上頭、回門等環節，結合現代簡化做法讓儀式既莊重又溫馨。",
    ),
    (
        ['預算', '財務', '債務', '儲蓄', '理財', '收費', '價錢', '價格', '費用'],
        "提供詳細的婚禮預算分配方案與省錢實招，涵蓋貸款申請、保險規劃與投資策略，科學管理婚禮財務輕鬆不超支。",
    ),
    (
        ['婚紗', '禮服', '新娘', '新郎', '伴娘', '造型'],
        "全面介紹婚紗款式選擇、試穿準備技巧、尺碼把握與保養方法，同步涵蓋新郎西裝與伴娘裙搭配，打造完美婚禮形象。",
    ),
    (
        ['籌備', '流程', '時間表', 'checklist', '清單', '規劃'],
        "从零開始制定完整婚禮籌備時間表，涵蓋供應商挑選比價、儀式流程安排與賓客招待細節，让整個過程井然有序。",
    ),
    (
        ['婚戒', '戒指', '鑽石', '珠寶'],
        "詳細解析鑽石4C標準、婚戒材質選擇與品牌比較，帮你精準挑選兼具美學與保值價值的完美對戒。",
    ),
    (
        ['回禮', '禮物', '禮金', '紅包'],
        "精選創意婚禮回禮靈感，涵蓋香薰蠟燭、個人化定制禮品與實用選項，展現新人獨特品味與細心周到。",
    ),
    (
        ['請柬', '請帖', '邀請卡'],
        "設計獨特婚禮請柬指南，從紙質材質選擇、版式風格到印刷工藝比較，打造令人印象深刻的婚禮第一印象。",
    ),
    (
        ['蜜月', '旅行', '目的地'],
        "推薦全球熱門蜜月目的地，涵蓋海島、歐洲城市、台灣風光等多種風格，提供行程規劃與簽證須知指南。",
    ),
    (
        ['註冊', '法律', '文件', '資格', '婚姻'],
        "詳解香港結婚註冊流程、所需文件清單與申請資格，涵蓋本地註冊與海外認證，让婚事手續順利無阻。",
    ),
    (
        ['化妝', '美髮', '髮型', '妝容'],
        "專業婚禮化妝與美髮造型指南，介紹試妝溝通技巧、持久妝容秘诀與當日造型準備流程，让你成為最耀眼的焦點。",
    ),
    (
        ['音樂', '司儀', '歌單', '演奏'],
        "精選婚禮音樂歌單與司儀挑選要點，涵蓋入場曲、第一支舞與背景音樂配樂建議，營造浪漫溫馨的婚禮氛圍。",
    ),
    (
        ['佈置', '花藝', '裝飾', '甜品'],
        "創意婚禮佈置與花藝設計靈感，包括背景牆設計、桌面擺設規劃與甜品桌配置，打造獨一無二的婚禮現場。",
    ),
    (
        ['賓客', '座位', '招待', '名單'],
        "賓客招待全攻略，涵蓋座位安排技巧、遠道賓客住宿交通建議與兒童照顧方案，確保每位賓客都感到賓至如歸。",
    ),
    (
        [],
        "詳細攻略與實用建議，涵蓋準備流程、注意事項與專業技巧。助你輕鬆籌備理想的婚禮，留下美好難忘的回憶。",
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
                last_period = expanded.rfind("。", TARGET_MIN - 1, TARGET_MAX)
                if last_period > 0:
                    expanded = expanded[: last_period + 1]
                else:
                    expanded = expanded[:TARGET_MAX]
            return expanded

    # Fallback
    base = current_desc.rstrip("。")
    expanded = f"{base}。{TOPIC_TEMPLATES[-1][1]}"
    if len(expanded) > TARGET_MAX:
        last_period = expanded.rfind("。", TARGET_MIN - 1, TARGET_MAX)
        if last_period > 0:
            expanded = expanded[: last_period + 1]
        else:
            expanded = expanded[:TARGET_MAX]
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
