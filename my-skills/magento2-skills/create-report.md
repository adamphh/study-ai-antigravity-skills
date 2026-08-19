---
name: Create Magento 2 Report
description: Hướng dẫn tạo báo cáo chuẩn Magento 2 với kiến trúc Aggregation Engine, Filter Form và Export CSV/Excel
---

# Hướng dẫn Tạo Báo Cáo Chuẩn Magento 2 (Magento 2 Reporting Guide)

Tài liệu này hướng dẫn cách xây dựng hệ thống báo cáo (Report) chuẩn mực theo đúng kiến trúc của Magento Core
(tương tự Sales Orders Report, Tax Report, Bestsellers Report), giải quyết triệt để bài toán hiệu năng và tràn RAM
khi xử lý dữ liệu lớn.

---

## 1. Tổng quan Kiến trúc Báo cáo Magento (2-Phase Architecture)

Khi báo cáo cần tổng hợp dữ liệu từ hàng triệu bản ghi (đơn hàng, hóa đơn, sản phẩm), việc truy vấn trực tiếp
(`GROUP BY`, `SUM`, `COUNT`, `JOIN`) trên các bảng giao dịch thô (`sales_order`, `sales_order_item`) lúc tải trang
sẽ gây khóa bảng, timeout và nghẽn hệ thống bán hàng.

Magento Core giải quyết vấn đề này bằng kiến trúc **2 Pha tách biệt**:

1. **Pha 1: Background Aggregation Engine (Tính toán ngầm & Snapshot)**:
   - Cron Job hoặc Quản trị viên kích hoạt tính toán tổng hợp dữ liệu theo định kỳ (hàng ngày/giờ).
   - Dữ liệu được tính sẵn (Pre-calculated metrics) và lưu vào bảng tổng hợp (`*_aggregated_*`).
2. **Pha 2: Report Presentation (Truy vấn & Hiển thị)**:
   - Báo cáo chỉ việc đọc dữ liệu từ bảng Aggregated đã tính sẵn (truy vấn cực nhanh < 10ms).
   - Hệ thống tự động bù đắp các ngày không phát sinh số liệu (Empty Rows / Zero-Filling) để biểu đồ liền mạch.

---

## 2. Cấu trúc Thư mục Module Báo cáo

```
{Vendor}/{ModuleName}/
├── etc/
│   ├── crontab.xml                                      # Lịch trình chạy tổng hợp ngầm
│   ├── reports.xml                                      # Đăng ký vào Reports > Statistics
│   ├── db_schema.xml                                    # Khai báo bảng Aggregated
│   └── di.xml                                           # Khai báo DI và Virtual Type
├── Block/
│   └── Adminhtml/
│       └── Report/
│           └── {ReportName}/
│               ├── Container.php                        # Container bọc Filter Form & Grid
│               └── Grid.php                             # Bảng hiển thị kế thừa AbstractGrid
├── Controller/
│   └── Adminhtml/
│       └── Report/
│           └── {ReportName}/
│               ├── Index.php                            # Action hiển thị trang báo cáo
│               ├── ExportCsv.php                        # Action xuất file CSV
│               └── ExportExcel.php                      # Action xuất file Excel (XML)
├── Model/
│   ├── Cron/
│   │   └── Aggregate{ReportName}.php                    # Cron task thực thi tổng hợp
│   └── ResourceModel/
│       └── Report/
│           ├── {ReportName}.php                         # Aggregator kế thừa AbstractReport
│           └── {ReportName}/
│               └── Collection.php                       # Collection kế thừa AbstractCollection
└── view/adminhtml/
    └── layout/
        └── {route}_report_{reportname}_index.xml        # Layout XML trang báo cáo
```

---

## 3. Bước 1: Khai báo Bảng Aggregated (`etc/db_schema.xml`)

Bảng tổng hợp lưu trữ 2 nhóm thông tin:
- **Dimensions (Chiều phân tích):** `period` (DATE), `store_id` (INT), `order_status` (VARCHAR).
- **Metrics (Chỉ số đo lường):** `orders_count`, `total_qty`, `total_revenue`, `total_tax`, `total_discount`...

```xml
<?xml version="1.0"?>
<!--
  ~ Copyright © Magestore. All rights reserved.
  ~ See COPYING.txt for license details.
  -->
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Setup/Declaration/Schema/etc/schema.xsd">
    <table name="{vendor}_{module}_sales_aggregated" resource="sales" engine="innodb" comment="Aggregated Sales Report">
        <column xsi:type="int" name="id" unsigned="true" nullable="false" identity="true" comment="Primary ID"/>
        <column xsi:type="date" name="period" nullable="false" comment="Period (Day/Month/Year)"/>
        <column xsi:type="smallint" name="store_id" unsigned="true" nullable="false" default="0" comment="Store ID"/>
        <column xsi:type="varchar" name="order_status" nullable="false" length="32" default="" comment="Order Status"/>
        <column xsi:type="int" name="orders_count" unsigned="true" nullable="false" default="0" comment="Orders Count"/>
        <column xsi:type="decimal" name="total_qty" scale="4" precision="12" nullable="false"
                default="0" comment="Total Qty"/>
        <column xsi:type="decimal" name="total_revenue" scale="4" precision="12" nullable="false"
                default="0" comment="Total Revenue"/>
        <column xsi:type="decimal" name="total_tax" scale="4" precision="12" nullable="false"
                default="0" comment="Total Tax"/>
        <column xsi:type="decimal" name="total_discount" scale="4" precision="12" nullable="false"
                default="0" comment="Total Discount"/>

        <constraint xsi:type="primary" referenceId="PRIMARY">
            <column name="id"/>
        </constraint>
        <constraint xsi:type="unique" referenceId="UNQ_{VENDOR}_{MODULE}_PERIOD_STORE_STATUS">
            <column name="period"/>
            <column name="store_id"/>
            <column name="order_status"/>
        </constraint>
        <index referenceId="IDX_{VENDOR}_{MODULE}_PERIOD" indexType="btree">
            <column name="period"/>
        </index>
        <index referenceId="IDX_{VENDOR}_{MODULE}_STORE_ID" indexType="btree">
            <column name="store_id"/>
        </index>
    </table>
</schema>
```

---

## 4. Bước 2: Xây dựng Resource Model Aggregator (`Model/ResourceModel/Report/{ReportName}.php`)

Class này chịu trách nhiệm tính toán dữ liệu từ các bảng giao dịch gốc và ghi vào bảng tổng hợp bằng cú pháp
`INSERT INTO ... ON DUPLICATE KEY UPDATE`.

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\ResourceModel\Report;

use Magento\Framework\Model\ResourceModel\Db\Context;
use Magento\Framework\Stdlib\DateTime\DateTime;
use Magento\Framework\Stdlib\DateTime\TimezoneInterface;
use Magento\Reports\Model\ResourceModel\Report\AbstractReport;
use Psr\Log\LoggerInterface;

class {ReportName} extends AbstractReport
{
    private DateTime $dateTime;

    /**
     * Constructor.
     *
     * @param Context $context
     * @param LoggerInterface $logger
     * @param TimezoneInterface $localeDate
     * @param DateTime $dateTime
     * @param string|null $connectionName
     */
    public function __construct(
        Context $context,
        LoggerInterface $logger,
        TimezoneInterface $localeDate,
        DateTime $dateTime,
        ?string $connectionName = null
    ) {
        $this->dateTime = $dateTime;
        parent::__construct($context, $logger, $localeDate, $connectionName);
    }

    /**
     * Define main table.
     *
     * @return void
     */
    protected function _construct(): void
    {
        $this->_init("{vendor}_{module}_sales_aggregated", "id");
    }

    /**
     * Aggregate report data for specific date range.
     *
     * @param string|null $from
     * @param string|null $to
     * @return $this
     */
    public function aggregate(?string $from = null, ?string $to = null): self
    {
        $connection = $this->getConnection();
        $sourceTable = $this->getTable("sales_order");
        $targetTable = $this->getMainTable();

        $periodExpr = $connection->getDatePartSql(
            $this->_getPeriodDateExpression($connection, "created_at")
        );

        $select = $connection->select()
            ->from(
                ["o" => $sourceTable],
                [
                    "period" => $periodExpr,
                    "store_id" => "o.store_id",
                    "order_status" => "o.status",
                    "orders_count" => new \Zend_Db_Expr("COUNT(o.entity_id)"),
                    "total_qty" => new \Zend_Db_Expr("COALESCE(SUM(o.total_qty_ordered), 0)"),
                    "total_revenue" => new \Zend_Db_Expr("COALESCE(SUM(o.base_grand_total), 0)"),
                    "total_tax" => new \Zend_Db_Expr("COALESCE(SUM(o.base_tax_amount), 0)"),
                    "total_discount" => new \Zend_Db_Expr("COALESCE(SUM(ABS(o.base_discount_amount)), 0)"),
                ]
            )
            ->where("o.state <> ?", \Magento\Sales\Model\Order::STATE_CANCELED)
            ->group([$periodExpr, "o.store_id", "o.status"]);

        if ($from !== null) {
            $select->where("o.created_at >= ?", $from);
        }
        if ($to !== null) {
            $select->where("o.created_at <= ?", $to);
        }

        $insertQuery = $connection->insertFromSelect(
            $select,
            $targetTable,
            [
                "period", "store_id", "order_status",
                "orders_count", "total_qty", "total_revenue", "total_tax", "total_discount"
            ],
            \Magento\Framework\DB\Adapter\AdapterInterface::INSERT_ON_DUPLICATE
        );

        $connection->query($insertQuery);
        return $this;
    }

    /**
     * Convert timestamp to localized date expression.
     *
     * @param \Magento\Framework\DB\Adapter\AdapterInterface $connection
     * @param string $field
     * @return \Zend_Db_Expr
     */
    protected function _getPeriodDateExpression($connection, string $field): \Zend_Db_Expr
    {
        return new \Zend_Db_Expr(sprintf("DATE(%s)", $field));
    }
}
```

---

## 5. Bước 3: Đăng ký Cron Job & Refresh Statistics

### 5.1. Khai báo Cron Job (`etc/crontab.xml`)
Cron job chạy mỗi đêm lúc 01:00 AM để tổng hợp dữ liệu ngày hôm trước:

```xml
<?xml version="1.0"?>
<!--
  ~ Copyright © Magestore. All rights reserved.
  ~ See COPYING.txt for license details.
  -->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Cron:etc/crontab.xsd">
    <group id="default">
        <job name="aggregate_{vendor}_{module}_sales_report"
             instance="{Vendor}\{ModuleName}\Model\Cron\Aggregate{ReportName}"
             method="execute">
            <schedule>0 1 * * *</schedule>
        </job>
    </group>
</config>
```

### 5.2. Cron Job Class (`Model/Cron/Aggregate{ReportName}.php`)

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\Cron;

use {Vendor}\{ModuleName}\Model\ResourceModel\Report\{ReportName} as ReportResource;
use Magento\Framework\Stdlib\DateTime\DateTime;
use Psr\Log\LoggerInterface;

class Aggregate{ReportName}
{
    private ReportResource $reportResource;
    private DateTime $dateTime;
    private LoggerInterface $logger;

    /**
     * Constructor.
     *
     * @param ReportResource $reportResource
     * @param DateTime $dateTime
     * @param LoggerInterface $logger
     */
    public function __construct(
        ReportResource $reportResource,
        DateTime $dateTime,
        LoggerInterface $logger
    ) {
        $this->reportResource = $reportResource;
        $this->dateTime = $dateTime;
        $this->logger = $logger;
    }

    /**
     * Execute cron daily aggregation.
     *
     * @return void
     */
    public function execute(): void
    {
        try {
            $yesterday = date("Y-m-d 00:00:00", strtotime("-1 day", $this->dateTime->gmtTimestamp()));
            $today = date("Y-m-d 23:59:59", $this->dateTime->gmtTimestamp());
            $this->reportResource->aggregate($yesterday, $today);
        } catch (\Throwable $e) {
            $this->logger->error("Report aggregation failed: " . $e->getMessage());
        }
    }
}
```

---

## 6. Bước 4: Xây dựng Report Collection (`Model/ResourceModel/Report/{ReportName}/Collection.php`)

Report Collection kế thừa `AbstractCollection` của Magento Reports để thừa hưởng:
- Cơ chế lọc theo ngày/tháng/năm (`period` grouping: Day, Month, Year).
- Cơ chế lọc theo Store View (`store_id`).
- Cơ chế tự động điền các khoảng trống ngày bằng `0` (Empty Rows Filling).

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\ResourceModel\Report\{ReportName};

use Magento\Reports\Model\ResourceModel\Report\Collection\AbstractCollection;

class Collection extends AbstractCollection
{
    /**
     * Period format string.
     *
     * @var string
     */
    protected $_periodFormat = "%Y-%m-%d";

    /**
     * Selected columns for report aggregation.
     *
     * @var array
     */
    protected $_selectedColumns = [];

    /**
     * Initialize collection.
     *
     * @return void
     */
    protected function _construct(): void
    {
        parent::_construct();
        $this->setModel(\Magento\Framework\DataObject::class);
        $this->_resource = $this->_resourceFactory->create(
            \{Vendor}\{ModuleName}\Model\ResourceModel\Report\{ReportName}::class
        );
        $this->setMainTable("{vendor}_{module}_sales_aggregated");
    }

    /**
     * Prepare custom columns mapping.
     *
     * @return $this
     */
    protected function _initSelect(): self
    {
        $this->_selectedColumns = [
            "period" => "period",
            "orders_count" => "SUM(orders_count)",
            "total_qty" => "SUM(total_qty)",
            "total_revenue" => "SUM(total_revenue)",
            "total_tax" => "SUM(total_tax)",
            "total_discount" => "SUM(total_discount)"
        ];

        $this->getSelect()->from($this->getMainTable(), $this->_selectedColumns);
        $this->getSelect()->group("period");
        return $this;
    }

    /**
     * Apply date range filter.
     *
     * @param string|null $from
     * @param string|null $to
     * @return $this
     */
    public function setDateRange(?string $from, ?string $to): self
    {
        $this->_from = $from;
        $this->_to = $to;
        return $this;
    }

    /**
     * Apply period grouping (day, month, year).
     *
     * @param string $period
     * @return $this
     */
    public function setPeriod(string $period): self
    {
        $this->_period = $period;
        return $this;
    }

    /**
     * Apply store filter to collection.
     *
     * @param array|int $storeIds
     * @return $this
     */
    public function setStoreIds($storeIds): self
    {
        $this->_stores = $storeIds;
        return $this;
    }
}
```

---

## 7. Bước 5: Giao diện Báo cáo Admin (Container, Filter Form & Grid)

### 7.1. Container Block (`Block/Adminhtml/Report/{ReportName}/Container.php`)

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Block\Adminhtml\Report\{ReportName};

use Magento\Backend\Block\Widget\Grid\Container;

class Container extends Container
{
    /**
     * Initialize container.
     *
     * @return void
     */
    protected function _construct(): void
    {
        $this->_blockGroup = "{Vendor}_{ModuleName}";
        $this->_controller = "adminhtml_report_{reportname}";
        $this->_headerText = __("Sales Summary Report");
        parent::_construct();
        $this->buttonList->remove("add");
    }
}
```

### 7.2. Report Grid Block (`Block/Adminhtml/Report/{ReportName}/Grid.php`)

Class này kế thừa `\Magento\Reports\Block\Adminhtml\Grid\AbstractGrid` để tích hợp:
- Bộ lọc thời gian chuẩn (Period: Ngày / Tháng / Năm, From Date, To Date).
- Store Switcher.
- Nút xuất file CSV và Excel.

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Block\Adminhtml\Report\{ReportName};

use {Vendor}\{ModuleName}\Model\ResourceModel\Report\{ReportName}\CollectionFactory;
use Magento\Backend\Block\Template\Context;
use Magento\Backend\Helper\Data as BackendHelper;
use Magento\Reports\Block\Adminhtml\Grid\AbstractGrid;

class Grid extends AbstractGrid
{
    private CollectionFactory $collectionFactory;

    /**
     * Constructor.
     *
     * @param Context $context
     * @param BackendHelper $backendHelper
     * @param CollectionFactory $collectionFactory
     * @param array $data
     */
    public function __construct(
        Context $context,
        BackendHelper $backendHelper,
        CollectionFactory $collectionFactory,
        array $data = []
    ) {
        $this->collectionFactory = $collectionFactory;
        parent::__construct($context, $backendHelper, $data);
    }

    /**
     * Initialize grid properties.
     *
     * @return void
     */
    protected function _construct(): void
    {
        parent::_construct();
        $this->setId("salesSummaryReportGrid");
        $this->setDefaultSort("period");
        $this->setDefaultDir("DESC");
        $this->setSaveParametersInSession(true);
    }

    /**
     * Prepare report collection.
     *
     * @return $this
     */
    protected function _prepareCollection(): self
    {
        parent::_prepareCollection();
        $collection = $this->collectionFactory->create();
        $this->_setCollectionOrder($collection);
        $this->setCollection($collection);
        return $this;
    }

    /**
     * Prepare grid columns.
     *
     * @return $this
     */
    protected function _prepareColumns(): self
    {
        $this->addColumn(
            "period",
            [
                "header" => __("Period"),
                "index" => "period",
                "width" => 100,
                "sortable" => false,
                "header_css_class" => "col-period",
                "column_css_class" => "col-period"
            ]
        );

        $this->addColumn(
            "orders_count",
            [
                "header" => __("Orders Count"),
                "index" => "orders_count",
                "type" => "number",
                "sortable" => false,
                "total" => "sum"
            ]
        );

        $this->addColumn(
            "total_qty",
            [
                "header" => __("Total Qty Ordered"),
                "index" => "total_qty",
                "type" => "number",
                "sortable" => false,
                "total" => "sum"
            ]
        );

        $this->addColumn(
            "total_revenue",
            [
                "header" => __("Total Revenue"),
                "index" => "total_revenue",
                "type" => "currency",
                "currency_code" => $this->_storeManager->getStore()->getBaseCurrencyCode(),
                "sortable" => false,
                "total" => "sum"
            ]
        );

        $this->addExport(
            ["url" => $this->getUrl("*/*/exportCsv", ["_current" => true]), "label" => __("CSV")]
        );
        $this->addExport(
            ["url" => $this->getUrl("*/*/exportExcel", ["_current" => true]), "label" => __("Excel XML")]
        );

        return parent::_prepareColumns();
    }
}
```

---

## 8. Bước 6: Layout XML & Controller Actions

### 8.1. Layout XML (`view/adminhtml/layout/{route}_report_{reportname}_index.xml`)

```xml
<?xml version="1.0"?>
<!--
  ~ Copyright © Magestore. All rights reserved.
  ~ See COPYING.txt for license details.
  -->
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    <update handle="report_sales"/>
    <body>
        <referenceContainer name="content">
            <block class="{Vendor}\{ModuleName}\Block\Adminhtml\Report\{ReportName}\Container"
                   name="report_{reportname}_container"/>
        </referenceContainer>
    </body>
</page>
```

### 8.2. Controller Hiển thị (`Controller/Adminhtml/Report/{ReportName}/Index.php`)

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Controller\Adminhtml\Report\{ReportName};

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\View\Result\Page;
use Magento\Framework\View\Result\PageFactory;

class Index extends Action
{
    public const ADMIN_RESOURCE = "{Vendor}_{ModuleName}::sales_report";

    private PageFactory $resultPageFactory;

    /**
     * Constructor.
     *
     * @param Context $context
     * @param PageFactory $resultPageFactory
     */
    public function __construct(
        Context $context,
        PageFactory $resultPageFactory
    ) {
        parent::__construct($context);
        $this->resultPageFactory = $resultPageFactory;
    }

    /**
     * Execute index action.
     *
     * @return Page
     */
    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->setActiveMenu("{Vendor}_{ModuleName}::sales_report");
        $resultPage->getConfig()->getTitle()->prepend(__("Sales Summary Report"));
        return $resultPage;
    }
}
```

### 8.3. Controller Export CSV Stream (`Controller/Adminhtml/Report/{ReportName}/ExportCsv.php`)

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Controller\Adminhtml\Report\{ReportName};

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Response\Http\FileFactory;
use Magento\Framework\App\ResponseInterface;
use Magento\Framework\View\Result\LayoutFactory;

class ExportCsv extends Action
{
    public const ADMIN_RESOURCE = "{Vendor}_{ModuleName}::sales_report";

    private FileFactory $fileFactory;
    private LayoutFactory $layoutFactory;

    /**
     * Constructor.
     *
     * @param Context $context
     * @param FileFactory $fileFactory
     * @param LayoutFactory $layoutFactory
     */
    public function __construct(
        Context $context,
        FileFactory $fileFactory,
        LayoutFactory $layoutFactory
    ) {
        parent::__construct($context);
        $this->fileFactory = $fileFactory;
        $this->layoutFactory = $layoutFactory;
    }

    /**
     * Export report to CSV.
     *
     * @return ResponseInterface
     */
    public function execute(): ResponseInterface
    {
        $fileName = "sales_summary_report_" . date("Y-m-d_H-i-s") . ".csv";
        $layout = $this->layoutFactory->create();
        $gridBlock = $layout->createBlock(
            \{Vendor}\{ModuleName}\Block\Adminhtml\Report\{ReportName}\Grid::class
        );

        return $this->fileFactory->create(
            $fileName,
            $gridBlock->getCsvFile(),
            \Magento\Framework\App\Filesystem\DirectoryList::VAR_DIR
        );
    }
}
```

---

## 9. Performance & Security Best Practices

1. **Luôn sử dụng Aggregation Table cho dữ liệu lớn:**
   - Tuyệt đối không viết Custom SQL `SELECT SUM(...) FROM sales_order` trực tiếp trong Controller/Block.
   - Bảng Aggregated chỉ chứa số hàng tương đương số ngày hoạt động (vài nghìn bản ghi thay vì hàng triệu đơn).

2. **Tối ưu Index & Composite Key:**
   - Luôn thiết lập Composite Unique Key trên các cột Dimension (`period`, `store_id`, `order_status`).
   - Sử dụng `INSERT ... ON DUPLICATE KEY UPDATE` để việc chạy lại cron hoặc Refresh Statistics có tính lũy kế
     (Idempotent), không gây trùng lặp dữ liệu.

3. **Stream Iterator khi Export:**
   - Khi xuất báo cáo hàng trăm nghìn dòng, sử dụng `\Magento\Framework\App\Response\Http\FileFactory`
     kết hợp Stream Output để dữ liệu ghi trực tiếp ra tệp tin thay vì lưu mảng lớn trong RAM.

4. **Khai báo Class References:**
   - Luôn sử dụng `ClassName::class` trong PHP code, không truyền tên class dạng chuỗi literal.
