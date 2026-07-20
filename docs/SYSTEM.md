# System Architecture
- Magento 2.4.7
- POS is a PWA
- reactjs ^16.8.6 (not use hooks)
- semantic-ui-react ^0.88.2
- nodejs ^18.x
- npm ^9.x

## Overview
This is an offline-first POS system.
- Magento is the source of truth.
- Browser IndexedDB is the local store.
- POS must work without internet.
- Data consistency > real-time freshness.
- Snapshot + delta sync model.

## Components

- Magento backend
- ReactJS POS client
- IndexedDB local store

## Data Flow

1. Catalog sync
2. Order sync
3. Price sync
4. Inventory sync
5. Catalogrule sync
6. Customer sync
7. Configuration sync

## Failure Modes

1. Network down
2. DB full
3. Concurrent sync
4. Partial sync

## Recovery

1. Resume sync
2. Rebuild from snapshot
3. Manual conflict resolution

## Constraints

- No request should fetch more than 500 records.
- Client must detect missing parts.
- Server must not recompute snapshot per POS.

