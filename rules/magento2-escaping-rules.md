# Magento 2 PHTML Escaping & PHPDoc Standards

1. **Required PHPDoc Annotations**:
   Every `.phtml` file must contain explicit `@var` annotations for `$block` and `$escaper` at the top of the file to prevent IDE red underline warnings:
   ```php
   /**
    * @var \Magestore\ModuleName\Block\BlockClass $block
    * @var \Magento\Framework\Escaper $escaper
    */
   ```

2. **Standard Escaping Methods**:
   - Plain HTML text content: `$block->escapeHtml($text)` or `$escaper->escapeHtml($text)`
   - HTML Attributes (`id`, `class`, `alt`, `title`, `value`, `data-*`): `$block->escapeHtmlAttr($attr)` or `$escaper->escapeHtmlAttr($attr)`
   - URLs (`href`, `src`, `action`): `$block->escapeUrl($url)` or `$escaper->escapeUrl($url)`
   - Inline JS variables inside string quotes: `$block->escapeJs($str)` or `$escaper->escapeJs($str)`

3. **Forbidden Escaping Patterns**:
   - NEVER wrap `$block->getChildHtml()`, `$block->getBlockHtml()`, `$block->getPagerHtml()`, or `$block->getFormattedAddress()` in `escapeHtml()`. Use `<?= /* @noEscape */ $block->getChildHtml(...) ?>`.
   - NEVER wrap `$secureRenderer->renderTag()` or `$secureRenderer->renderEventListenerAsTag()` in `escapeHtml()`.
   - NEVER wrap raw JSON in `escapeHtml()`. Inside `<script>` tags, use `<?= /* @noEscape */ json_encode(...) ?>` or `escapeJs()`. For HTML data attributes (e.g., Alpine.js `x-data`), use `$block->escapeHtmlAttr(json_encode($data))` to prevent attribute breaking or XSS.
