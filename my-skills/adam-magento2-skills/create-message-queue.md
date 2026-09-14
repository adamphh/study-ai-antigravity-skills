---
name: Create Message Queue
description: Hướng dẫn tạo Message Queue (Async) trong Magento 2
---

# Tạo Message Queue trong Magento 2

Message Queue cho phép xử lý tasks nặng asynchronously.

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   ├── communication.xml
│   ├── queue_consumer.xml
│   ├── queue_publisher.xml
│   └── queue_topology.xml
└── Model/
    ├── Consumer.php
    └── Publisher.php
```

## 1. Định nghĩa Topic

`etc/communication.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Communication/etc/communication.xsd">
    
    <topic name="{vendor}.{modulename}.{action}" 
           request="{Vendor}\{ModuleName}\Api\Data\MessageInterface"/>
           
</config>
```

## 2. Định nghĩa Queue Topology

`etc/queue_topology.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework-message-queue:etc/topology.xsd">
    
    <exchange name="{vendor}.{modulename}.exchange" type="topic" connection="db">
        <binding id="{vendor}.{modulename}.binding" 
                 topic="{vendor}.{modulename}.{action}" 
                 destinationType="queue" 
                 destination="{vendor}.{modulename}.queue"/>
    </exchange>
    
</config>
```

## 3. Đăng ký Consumer

`etc/queue_consumer.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework-message-queue:etc/consumer.xsd">
    
    <consumer name="{vendor}.{modulename}.consumer"
              queue="{vendor}.{modulename}.queue"
              handler="{Vendor}\{ModuleName}\Model\Consumer::process"
              consumerInstance="Magento\Framework\MessageQueue\Consumer"
              connection="db"/>
              
</config>
```

## 4. Đăng ký Publisher

`etc/queue_publisher.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework-message-queue:etc/publisher.xsd">
    
    <publisher topic="{vendor}.{modulename}.{action}">
        <connection name="db" exchange="{vendor}.{modulename}.exchange"/>
    </publisher>
    
</config>
```

## 5. Message Interface

```php
<?php
namespace {Vendor}\{ModuleName}\Api\Data;

interface MessageInterface
{
    public function getEntityId(): int;
    public function setEntityId(int $id): self;
    public function getData(): array;
    public function setData(array $data): self;
}
```

## 6. Publisher Class

```php
<?php
namespace {Vendor}\{ModuleName}\Model;

use Magento\Framework\MessageQueue\PublisherInterface;
use {Vendor}\{ModuleName}\Api\Data\MessageInterfaceFactory;

class Publisher
{
    private PublisherInterface $publisher;
    private MessageInterfaceFactory $messageFactory;
    private const TOPIC = '{vendor}.{modulename}.{action}';

    public function __construct(
        PublisherInterface $publisher,
        MessageInterfaceFactory $messageFactory
    ) {
        $this->publisher = $publisher;
        $this->messageFactory = $messageFactory;
    }

    public function publish(int $entityId, array $data): void
    {
        $message = $this->messageFactory->create();
        $message->setEntityId($entityId);
        $message->setData($data);
        
        $this->publisher->publish(self::TOPIC, $message);
    }
}
```

## 7. Consumer Class

```php
<?php
namespace {Vendor}\{ModuleName}\Model;

use Psr\Log\LoggerInterface;
use {Vendor}\{ModuleName}\Api\Data\MessageInterface;

class Consumer
{
    private LoggerInterface $logger;

    public function __construct(LoggerInterface $logger)
    {
        $this->logger = $logger;
    }

    public function process(MessageInterface $message): void
    {
        try {
            $entityId = $message->getEntityId();
            $data = $message->getData();
            
            // Process your heavy task here
            $this->logger->info("Processing entity: " . $entityId);
            
        } catch (\Exception $e) {
            $this->logger->error("Queue processing error: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Chạy Consumer

```bash
# Chạy consumer
bin/magento queue:consumers:start {vendor}.{modulename}.consumer

# Chạy với giới hạn messages
bin/magento queue:consumers:start {vendor}.{modulename}.consumer --max-messages=100

# Xem danh sách consumers
bin/magento queue:consumers:list
```

## Cấu hình Cron cho Consumer

`etc/crontab.xml`

```xml
<config>
    <group id="default">
        <job name="{vendor}_{modulename}_consumer" 
             instance="Magento\MessageQueue\Model\Cron\ConsumersRunner" 
             method="run">
            <schedule>* * * * *</schedule>
        </job>
    </group>
</config>
```
