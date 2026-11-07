# 上线三步

这个仓库要建成 **`Smilewithoutfalling/Smilewithoutfalling`** —— 仓库名和用户名完全一致，GitHub 才会把它渲染成你的个人主页。

## 1. 建仓库

网页建：<https://github.com/new>

- Repository name：`Smilewithoutfalling`
- 可见性：**Public**（私有仓库不会渲染主页）
- **不要**勾 "Add a README file"（这里已经有一份，勾了会冲突）

## 2. 推上去

```bash
cd profile-readme
git init -b main
git add .
git commit -m "profile: initial"
git remote add origin https://github.com/Smilewithoutfalling/Smilewithoutfalling.git
git push -u origin main
```

推完直接打开 <https://github.com/Smilewithoutfalling> 就能看到。

## 3. 开 Actions

仓库 → Settings → Actions → General → Workflow permissions → 选 **Read and write permissions** → Save。

然后 Actions → `Update profile contributions` → Run workflow 手动跑一次，确认表格和统计卡能自己刷新。

---

# 文件

| 文件 | 作用 |
|---|---|
| `README.md` | 主页本体。两处 marker 之间的内容由脚本生成，**不要手改**，改了下次也会被覆盖：`PROFILE_BADGES` 里是两个计数徽章的数字，`OPEN_SOURCE_CONTRIBUTIONS` 里是表格 |
| `assets/open-source-stats.svg` | 统计卡，脚本生成。深色，跟随 GitHub 深色主题 |
| `scripts/update_profile.py` | 拉 PR、重写表格、改徽章数字、重画 SVG。只用标准库，没有依赖 |
| `scripts/snapshot.example.json` | 一份真实的搜索响应快照，用来离线预览 |
| `.github/workflows/update-profile.yml` | 每天 03:17 UTC 跑一次，有变化就 commit |

---

# 数据口径

**只统计「外部 PR」**，查询是 `is:pr author:Smilewithoutfalling -user:Smilewithoutfalling`。`-user:` 排除你自己的仓库，所以 `datachat` 里那 100 多个 PR 不计入 —— 自己给自己提的 PR 不构成"贡献"，混进去数字就失去了意义。

**只显示 merged 和 open。** closed 但没有 merge 的不计入，那是一次没通过的尝试，不是贡献。

**私有仓库里的 PR 看不到。** GitHub 的搜索只索引你能搜到的内容，所以脚本给出的这个数字是**下限**，不是全量。这一点不打算藏：如果哪天数字看着偏低，原因大概率在这里。

**每天自动跑。** 定时任务、`workflow_dispatch` 手动触发都可以。脚本只在内容真的变了的时候 commit，不会每天凭空多一个空提交。transient 的 5xx / 429 会退避重试三次，避免一次网关抖动把主页冻结 24 小时。

---

# 本地预览

```bash
# 从已保存的搜索响应生成（不打 API，不消耗限速）
python3 scripts/update_profile.py --from-json=scripts/snapshot.example.json

# 只打印，不写文件
python3 scripts/update_profile.py --dry-run

# 检查是否过期（CI 用；过期返回 1）
python3 scripts/update_profile.py --check

# 正常模式：直接打 GitHub API
GITHUB_TOKEN=ghp_xxx python3 scripts/update_profile.py
```

不带 token 时 search API 限速 **10 次/分钟**，脚本只翻一页（100 条），够用。带了 token 是 30 次/分钟。

---

# 要你自己改的 5 处

1. **名字** —— `README.md` 第一行的 `Hey, I'm Jianhong 👋`。`Jianhong` 是我按你 Windows 用户名拼的，不对就改掉。

2. **typing 动画的 4 行文案** —— 在 README 里那个 `readme-typing-svg.demolab.com` 的 URL 上。格式很挑：行之间用 `;`，空格用 `+`，`/` 写成 `%2F`，`&` 写成 `%26`。改完在浏览器打开那个 URL 就能预览。

3. **三处文案** —— `What I Build`、`Research`、`Focus Areas`。现在写的是我从你的项目里读出来的（病理多模态、评测闸门、Agent 运行时、NL2SQL），有不准确的直接改。

4. **`scripts/update_profile.py` 的 `USERNAME`** —— 默认已经是 `Smilewithoutfalling`，换账号才需要动。

5. **`DESCRIPTIONS`** —— 这张表把 PR 标题翻成一句人话（`fix(cli)!: exit 1 when teamai remove removes nothing` → "Made `remove` fail loudly instead of silently succeeding when nothing matched"）。没在表里的 PR 自动回退到原始标题，所以新贡献不会漏，只是措辞生硬。重要的新 PR 回来补一行就行。

---

# 顺手建议

主页做好之后，右侧信息栏现在还是空的，观感上会拖后腿：

- **bio**：`Computational pathology · multimodal survival analysis · LLM application engineering`
- **Location**：广州
- **仓库描述**：`datachat` 现在没有 description、没有 topics，别人点进去不知道是什么。补一句 + 加 `nl2sql` `llm` `data-analysis` 这类 topic，被搜到的概率就变了。

---

# 已知限制

- 统计卡最多画 **6 个仓库**，多的折叠成 `+N more repositories` —— 超过 6 个时图表就变成一排标签，读者也读不过来。
- 主表只留 **最近 10 条** merged，其余收进 `<details>` 折叠。33 条平铺是一份日志，不是一份履历。
- 徽章上的数字**不自动更新** —— 那四个 badge 指向的是 GitHub 搜索链接，不写死数字，因为写死就一定会过期，而过期的数字比没有数字更糟。
