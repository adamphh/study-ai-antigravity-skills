---
marp: true
theme: uncover
class: invert
paginate: true
header: 'Antigravity CLI Agent Workflow'
footer: 'Magestore WebPOS & Magento 2 Team'
style: |
  section {
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 24px;
    padding: 40px;
    background-color: #0f172a;
    color: #e2e8f0;
    text-align: left;
  }
  h1 {
    font-size: 42px;
    color: #38bdf8;
    margin-bottom: 20px;
  }
  h2 {
    font-size: 32px;
    color: #f59e0b;
    border-bottom: 2px solid #334155;
    padding-bottom: 10px;
  }
  h3 {
    font-size: 26px;
    color: #a78bfa;
  }
  table {
    font-size: 19px;
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }
  th {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 10px;
  }
  td {
    padding: 8px 10px;
    border-bottom: 1px solid #334155;
  }
  code {
    background-color: #1e293b;
    color: #fbbf24;
    font-size: 0.9em;
    padding: 2px 6px;
    border-radius: 4px;
  }
  pre {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 8px;
    font-size: 18px;
  }
  .highlight-box {
    background: #1e293b;
    border-left: 4px solid #38bdf8;
    padding: 15px;
    border-radius: 4px;
    margin-top: 15px;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 15px;
  }
  .card-red {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #ef4444;
    border-radius: 8px;
    padding: 15px;
    font-size: 18px;
  }
  .card-green {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid #22c55e;
    border-radius: 8px;
    padding: 15px;
    font-size: 18px;
  }
  .card-blue {
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid #38bdf8;
    border-radius: 8px;
    padding: 15px;
    font-size: 18px;
  }
---

<!-- Slide 1: Cover -->
# 🚀 Cách Dùng Antigravity CLI Làm Việc Hàng Ngày Cho Dev

![bg right:45% fit](/home/bss/.gemini/antigravity-cli/brain/f7f4bfc3-a2b6-4038-a0ea-6e19188df797/ai_developer_pair_programming_1787278371532.jpg)

- **Người chia sẻ:** Adam 96
- **Team:** Rong

---

<!-- Slide 2: Problems -->
## ⚠️ Những Vấn Đề Hay Gặp Khi Để AI Tự Làm

<div class="grid-3">
  <div class="card-red">
    <h3>1. Sửa Nhầm Vào Core</h3>
    <ul>
      <li>Sửa thẳng vào <code>src/pos/</code> hoặc <code>vendor/</code></li>
      <li>Update core là bị ghi đè mất</li>
      <li>Đáng lẽ viết plugin thì lại sửa file gốc</li>
    </ul>
  </div>
  <div class="card-red">
    <h3>2. Chậm & Tốn Token</h3>
    <ul>
      <li>Grep tìm kiếm khắp ổ cứng</li>
      <li>Đọc cả file mấy nghìn dòng chỉ lấy 1 hàm</li>
      <li>Mới chat vài câu đã hết bộ nhớ context</li>
    </ul>
  </div>
  <div class="card-red">
    <h3>3. Code Không Chạy Thử</h3>
    <ul>
      <li>Đặt tên biến, tên hàm lung tung</li>
      <li>Không chạy test kiểm tra thực tế</li>
      <li>Để lại file test rác trong project</li>
    </ul>
  </div>
</div>

---

<!-- Slide 3: Root Cause -->
## ❓ Vì Sao AI Hay Làm Sai Và Chạy Chậm?

```
[Chỉ đưa yêu cầu ngắn]
       │
       ▼
[AI phải tự đi dò tìm file khắp ổ cứng]
       │
       ▼
[Đọc nhầm file lớn & Tràn bộ nhớ Context]
       │
       ▼
[Chọn cách nhanh nhất: Sửa thẳng vào file Core tìm thấy]
```

<div class="highlight-box">
  <b>3 Thiếu Sót Cốt Lõi:</b><br/>
  1. Chưa dặn chỗ nào được sửa, chỗ nào cấm chạm vào.<br/>
  2. Không có sẵn bảng mục lục code để tra cứu nhanh.<br/>
  3. Thiếu quy trình bắt buộc phải lên Plan và chạy test trước khi commit.
</div>

---

<!-- Slide 4: 4 Pillars -->
## 🏛️ 4 Phần Cấu Thành Một AI Agent

![bg right:40% fit](/home/bss/.gemini/antigravity-cli/brain/f7f4bfc3-a2b6-4038-a0ea-6e19188df797/ai_guardrails_concept_1787278384754.jpg)

<div style="font-size: 20px;">

1. **📋 Mục tiêu & Vai trò:** Dặn AI biết mình là ai, làm việc gì.
2. **🚧 Ranh giới (Guardrails):** Chỉ rõ chỗ được sửa, chỗ cấm chạm vào.
3. **🔧 Công cụ (Tools):** Đọc/ghi file, chạy Docker/NPM, đọc Jira.
4. **📖 Mục lục (Indexer):** Tra nhanh vị trí code trong 1 giây.

👉 **Tất cả xoay quanh Context Window:** Giữ bộ nhớ AI sạch sẽ để ra quyết định chính xác!
</div>

---

<!-- Slide 5: Solution Overview -->
## 🛠️ Tổng Quan Cách Tổ Chức Hệ Thống

<div class="grid-3">
  <div class="card-blue">
    <h3>1. Ranh Giới (Rules)</h3>
    <ul>
      <li>Lưu vị trí các dự án</li>
      <li>Cấm sửa vào Core 100%</li>
      <li>Chuẩn format dòng code <= 120 ký tự</li>
    </ul>
  </div>
  <div class="card-blue">
    <h3>2. Bộ Mục Lục (Index)</h3>
    <ul>
      <li>Tầng 1: Core dùng chung</li>
      <li>Tầng 2: Riêng từng dự án</li>
      <li>Tra cứu nhanh trong 1 giây</li>
    </ul>
  </div>
  <div class="card-blue">
    <h3>3. Quy Trình (Workflow)</h3>
    <ul>
      <li>11 bước từ Jira đến Git</li>
      <li>Tự chạy test Docker/NPM</li>
      <li>Subagent review độc lập</li>
    </ul>
  </div>
</div>

---

<!-- Slide 6: Step 1 - In-Memory -->
## ⚡ Cách 1: Tìm Đúng Thư Mục Dự Án Ngay Lập Tức

<div class="grid-2">
  <div class="card-red">
    <h3>❌ Cách Cũ: Dùng Shell Scan</h3>
    <p><code>find /home/bss -name "*P1115*"</code></p>
    <ul>
      <li>Quét hàng trăm GB ổ đĩa</li>
      <li>Chờ lâu, dễ timeout</li>
      <li>Tốn rất nhiều token vô ích</li>
    </ul>
  </div>
  <div class="card-green">
    <h3>✅ Cách Mới: Tra Bảng Bộ Nhớ</h3>
    <p><code>project-mapping.md</code></p>
    <ul>
      <li><code>P1115</code> ➔ <code>/mnt/projects/p1115-...</code></li>
      <li>Nhảy vào thư mục trong <b>0.1 giây</b></li>
      <li><b>0 lệnh shell</b>, tuyệt đối không quét bừa bãi</li>
    </ul>
  </div>
</div>

---

<!-- Slide 7: Step 2 - 2-Tier Index -->
## 📖 Cách 2: Bộ Mục Lục Code 2 Tầng (Tiết Kiệm 80% Token)

```
                            [ Router Hub: `indexes/README.md` ]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
       [ TẦNG 1: DÙNG CHUNG ]                        [ TẦNG 2: TỪNG DỰ ÁN ]
       (study-ai-antigravity-skills)                 (docs/data-flows/)
       • WebPOS Services (80+ classes)               • Client Plugins (`extension-plugins`)
       • Payment, Reward, Barcode...                 • Client Rewrites, Mixins
       • Lập 1 lần, dùng cho mọi dự án               • Server Custom & FixBug riêng
```

<div class="highlight-box">
  💡 Thay vì đọc cả file 3.000 dòng để tìm 1 hàm ➔ Xem mục lục là biết ngay hàm ở dòng số <code>#L56</code>.
</div>

---

<!-- Slide 8: Step 3 - Scope Guardrails -->
## 🚧 Cách 3: Đặt Ranh Giới Rõ Ràng — Cấm Sửa Vào Core

### 1. Thư mục được phép sửa:
- **Backend:** `app/code/Magestore/*Custom*` hoặc `*FixBug*`
- **Frontend:** `client/pos/src/extension/*custom*` hoặc `*fix-bug*`
- **Tuyệt đối cấm:** Sửa trực tiếp trong `src/pos/` hoặc `vendor/`

### 2. Quy định khi viết code:
```php
// ✅ Luôn dùng ::class trong PHP
$this->cartRepo = $objectManager->get(CartRepositoryInterface::class);
```
```javascript
// ✅ WebPOS: Nạp service bên trong hàm để tránh lỗi undefined
const QuoteService = require("service/checkout/QuoteService").default;
```

---

<!-- Slide 9: 10 Steps Overview -->
## 🔄 Quy Trình 10 Bước Thực Chiến Khi Nhận Task

<div style="font-size: 19px; line-height: 1.6;">

```
[0. Vào dự án (project-mapping)] ──➔ [1. Tạo Git Branch từ release] ──➔ [2. Đọc Jira & Chuyển In Progress]
                                                                                   │
┌──────────────────────────────────────────────────────────────────────────────────┘
│
▼
[3. Check Môi trường & Index code] ──➔ [4. Đọc Data Flow & Check trùng] ──➔ [5. Lập Plan & Duyệt]
                                                                                   │
┌──────────────────────────────────────────────────────────────────────────────────┘
│
▼
[6. Viết Code (npm upgrade)] ──➔ [7. Chạy test & Dọn file rác] ──➔ [8. Soi Git diff & Walkthrough]
                                                                                   │
┌──────────────────────────────────────────────────────────────────────────────────┘
│
▼
[9. Nhờ Subagent review độc lập] ──➔ [10. Tạo Commit chuẩn & Gợi ý học hỏi (/learn)]
```

</div>

---

<!-- Slide 10: Steps 0-1 -->
## 🚀 Bước 0 & 1: Định Vị Dự Án & Chuẩn Bị Git Branch

<div class="grid-2">
  <div class="card-blue">
    <h3>Bước 0: Vào Thư Mục Dự Án</h3>
    <ul>
      <li>Check phiên chat cũ để mở lại (nếu có).</li>
      <li>Tra bảng <code>project-mapping.md</code> để đặt thư mục làm việc (0 lệnh shell).</li>
    </ul>
  </div>
  <div class="card-green">
    <h3>Bước 1: Chuẩn Bị Git Branch Sạch</h3>
    <ul>
      <li>Kiểm tra branch hiện tại.</li>
      <li>Đảm bảo pull code mới nhất từ nhánh <code>release</code>.</li>
      <li>Tạo branch riêng: <code>feature/{dự_án}-{issue}</code> (tránh dính code task cũ).</li>
    </ul>
  </div>
</div>

---

<!-- Slide 11: Steps 2-4 -->
## 🔍 Bước 2, 3 & 4: Đọc Jira An Toàn & Tra Cứu Mục Lục

### 🎯 1. Đọc Jira & Tự Đổi Trạng Thái An Toàn (Bước 2)
- **Nếu task đang ở `To Do`:** AI tự động chuyển sang **`In Progress`** (`jira_transition_issue`).
- **Nếu task đang ở trạng thái khác (`In Progress`, `Done`...):** **CẤM** tuyệt đối không thay đổi trạng thái.
- Đọc tóm tắt yêu cầu, mô tả lỗi và Acceptance Criteria.

### 📖 2. Kiểm Tra Môi Trường & Tra Cứu Không Cần Grep (Bước 3 & 4)
- **Auto-Init & Auto-Index:** Tự tạo 4 file mục lục nếu dự án mới.
- **Check trùng lặp:** Tra cứu bảng ma trận `extension-plugins.md` để biết tính năng đã có extension nào can thiệp trước đó chưa mà **không cần chạy 1 lệnh grep nào!**

---

<!-- Slide 12: Step 7 -->
## 📋 Bước 3: Lập Kế Hoạch (Plan) Trước Khi Code

<div class="grid-2">
  <div class="card-blue">
    <h3>File Plan Tiêu Chuẩn Gồm:</h3>
    <ol>
      <li><b>Yêu cầu:</b> Cần làm những gì?</li>
      <li><b>Nguyên nhân:</b> Vì sao bị lỗi?</li>
      <li><b>Giải pháp:</b> Sửa file nào, hàm nào?</li>
      <li><b>Kiểm thử:</b> Test kịch bản nào?</li>
    </ol>
  </div>
  <div class="card-green">
    <h3>Chủ Động Hỏi Lại:</h3>
    <p>Nếu yêu cầu chưa rõ ràng ➔ AI tự động hỏi 2–3 câu trắc nghiệm để làm rõ logic.</p>
    <div class="highlight-box">
      <b>Quy tắc vàng:</b> Chỉ khi bạn bấm <b>Approve</b> kế hoạch thì AI mới bắt đầu viết code!
    </div>
  </div>
</div>

---

<!-- Slide 13: Step 8-9 -->
## 🧪 Bước 4: Viết Code & Chạy Thử Test Tự Động

```
[1. Viết code chuẩn theo Plan]
               │
               ▼
[2. Chạy test tự động: PHP qua Docker / JS qua NPM]
               │
               ▼
[3. Ghi kết quả pass/fail vào walkthrough.md]
               │
               ▼
[4. Tự xóa các file test tạm (Giữ Git luôn sạch sẽ)]
```

- **Máy không cài PHP?** AI tự biết gọi lệnh qua container Docker (`docker exec phpunit...`).
- **Không lo rác Git:** Tệp test tạm thời được xóa sạch trước khi commit.

---

<!-- Slide 14: Step 10-11 -->
## 🕵️ Bước 5: Subagent Review & Chuẩn Hóa Git

<div class="grid-2">
  <div class="card-blue">
    <h3>1. Subagent Code Reviewer</h3>
    <p>Gọi một phụ tá độc lập soi lại toàn bộ diff:</p>
    <ul>
      <li>🔍 <b>Memory Leak:</b> Quên unbind event</li>
      <li>🔍 <b>Race Condition:</b> Bất đồng bộ khi sync</li>
      <li>🔍 <b>Null Pointer:</b> Thiếu kiểm tra <code>?.</code></li>
    </ul>
  </div>
  <div class="card-green">
    <h3>2. Chuẩn Hóa Git Commit</h3>
    <p>Tạo commit message đúng mẫu của team:</p>
    <code>Feat [P1115 - 391]: [US09] Customize Tyro popup</code>
    <br/><br/>
    <p>💡 Gợi ý chạy <code>/learn</code> nếu task có kinh nghiệm hay để lưu vào bộ nhớ chung.</p>
  </div>
</div>

---

<!-- Slide 15: Results -->
## 📊 Kết Quả Thực Tế Trước Và Sau Khi Áp Dụng

| Tiêu chí so sánh | Cách làm cũ | Khi áp dụng hệ thống này |
| :--- | :--- | :--- |
| **Token tiêu thụ mỗi task** | ~45.000 – 60.000 tokens | **~8.000 – 12.000 tokens** *(Giảm ~80%)* |
| **Thời gian tìm file code** | Mất 3 – 5 phút chờ grep | **5 – 10 giây** *(Tra qua mục lục)* |
| **Sửa nhầm vào file Core** | Thỉnh thoảng vẫn bị | **0 lần** *(Chặn cứng bằng Rule)* |
| **Lỗi vi phạm chuẩn code** | Hay quên (dài dòng, thiếu doc) | **0 lỗi** *(AI tự kiểm tra trước)* |
| **Mức độ chủ động của AI** | Phải ngồi gõ nhắc từng câu | **1 câu lệnh giải quyết trọn vẹn** |

---

<!-- Slide 16: Setup & QA -->
## 🛠️ 3 Bước Bắt Đầu Ngay Trên Máy Bạn

1. **Bước 1:** Lấy thư mục cấu hình `.agent` và `.gemini/config` về máy.
2. **Bước 2:** Mở file `project-mapping.md` điền đường dẫn các dự án của bạn vào.
3. **Bước 3:** Gõ lệnh: `Bắt đầu task PXXXX-YYY` ➔ Bắt đầu làm việc!

---

# 💬 HỎI ĐÁP & THẢO LUẬN
### Cảm ơn anh em đã lắng nghe! 

*Ai có câu hỏi hay muốn demo thử trên một task thực tế không?*
