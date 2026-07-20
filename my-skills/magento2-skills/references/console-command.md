# Tạo Console Command (CLI)

## Quy trình thực hiện

1. Khai báo Command class trong `etc/di.xml` để đăng ký vào danh sách CLI.
2. Tạo class Command kế thừa `Symfony\Component\Console\Command\Command`.
3. Định nghĩa tên command, input options/arguments trong `configure()`.
4. Thực thi logic trong `execute()`.

## Cấu trúc mẫu

### etc/di.xml
```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    <type name="Magento\Framework\Console\CommandListInterface">
        <arguments>
            <argument name="commands" xsi:type="array">
                <item name="custom_action_command" xsi:type="object">{Vendor}\{Module}\Console\Command\CustomActionCommand</item>
            </argument>
        </arguments>
    </type>
</config>
```

### Console/Command/CustomActionCommand.php
```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Console\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Magento\Framework\App\State;
use Magento\Framework\App\Area;

class CustomActionCommand extends Command
{
    private const OPTION_NAME = 'name';

    public function __construct(
        private readonly State $appState
    ) {
        parent::__construct();
    }

    /**
     * Configure command options and description
     */
    protected function configure(): void
    {
        $this->setName('custom:action:run')
            ->setDescription('Run a custom backend process via CLI')
            ->addOption(
                self::OPTION_NAME,
                'n',
                InputOption::VALUE_OPTIONAL,
                'Optional name option'
            );
        parent::configure();
    }

    /**
     * Execute command
     */
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        try {
            // Tránh lỗi Area code not set khi chạy CLI
            $this->appState->setAreaCode(Area::AREA_ADMINHTML);

            $name = $input->getOption(self::OPTION_NAME) ?: 'World';
            $output->writeln("<info>Running custom action for: {$name}...</info>");

            // logic thực thi ở đây

            $output->writeln("<info>Custom command executed successfully.</info>");
            return Command::SUCCESS;
        } catch (\Exception $e) {
            $output->writeln("<error>Error: {$e->getMessage()}</error>");
            return Command::FAILURE;
        }
    }
}
```

## Checklist trước khi trả lời

- [ ] Phải bọc logic execute trong khối `try/catch` để quản lý mã lỗi đầu ra (`Command::SUCCESS` hoặc `Command::FAILURE`).
- [ ] Luôn gọi `$this->appState->setAreaCode(Area::AREA_ADMINHTML)` để tránh lỗi "Area code is not set" khi code CLI gọi đến các Class core phụ thuộc vào Store/Area.
- [ ] Sử dụng đúng định dạng tag màu của Symfony Console (`<info>`, `<comment>`, `<error>`) để hiển thị thông báo ra Terminal đẹp mắt.
