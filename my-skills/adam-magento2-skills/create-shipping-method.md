---
name: Create Shipping Method
description: Hướng dẫn tạo Shipping Method trong Magento 2
---

# Tạo Shipping Method trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   ├── config.xml
│   └── adminhtml/
│       └── system.xml
├── Model/
│   └── Carrier/
│       └── {CarrierName}.php
```

## 1. Carrier Model

`Model/Carrier/{CarrierName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\Carrier;

use Magento\Framework\App\Config\ScopeConfigInterface;
use Magento\Quote\Model\Quote\Address\RateRequest;
use Magento\Quote\Model\Quote\Address\RateResult\ErrorFactory;
use Magento\Quote\Model\Quote\Address\RateResult\MethodFactory;
use Magento\Shipping\Model\Carrier\AbstractCarrier;
use Magento\Shipping\Model\Carrier\CarrierInterface;
use Magento\Shipping\Model\Rate\ResultFactory;
use Psr\Log\LoggerInterface;

class {CarrierName} extends AbstractCarrier implements CarrierInterface
{
    protected $_code = '{carrier_code}';
    protected $_isFixed = true;

    private ResultFactory $rateResultFactory;
    private MethodFactory $rateMethodFactory;

    public function __construct(
        ScopeConfigInterface $scopeConfig,
        ErrorFactory $rateErrorFactory,
        LoggerInterface $logger,
        ResultFactory $rateResultFactory,
        MethodFactory $rateMethodFactory,
        array $data = []
    ) {
        $this->rateResultFactory = $rateResultFactory;
        $this->rateMethodFactory = $rateMethodFactory;
        parent::__construct($scopeConfig, $rateErrorFactory, $logger, $data);
    }

    /**
     * Collect and get rates
     */
    public function collectRates(RateRequest $request)
    {
        if (!$this->getConfigFlag('active')) {
            return false;
        }

        $result = $this->rateResultFactory->create();

        // Check if shipping is available for destination
        if (!$this->isAvailable($request)) {
            return false;
        }

        // Add shipping method
        $method = $this->rateMethodFactory->create();
        $method->setCarrier($this->_code);
        $method->setCarrierTitle($this->getConfigData('title'));
        $method->setMethod('standard');
        $method->setMethodTitle($this->getConfigData('name'));

        // Calculate shipping price
        $shippingPrice = $this->calculatePrice($request);
        $method->setPrice($shippingPrice);
        $method->setCost($shippingPrice);

        $result->append($method);

        // Add express method (optional)
        if ($this->getConfigFlag('enable_express')) {
            $expressMethod = $this->rateMethodFactory->create();
            $expressMethod->setCarrier($this->_code);
            $expressMethod->setCarrierTitle($this->getConfigData('title'));
            $expressMethod->setMethod('express');
            $expressMethod->setMethodTitle('Express Delivery');
            $expressMethod->setPrice($shippingPrice * 1.5);
            $expressMethod->setCost($shippingPrice * 1.5);
            $result->append($expressMethod);
        }

        return $result;
    }

    /**
     * Get allowed shipping methods
     */
    public function getAllowedMethods(): array
    {
        return [
            'standard' => $this->getConfigData('name'),
            'express' => 'Express Delivery'
        ];
    }

    /**
     * Calculate shipping price based on request
     */
    private function calculatePrice(RateRequest $request): float
    {
        $basePrice = (float)$this->getConfigData('price');
        
        // Free shipping threshold
        $freeShippingThreshold = (float)$this->getConfigData('free_shipping_threshold');
        if ($freeShippingThreshold > 0 && $request->getPackageValue() >= $freeShippingThreshold) {
            return 0;
        }

        // Price per kg
        $pricePerKg = (float)$this->getConfigData('price_per_kg');
        if ($pricePerKg > 0 && $request->getPackageWeight() > 0) {
            $basePrice += $request->getPackageWeight() * $pricePerKg;
        }

        return $basePrice;
    }

    /**
     * Check if shipping is available
     */
    private function isAvailable(RateRequest $request): bool
    {
        $destCountry = $request->getDestCountryId();
        $allowedCountries = explode(',', $this->getConfigData('specificcountry') ?? '');
        
        if ($this->getConfigData('sallowspecific') && !in_array($destCountry, $allowedCountries)) {
            return false;
        }
        
        return true;
    }
}
```

## 2. Config mặc định

`etc/config.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Store:etc/config.xsd">
    <default>
        <carriers>
            <{carrier_code}>
                <active>1</active>
                <model>{Vendor}\{ModuleName}\Model\Carrier\{CarrierName}</model>
                <title>Carrier Title</title>
                <name>Standard Shipping</name>
                <price>5.00</price>
                <price_per_kg>0</price_per_kg>
                <free_shipping_threshold>100</free_shipping_threshold>
                <sallowspecific>0</sallowspecific>
                <sort_order>100</sort_order>
            </{carrier_code}>
        </carriers>
    </default>
</config>
```

## 3. Admin System Config

`etc/adminhtml/system.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Config:etc/system_file.xsd">
    <system>
        <section id="carriers">
            <group id="{carrier_code}" translate="label" sortOrder="100" showInDefault="1" showInWebsite="1" showInStore="1">
                <label>Custom Carrier</label>
                
                <field id="active" translate="label" type="select" sortOrder="10" showInDefault="1" showInWebsite="1">
                    <label>Enabled</label>
                    <source_model>Magento\Config\Model\Config\Source\Yesno</source_model>
                </field>
                
                <field id="title" translate="label" type="text" sortOrder="20" showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Title</label>
                </field>
                
                <field id="name" translate="label" type="text" sortOrder="30" showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Method Name</label>
                </field>
                
                <field id="price" translate="label" type="text" sortOrder="40" showInDefault="1" showInWebsite="1">
                    <label>Shipping Price</label>
                    <validate>validate-number validate-zero-or-greater</validate>
                </field>
                
                <field id="free_shipping_threshold" translate="label" type="text" sortOrder="50" showInDefault="1" showInWebsite="1">
                    <label>Free Shipping Threshold</label>
                    <comment>Free shipping if order total >= this value (0 = disabled)</comment>
                </field>
                
                <field id="sallowspecific" translate="label" type="select" sortOrder="60" showInDefault="1" showInWebsite="1">
                    <label>Ship to Applicable Countries</label>
                    <source_model>Magento\Shipping\Model\Config\Source\Allspecificcountries</source_model>
                </field>
                
                <field id="specificcountry" translate="label" type="multiselect" sortOrder="70" showInDefault="1" showInWebsite="1">
                    <label>Ship to Specific Countries</label>
                    <source_model>Magento\Directory\Model\Config\Source\Country</source_model>
                </field>
                
                <field id="sort_order" translate="label" type="text" sortOrder="100" showInDefault="1" showInWebsite="1">
                    <label>Sort Order</label>
                </field>
            </group>
        </section>
    </system>
</config>
```

## Tracking Support

Thêm tracking vào carrier:

```php
protected $_isFixed = false;
protected $_canTrack = true;

public function getTrackingInfo($trackingNumber)
{
    $tracking = $this->_trackStatusFactory->create();
    $tracking->setCarrier($this->_code);
    $tracking->setCarrierTitle($this->getConfigData('title'));
    $tracking->setTracking($trackingNumber);
    $tracking->setUrl('https://tracking-url.com/' . $trackingNumber);
    
    return $tracking;
}
```
