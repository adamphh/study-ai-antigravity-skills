# React-Toastify Auto-Dismiss Fix Pattern (`ToastObserver`)

## 1. Vấn đề (Problem Statement)
Trong ứng dụng WebPOS sử dụng thư viện `react-toastify` (ví dụ v3.4.3):
- Cơ chế tự động đóng (`autoClose`) mặc định dựa hoàn toàn vào CSS animation `trackProgress` trong `ProgressBar` và sự kiện `onAnimationEnd`.
- Khi người dùng hoàn tất đặt hàng hoặc thanh toán, POS thường mở hộp thoại in (Native Print Dialog hoặc Iframe `window.print()`), hoặc chuyển tab khiến trình duyệt rơi vào trạng thái blur / modal.
- Trạng thái này làm đóng băng (freeze/suspend) luồng render animation của trình duyệt, khiến sự kiện `animationend` không được kích hoạt.
- Hậu quả: Toast message (đặc biệt là message xanh sau khi đặt hàng thành công) bị treo vĩnh viễn trên UI cho đến khi click thủ công, và khi đặt nhiều order liên tiếp các toast sẽ bị chồng đè lên nhau.

---

## 2. Giải Pháp Chuẩn (Standard Solution)
Tạo `ToastObserver` trong module `fix-bug` (`src/extension/fix-bug/observer/ToastObserver.js`) để can thiệp trực tiếp vào `EventManager` của `react-toastify`:
1. Lắng nghe `ACTION.SHOW`:
   - Khi có toast xuất hiện với `autoClose !== false`, khởi tạo một timer Javascript fallback (`setTimeout` với thời gian `delay + 300ms`) gọi `toast.dismiss(toastId)`.
2. Lắng nghe `ACTION.CLEAR`:
   - Xóa bỏ các active timer khi toast bị đóng hoặc dọn dẹp để tránh memory leak.

---

## 3. Mã Nguồn Mẫu (Reference Implementation)

```javascript
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */

/**
 * ToastObserver
 *
 * Fallback auto-dismiss timer for react-toastify to prevent stuck toasts
 * when browser print dialog or background throttling blocks CSS animationend event.
 */
class ToastObserver {
    activeTimers = {};

    /**
     * Constructor
     */
    constructor() {
        this.init();
    }

    /**
     * Initialize event listeners for toast actions
     */
    init() {
        try {
            const EventManager = require("react-toastify/lib/util/EventManager").default;
            const {ACTION} = require("react-toastify/lib/constant");
            const {toast} = require("react-toastify");

            if (!EventManager || !ACTION || !toast) {
                return;
            }

            // Listen for SHOW_TOAST action to set up JS fallback timer
            EventManager.on(ACTION.SHOW, (content, options) => {
                if (!options || typeof options.toastId === 'undefined') {
                    return;
                }

                const toastId = options.toastId;

                // Clear any existing timer for this toastId
                if (this.activeTimers[toastId]) {
                    clearTimeout(this.activeTimers[toastId]);
                    delete this.activeTimers[toastId];
                }

                // If autoClose is not disabled (autoClose !== false)
                if (options.autoClose !== false) {
                    const defaultDelay = 2000;
                    const delay = (typeof options.autoClose === 'number' && options.autoClose > 0)
                        ? options.autoClose
                        : defaultDelay;

                    // Fallback timeout with 300ms buffer after CSS animation
                    this.activeTimers[toastId] = setTimeout(() => {
                        try {
                            toast.dismiss(toastId);
                        } catch (e) {
                            // ignore dismiss error
                        }
                        delete this.activeTimers[toastId];
                    }, delay + 300);
                }
            });

            // Listen for CLEAR_TOAST action to clean up tracked timers
            EventManager.on(ACTION.CLEAR, (id) => {
                if (id !== null && typeof id !== 'undefined') {
                    if (this.activeTimers[id]) {
                        clearTimeout(this.activeTimers[id]);
                        delete this.activeTimers[id];
                    }
                } else {
                    Object.keys(this.activeTimers).forEach((key) => {
                        clearTimeout(this.activeTimers[key]);
                        delete this.activeTimers[key];
                    });
                }
            });
        } catch (error) {
            // Handle any unexpected initialization errors gracefully
        }
    }
}

export default ToastObserver;
```

---

## 4. Đăng Ký Trong `etc/config.js`

```javascript
import ModuleConfigAbstract from "../../ModuleConfigAbstract";
import ToastObserver from "../observer/ToastObserver";

class Config extends ModuleConfigAbstract {
    module = ['fix-bug'];
    observer = (() => {
        new ToastObserver();
    })();
}

export default (new Config());
```
