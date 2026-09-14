---
name: Create ACL (Admin Permissions)
description: Hướng dẫn tạo ACL để quản lý quyền Admin trong Magento 2
---

# Tạo ACL (Admin Permissions) trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
└── etc/
    └── acl.xml
```

## 1. Định nghĩa ACL

`etc/acl.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Acl/etc/acl.xsd">
    <acl>
        <resources>
            <resource id="Magento_Backend::admin">
                
                <!-- Top-level menu permission -->
                <resource id="{Vendor}_{ModuleName}::menu" 
                          title="{Module Name}" 
                          sortOrder="100">
                    
                    <!-- Sub-menu / Feature permissions -->
                    <resource id="{Vendor}_{ModuleName}::manage" 
                              title="Manage Entities" 
                              sortOrder="10">
                        
                        <!-- CRUD permissions -->
                        <resource id="{Vendor}_{ModuleName}::view" 
                                  title="View" 
                                  sortOrder="10"/>
                        <resource id="{Vendor}_{ModuleName}::create" 
                                  title="Create" 
                                  sortOrder="20"/>
                        <resource id="{Vendor}_{ModuleName}::edit" 
                                  title="Edit" 
                                  sortOrder="30"/>
                        <resource id="{Vendor}_{ModuleName}::delete" 
                                  title="Delete" 
                                  sortOrder="40"/>
                    </resource>
                    
                </resource>
                
                <!-- Configuration permission -->
                <resource id="Magento_Backend::stores">
                    <resource id="Magento_Backend::stores_settings">
                        <resource id="Magento_Config::config">
                            <resource id="{Vendor}_{ModuleName}::config" 
                                      title="{Module Name} Configuration"/>
                        </resource>
                    </resource>
                </resource>
                
            </resource>
        </resources>
    </acl>
</config>
```

## 2. Sử dụng trong Admin Controller

```php
<?php
namespace {Vendor}\{ModuleName}\Controller\Adminhtml\{Entity};

use Magento\Backend\App\Action;

class Index extends Action
{
    /**
     * ACL resource để kiểm tra quyền
     */
    public const ADMIN_RESOURCE = '{Vendor}_{ModuleName}::view';

    public function execute()
    {
        // Controller logic
    }
}
```

## 3. Sử dụng trong Menu

`etc/adminhtml/menu.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Backend:etc/menu.xsd">
    <menu>
        <add id="{Vendor}_{ModuleName}::menu"
             title="{Module Name}"
             module="{Vendor}_{ModuleName}"
             sortOrder="100"
             resource="{Vendor}_{ModuleName}::menu"/>
             
        <add id="{Vendor}_{ModuleName}::manage"
             title="Manage Entities"
             module="{Vendor}_{ModuleName}"
             sortOrder="10"
             parent="{Vendor}_{ModuleName}::menu"
             action="{route}/entity/index"
             resource="{Vendor}_{ModuleName}::manage"/>
    </menu>
</config>
```

## 4. Sử dụng trong System Config

`etc/adminhtml/system.xml`

```xml
<section id="{vendor}_{modulename}" ...>
    <resource>{Vendor}_{ModuleName}::config</resource>
    ...
</section>
```

## 5. Kiểm tra quyền trong Code

```php
<?php
use Magento\Framework\AuthorizationInterface;

class SomeClass
{
    private AuthorizationInterface $authorization;
    
    public function __construct(AuthorizationInterface $authorization)
    {
        $this->authorization = $authorization;
    }
    
    public function canDelete(): bool
    {
        return $this->authorization->isAllowed('{Vendor}_{ModuleName}::delete');
    }
}
```

## 6. Kiểm tra quyền trong Template

```php
<?php if ($block->getAuthorization()->isAllowed('{Vendor}_{ModuleName}::edit')): ?>
    <button>Edit</button>
<?php endif; ?>
```

## Cấu trúc ACL phổ biến

```
Magento_Backend::admin
├── {Vendor}_{ModuleName}::menu          # Menu access
│   ├── {Vendor}_{ModuleName}::manage    # Feature access
│   │   ├── {Vendor}_{ModuleName}::view
│   │   ├── {Vendor}_{ModuleName}::create
│   │   ├── {Vendor}_{ModuleName}::edit
│   │   └── {Vendor}_{ModuleName}::delete
│   └── {Vendor}_{ModuleName}::settings  # Settings access
└── Magento_Backend::stores
    └── Magento_Config::config
        └── {Vendor}_{ModuleName}::config # System config access
```
