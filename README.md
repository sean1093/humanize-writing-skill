# humanize-writing-skill

這是一個 Claude skill，用來寫出或改寫成「讀起來像真人寫的」英文。它會拿掉常見的 AI 痕跡（AI tells），例如 delve、tapestry、"It's not X, it's Y"、凡事列三點、大量破折號、結尾總結、句子長度太平均，並加入具體細節、立場和自然的節奏。

適合用在：**履歷、報告、英文口說練習**，也適用 email、求職信、LinkedIn、部落格。
支援兩種模式：**從零寫**，以及**改寫你給的文字**。

---

## 目錄

1. [安裝](#1-安裝)
2. [確認有裝成功](#2-確認有裝成功)
3. [怎麼用：範例指令](#3-怎麼用範例指令)
4. [你會得到什麼](#4-你會得到什麼)
5. [讓效果更好的訣竅](#5-讓效果更好的訣竅)
   - [還是被檢測出來？](#還是被檢測出來)
   - [設定你的語氣檔（voice profile）](#設定你的語氣檔voice-profile)
6. [單獨使用檢查腳本](#6-單獨使用檢查腳本)
7. [檔案結構](#7-檔案結構)
8. [限制與注意事項](#8-限制與注意事項)

---

## 1. 安裝

### Claude Code：所有專案都能用（推薦）

```bash
git clone https://github.com/sean1093/humanize-writing-skill
mkdir -p ~/.claude/skills
cp -r humanize-writing-skill/humanize-writing ~/.claude/skills/
```

裝好的路徑是 `~/.claude/skills/humanize-writing/SKILL.md`。

### Claude Code：只給某個專案用

```bash
mkdir -p <你的專案>/.claude/skills
cp -r humanize-writing-skill/humanize-writing <你的專案>/.claude/skills/
```

這個資料夾 commit 進專案之後，團隊其他人也能用。

### Claude.ai（網頁版 / App）

**最簡單：直接下載打包好的檔案**

1. 下載 [`dist/humanize-writing.zip`](dist/humanize-writing.zip)（在 GitHub 上點進檔案，再按右上角的 Download）。
2. 到 Claude.ai 的 **Settings → Capabilities → Skills**，按 **Upload skill**，選這個 zip。
3. 確認 skill 已啟用（開關打開）。

**自己打包的話**，要注意兩點，不然上傳會出錯：
- zip 裡最外層必須是 `humanize-writing/` **資料夾**，`SKILL.md` 放在資料夾裡面，不能直接放在 zip 根目錄。
- 不要用 GitHub 的「Download ZIP」整包上傳，因為那樣最外層會是 `humanize-writing-skill-master/`，多了一層。

```bash
cd humanize-writing-skill
zip -r humanize-writing.zip humanize-writing -x "humanize-writing/evals/*"
```

> Claude.ai 需要開啟「Code execution」相關功能，才能執行檢查腳本。沒有開也能用，只是少了自動檢查這一步。

### 更新到最新版

```bash
cd humanize-writing-skill && git pull
cp -r humanize-writing ~/.claude/skills/
```

---

## 2. 確認有裝成功

**重新開一個** Claude Code session（skill 在啟動時載入），然後問：

```
What skills do you have available?
```

清單裡看到 `humanize-writing` 就代表成功了。也可以直接輸入 `/humanize-writing` 呼叫它。

---

## 3. 怎麼用：範例指令

平常怎麼講話就怎麼下指令就好，不用特別寫 skill 名稱。只要內容提到「去 AI 味」、「像人寫的」、「履歷」、「面試自我介紹」、「報告」這類需求，Claude 會自動套用這個 skill。中文、英文提問都可以，**產出一律是英文**，說明會用你提問的語言。

想確保一定會用到這個 skill，可以在開頭加上 `/humanize-writing`。

### 履歷

**改寫**
```
/humanize-writing 幫我改這幾條履歷，recruiter 說看起來像 AI 寫的：
- Spearheaded cross-functional initiatives to streamline onboarding, resulting in a 40% increase in efficiency.
- Leveraged data-driven insights to optimize marketing campaigns.
```

**從零寫**
```
幫我寫履歷的工作經歷，英文，不要有 AI 味。
我在 ABC 公司當後端工程師 4 年，用 Go 和 PostgreSQL，
做過付款系統重構（每天處理約 50 萬筆交易），帶過 2 個新人。
```

### 報告

**改寫**
```
Rewrite the intro of my quarterly report so it doesn't sound like ChatGPT:
"In today's rapidly evolving business landscape, customer retention plays a pivotal role..."
Q3 churn was 6.1%, up from 4.8% in Q2.
```

**從零寫**
```
幫我寫一份英文的專案結案報告摘要（約 300 字），給主管看。
重點：專案延遲 2 週、原因是第三方 API 變更、最後上線後錯誤率從 3% 降到 0.5%。
```

### 英文口說練習

**面試自我介紹**
```
幫我寫一段一分鐘的英文自我介紹，面試用。
我是後端工程師，做了 4 年，主要寫 Go 跟 PostgreSQL，想換到 fintech。
要聽起來自然，不要像背稿。我的英文程度大概中上。
```

**面試題目回答**
```
面試會被問 "Tell me about a time you disagreed with your manager."
我的經驗是：主管想直接上線新功能，我覺得測試不夠，最後我們折衷先上 10% 流量。
幫我寫成口說的回答，大概 1.5 分鐘。
```

**IELTS 雅思口說**

Skill 內建一份 Part 2 範例模板（`references/ielts-speaking.md`），預設會照這個風格寫：用字淺白，每篇只放 3 到 6 個主題字詞，一個具體故事加上你自己的經驗，長度 180 到 250 字（約 1.5 到 2 分鐘）。

結構：
1. 開場：介紹對象（1 句）
2. 怎麼認識的：一開始…後來…（2 到 3 句）
3. 主要理由：點出一個具體概念，再用簡單的話解釋（2 到 3 句）
4. 一個具體故事：I remember that…（3 到 4 句）
5. 跟自己的連結：你自己的經驗（3 到 4 句）
6. 收尾：So, for me… That's why…（2 句）

**給你自己的經驗，效果最好**，回答會更自然，你也更容易記住、講得流利：
```
雅思口說 part 2：Describe a skill you learned that you are proud of.
我的經驗：大學一年級學游泳，本來很怕水，練了一個學期，現在可以游 1000 公尺。
```

沒給經驗也可以，skill 會用 `[ ]` 標出建議的故事，你再換成自己的：
```
幫我寫雅思口說 part 2：Describe a place you visited that you would like to go back to.
```

Part 1（30 到 60 字）和 Part 3（70 到 120 字）也適用，題目貼上去就好。想要不同程度，就加一句「程度 band 7」。

想換成自己的範例模板，直接改 `references/ielts-speaking.md` 第 1 節的範例答案。

**改寫你自己寫的稿子**
```
這是我準備的英文簡報開場，念起來很像在背作文，幫我改成自然的口語：
"Good morning everyone. Today I would like to delve into the key findings of our research..."
```

### 其他（email、LinkedIn、求職信）

```
幫我把這封 email 改得自然一點，像真人寫的：[貼上內容]
```

---

## 4. 你會得到什麼

每次的回覆通常包含：

1. **成品**：可以直接複製貼上，或拿來念的英文。
2. **改動說明**（3 到 6 點）：改了什麼、為什麼這樣改。
3. **`[placeholder]`**：需要你自己補的真實細節，例如：
   ```
   Built the new-hire checklist in Notion; laptop setup went from [X] days to [Y].
   ```
   **這是刻意的設計。** Skill 不會替你編造經歷、數字、人名或引用來源，請把括號換成真實資訊。這些具體細節也正是讓文字像人寫的關鍵。
4. **（只有口說練習）** 3 到 6 個可以重複使用的片語，有時也會標出容易念錯的字。

---

## 5. 讓效果更好的訣竅

- **給真實細節。** 數字、專案名稱、具體事件，給越多，成品越不像 AI，也不會留一堆 placeholder。
- **說清楚用途和讀者。** 例如「給主管看的週報」或「外商面試的自我介紹」，語氣會差很多。
- **口說練習要講程度和時間。** 例如「程度中等、1 分鐘」。稿子超出你的程度，念起來反而像背稿。
- **改完自己念一遍。** 覺得哪句不像你會說的話，直接跟 Claude 說「第二段太正式了」或「這句我不會這樣講」。

### 還是被檢測出來？

AI 檢測器主要看兩件事：**用字好不好猜**（每個字都是最可能的下一個字），以及**節奏是不是太平均**。只拿掉 delve 這類字詞不夠，文字如果還是很順、很平衡、很籠統，照樣會被抓出來。效果由高到低：

1. **自己先寫，再讓 Claude 輕改。** 這是最有效的方法。英文寫得不好也沒關係，或者用條列筆記，甚至中英混雜都可以。Skill 會用「輕度編輯」模式，保留你的用字和語序，只修文法和最明顯的 AI 痕跡。
   ```
   /humanize-writing 這是我自己寫的報告草稿，幫我輕度修改就好，不要改太多，保留我的用字：
   [貼上你的草稿]
   ```
2. **給寫作樣本**（見下一節）。Skill 會量出你的句長、用字長度、縮寫頻率等習慣，讓成品往你的風格靠攏。
3. **填完 placeholder 後，自己再改幾句。** 你親手改過的字，就是最「人」的訊號。
4. **不要改完又丟回 ChatGPT 或 Grammarly 潤飾。** 過度潤飾是真人文章被誤判成 AI 的常見原因。

**不要用**市面上「AI humanizer」常見的技巧，例如插入隱形字元、替換成長得像的 Unicode 字母、故意打錯字、同義詞替換器。Turnitin 等工具會專門抓這些，還可能讓履歷在 ATS 系統解析失敗。這個 skill 刻意不做這些事。

> 沒有任何工具能保證 100% 通過檢測，檢測器本身也常把真人寫的文章誤判成 AI。

### 設定你的語氣檔（voice profile）

1. 打開 `humanize-writing/references/voice-profile.md`。
2. 貼上 2 到 3 段你**自己寫、沒用 AI**的英文（email、報告、訊息都可以），總共 300 字以上最好。
3. 可以順便寫幾句你的習慣，例如「我句子很短」、「英文是第二語言，不要用太難的字」。
4. Claude Code 存檔後就會生效。Claude.ai 要重新打包上傳（見[安裝](#claudeai網頁版--app)）。

不想存檔的話，也可以每次直接在對話裡貼樣本：
```
照我的語氣寫，這是我平常寫的 email：
[貼上樣本]
```

## 6. 單獨使用檢查腳本

不透過 Claude，也可以直接拿腳本檢查任何英文文字（只需要 Python 3，不用安裝任何套件）：

```bash
# 檢查檔案
python3 humanize-writing/scripts/check_tells.py draft.txt

# 從剪貼簿或 pipe 輸入
cat draft.txt | python3 humanize-writing/scripts/check_tells.py -

# 輸出 JSON
python3 humanize-writing/scripts/check_tells.py draft.txt --json

# 跟你自己寫的樣本比較風格差距
python3 humanize-writing/scripts/check_tells.py draft.txt --compare my_sample.txt
```

輸出範例：
```
RHYTHM & STYLE
  sentence length mean 11.9, stdev 7.2, CV 0.61
  short (<=8 words) 50.0%, long (>=30) 0.0%
  paragraph length CV 0.25
  ...

FLAGGED WORDS
  'landscape' x1  (lines 1)
  'navigate' x1  (lines 3)
  'fosters' x1  (lines 3)
  ...

FLAGGED PHRASES
  "in today's fast-paced digital landscape" x1  (lines 1)
  "it's important to note" x1  (lines 1)
  'plays a crucial role' x1  (lines 1)
  ...

STRUCTURAL PATTERNS (triplet_list is noisy; check by eye)
  'negation_reframe' x2  (lines 1, 3)
  'trailing_participle' x1  (lines 3)
  'triplet_list' x1  (lines 3)

BLAND / PREDICTABLE WORDING (10.6 per 1000 words)
  'approach' x1  (lines 1)

REWRITE THESE SENTENCES FIRST
  [9] In today's fast-paced digital landscape, remote work has become more than just a trend — it's a fundamental shift in how we approach our professional lives.
  [8] It empowers employees to navigate the complexities of modern life, highlighting the importance of work-life balance.
  [6] It's important to note that this transition plays a crucial role in shaping company culture.
  ...

TOTAL TELLS (excluding triplets and bland): 18  (191.5 per 1000 words)
```

怎麼看結果：
- **FLAGGED WORDS / PHRASES**：AI 常用的字詞和套語，後面附行號。
- **STRUCTURAL PATTERNS**：AI 常用的句型，例如 "not just X, but Y"，或句尾加上 ", highlighting..." 這種評論。
- **sentence length CV**：句子長短的變化程度。低於 0.4 代表句子長度太平均，讀起來像機器寫的。
- **em dashes**：每 300 字超過 1 個就偏多。
- **BLAND / PREDICTABLE WORDING**：「安全但好猜」的字，例如 various、ensure、in terms of。單獨出現沒關係，每千字超過約 15 個就偏多。
- **REWRITE THESE SENTENCES FIRST**：AI 痕跡最多的幾句，優先改這些。
- **opener share**：句子開頭重複的程度。太多句用 The、This、It 開頭會很單調。
- **TOTAL TELLS**：總數越低越好。但出現一兩個不代表有問題，人也會用這些字。
- **VOICE MATCH**（加上 `--compare` 時才會出現）：草稿和你的樣本在各項風格上的差距。標 `too high` 或 `too low` 的項目，就是要往你的習慣調整的地方。

> 這個腳本只是「煙霧警報器」，不是 AI 檢測器。分數低不保證能通過任何檢測工具。

---

## 7. 檔案結構

```
humanize-writing/
├── SKILL.md                  # 主流程：選模式 → 起草 → 檢查 → 改寫 → 再檢查
├── references/
│   ├── ai-tells.md           # AI 慣用字詞、句型、結構清單與替代寫法
│   ├── techniques.md         # 10 組改寫前後對照
│   ├── genres.md             # 履歷、報告、口說、email 等各文體的寫法
│   ├── ielts-speaking.md     # 雅思口說範例答案、Part 1/2/3 模板
│   └── voice-profile.md      # 你的寫作樣本（自己填）
├── scripts/
│   └── check_tells.py        # 檢查腳本
└── evals/
    └── evals.json            # 測試題目（開發用，不會打包進 zip）

dist/
├── humanize-writing.zip      # 給 Claude.ai 上傳用
└── humanize-writing.skill    # 同內容，.skill 格式
```

想自訂的話，最常改的是這兩個地方：
- 要加禁用字詞：改 `references/ai-tells.md`，以及 `scripts/check_tells.py` 裡的 `WORDS` / `PHRASES`。
- 要調整某種文體的寫法：改 `references/genres.md`。

---

## 8. 限制與注意事項

- **不保證通過任何 AI 檢測器。** GPTZero、Turnitin 這類工具一直在更新，誤判率也高。這個 skill 的目標是讓人讀起來自然，不是去鑽某個檢測器的漏洞。
- **不會捏造內容。** 需要你的真實經驗、數字或引用來源時，它會留 placeholder，而不是自己編。
- **只針對英文。** 中文的去 AI 味規則不一樣，目前不支援。
- **請遵守使用場合的規定。** 如果學校作業或考試禁止使用 AI，用這個 skill 也一樣不符合規定。
