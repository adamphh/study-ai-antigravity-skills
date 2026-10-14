---
name: Create CLI Command
description: Hướng dẫn tạo CLI Command trong Magento 2
---

# Tạo CLI Command trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── Console/
│   └── Command/
│       └── {CommandName}Command.php
└── etc/
    └── di.xml
```

## 1. Tạo Command Class

`Console/Command/{CommandName}Command.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Console\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Magento\Framework\App\State;
use Magento\Framework\App\Area;

class {CommandName}Command extends Command
{
    private const ARGUMENT_NAME = 'name';
    private const OPTION_DRY_RUN = 'dry-run';

    private State $state;

    public function __construct(State $state, string $name = null)
    {
        $this->state = $state;
        parent::__construct($name);
    }

    protected function configure(): void
    {
        $this->setName('{vendor}:{module}:{action}');
        $this->setDescription('Command description');
        
        $this->addArgument(
            self::ARGUMENT_NAME,
            InputArgument::REQUIRED,
            'Name argument'
        );
        
        $this->addOption(
            self::OPTION_DRY_RUN,
            'd',
            InputOption::VALUE_NONE,
            'Dry run mode'
        );

        parent::configure();
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        try {
            $this->state->setAreaCode(Area::AREA_ADMINHTML);
        } catch (\Exception $e) {
            // Area code already set
        }

        $name = $input->getArgument(self::ARGUMENT_NAME);
        $isDryRun = $input->getOption(self::OPTION_DRY_RUN);

        $output->writeln('<info>Starting process...</info>');
        
        if ($isDryRun) {
            $output->writeln('<comment>Running in dry-run mode</comment>');
        }

        // Your logic here
        $output->writeln(sprintf('Processing: %s', $name));

        $output->writeln('<info>Done!</info>');
        
        return Command::SUCCESS;
    }
}
```

## 2. Đăng ký trong di.xml

`etc/di.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    
    <type name="Magento\Framework\Console\CommandListInterface">
        <arguments>
            <argument name="commands" xsi:type="array">
                <item name="{vendor}_{module}_{action}" xsi:type="object">
                    {Vendor}\{ModuleName}\Console\Command\{CommandName}Command
                </item>
            </argument>
        </arguments>
    </type>
    
</config>
```

## 3. Sử dụng Command

```bash
# Chạy command
bin/magento {vendor}:{module}:{action} "my-argument"

# Với option
bin/magento {vendor}:{module}:{action} "my-argument" --dry-run

# Xem help
bin/magento {vendor}:{module}:{action} --help
```

## Output Formatting

```php
// Colors
$output->writeln('<info>Green text</info>');
$output->writeln('<comment>Yellow text</comment>');
$output->writeln('<error>Red text</error>');
$output->writeln('<question>Black on cyan</question>');

// Progress Bar
$progressBar = new \Symfony\Component\Console\Helper\ProgressBar($output, 100);
$progressBar->start();
for ($i = 0; $i < 100; $i++) {
    $progressBar->advance();
}
$progressBar->finish();

// Table
$table = new \Symfony\Component\Console\Helper\Table($output);
$table->setHeaders(['ID', 'Name']);
$table->setRows([['1', 'Item 1'], ['2', 'Item 2']]);
$table->render();
```
