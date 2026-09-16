# PRESENTATIONS — 婚禮視頻展示項目

**Each of the 40 presentations is an independent Vite + React project.**

## OVERVIEW
40 個獨立婚禮視頻展示項目，部署於 GitHub Pages。每個項目含 6 章結構（冷開→內容→CTA），繁體中文口播稿，支援手動/自動播放模式。

## STRUCTURE
```
presentations/
├── index.html                 # 40 個視頻索引頁
├── _scaffold.sh               # 新項目生成器（8 種主題配色）
├── build-scripts/
│   ├── build-all.sh           # 平行建構全部 40 個專案
│   └── patch-base.sh          # 批次修補 vite.base path
├── 01-hong-kong-wedding-flow/
│   ├── article.md             # 內容源文件
│   ├── outline.md             # 章節大綱
│   ├── script.md              # 口播稿
│   └── presentation/          # 獨立 Vite+React 專案
│       ├── src/
│       │   ├── App.tsx        # 主入口
│       │   ├── main.tsx
│       │   ├── chapters/      # 6 章節目（01-coldopen ~ 06-cta）
│       │   │   └── 01-coldopen/
│       │   │       ├── Coldopen.tsx
│       │   │       ├── Coldopen.css
│       │   │       └── narrations.ts  # 旁白文本數組
│       │   ├── components/    # Stage / ProgressBar / AutoToggle / AutoStartGate
│       │   ├── hooks/
│       │   │   ├── useStepper.ts
│       │   │   ├── useAudioPlayer.ts
│       │   │   └── useAutoMode.ts
│       │   ├── registry/
│       │   │   ├── chapters.ts  # 章節註冊表
│       │   │   └── types.ts     # ChapterDef / Narration / ChapterStepProps
│       │   └── styles/
│       │       ├── fonts.css
│       │       ├── tokens.css   # 主題色變量（scaffold 生成）
│       │       ├── base.css
│       │       └── animations.css
│       ├── public/audio/      # TTS 音訊（按需生成）
│       ├── vite.config.ts
│       ├── tsconfig.json      # project references
│       ├── tsconfig.app.json
│       ├── tsconfig.node.json
│       ├── eslint.config.js
│       └── package.json
└── [39 more projects...]
```

## STRUCTURE
| 任務 | 位置 |
|------|------|
| 新增簡報 | `presentations/_scaffold.sh` |
| 章節內容 | `presentations/XX-slug/article.md` + `outline.md` + `script.md` |
| 旁白文本 | `src/chapters/<NN>-<id>/narrations.ts` |
| 投影片組件 | `src/chapters/<NN>-<id>/<Id>.tsx` |
| 章節註冊 | `src/registry/chapters.ts` |
| TTS 音訊生成 | `npm run extract-narrations && npm run synthesize-audio` |
| 平行建構全部 | `bash presentations/build-scripts/build-all.sh` |
| 批量修補 base | `bash presentations/build-scripts/patch-base.sh` |

## CONVENTIONS
- **檔名格式**：`NN-slug-name/presentation/`（2 位數字前綴）
- **章節命名**：`01-coldopen`、`02-xxx`、...、`06-cta`
- **narrations.ts**：純字串數組，空字串 = 靜默步驟（auto mode 用 estimate fallback）
- **Audio 路徑**：`public/audio/<chapter-id>/<step+1>.mp3`（1-indexed）
- **主题色**：通过 scaffold 生成的 `tokens.css`（:root CSS 變量），8 種配色可选
- **TypeScript 嚴格模式**：noUnusedLocals、verbatimModuleSyntax、erasableSyntaxOnly

## ANTI-PATTERNS
- 勿硬編碼 `BASE_URL` — 用 `import.meta.env.BASE_URL`
- 勿在 `narrations.ts` 使用 `{text, minHoldMs}` 格式（已移除）
- 勿提交 `dist/` / `node_modules/`
- 勿直接編輯 `tokens.css` — 由 scaffold 根據主題生成
- 本地 dev 用 `npx vite --base ""`（vite.config.ts base 為 GitHub Pages 路徑）

## COMMANDS
```bash
# 新增簡報
bash presentations/_scaffold.sh 41 "new-topic-slug" "新主題標題" default

# 單個簡報
cd presentations/41-new-topic/presentation
npm run dev                          # 本地開發（--base "" 已内嵌）
npm run build                        # 生產建構（含 tsc -b）
npx tsc --noEmit                     # 類型檢查
npm run lint                         # ESLint

# 音訊生成
npm run extract-narrations           # 輸出 audio-segments.json
bash scripts/synthesize-audio.sh     # TTS 合成 mp3（provider-agnostic）

# 批量
bash presentations/build-scripts/build-all.sh [--skip-existing]
bash presentations/build-scripts/patch-base.sh
```

## NOTES
- 內容管線：`scripts/expand_presentation_content.py` 可從部落格文章自動生成 narrations.ts
- 音訊提供者：內建 MiniMax mmx-cli + OpenAI TTS，可換 ElevenLabs / edge-tts / Azure
- 40 個簡報目前無 shared node_modules（各專案獨立 install）
- `public/` 目錄含音訊和靜態資源，`assets/` 存 build 後產物

## SELF-UPDATE

每次新增簡報或修改共享 component（Stage / useStepper / useAudioPlayer），更新此檔 STRUCTURE 與 COMMANDS 後 commit：

```bash
git add AGENTS.md
git commit -m "docs: update presentations/AGENTS.md — {change}"
```

如发现新的 build 陷阱或 TypeScript 坑位，寫入 `../../docs/lessons/presentation-{topic}.md`。
