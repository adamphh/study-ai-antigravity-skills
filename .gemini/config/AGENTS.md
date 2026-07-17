# Workspace Coding Rules & Guidelines

## Core Principles
1. **Never Edit Core Files Directly**: Always use the extensibility mechanisms of the POS framework (Plugins, Rewrites, Mixins, Event Observers) to customize core functionalities. For files in `client/pos/src`, changes are ONLY allowed within the `src/extension/` directory.
2. **Always Create a Plan First**: Always create a plan file (e.g. `Plans/{ma_du_an}-{ma_issue}_plan_v1.0.md` and `implementation_plan.md` artifact) for the user to review. Do not start implementing code until the user explicitly reviews and approves the plan. trong đó {ma_du_an} và {ma_issue} lấy từ git branch.
3. **Communication Guidelines**:
   - Always explain briefly and concisely in Vietnamese.
   - Comment code in English. Always add comments in rewritten, plugin, or customize files explaining what was changed or customized compared to the original core classes/files to make it easy to review.
   - Always ask the user for clarification if any requirements or issues are not fully understood.
4. **Creating a New Module in Extension**:
   - Create a directory: `src/extension/<module_name>/`.
   - Create a configuration file: `src/extension/<module_name>/etc/config.js` extending `ModuleConfigAbstract`.
   - Enable & Register: Run `npm run upgrade` in the `client/pos` directory. This script automatically enables the module in `modules.json`, updates `src/extension/config.js` imports, and merges any custom dependencies from the extension's local `package.json`.

## Customization Patterns for webpos client

### Rewrite Mechanism
- For overriding class methods or properties, create rewrite files under `src/extension/<extension_name>/rewrite/`.
- Register rewrites in `src/extension/<extension_name>/etc/config.js` under the `rewrite` block.
- Use wrapper functions for rewrites:
  ```javascript
  export default function (BaseClass) {
      return class Rewrite extends BaseClass {
          // Overridden methods or properties
      };
  }
  ```

### Plugins (Before, Around, After)
- Register plugins in the `plugin` block of `etc/config.js` to modify arguments, wrap execution, or alter return values of specific methods.

### Mixins
- Inject new methods or static functions into core classes via `mixin` registration in `etc/config.js`.

### Event Observers
- Subscribe to custom events using `listen` from `event-bus` or dispatch new ones with `fire`.

### Layout Customization Mechanism
- Inject or customize UI elements in screens/pages by declaring them in the `layout` block of `etc/config.js`.
- Layout configurations correspond to the layout hooks defined in core components via `layout('[block]')('[hook]')()(this)`.
- Layout plugins can be plain text, React components, or functions that receive the parent component instance as an argument.

## Git Commit Guidelines
1. **Commit Message Format**:
   - Use the format: `{Fix/Feat} [{mã dự án} - {issue id}]: {ticket ID hoặc user story name}`
     - `{Fix/Feat}`: Use `Fix` for bugs, `Feat` for user stories / features.
     - `{mã dự án}`: Project code (e.g. `P1115` at the start of branch).
     - `{issue id}`: Issue ID (e.g. `391` after project code in branch).
     - Example: `Feat [P1115 - 391]: [US09] Customize Tyro payment popup layout and cancellation flow`.
2. **Review Changes Before Committing**:
   - Always run `git status` and `git diff` to review code modifications.
   - Do not stage or commit temporary build outputs, configs, or dependencies.
3. **Commit Scope**:
   - Only commit files within the defined implementation plan.

