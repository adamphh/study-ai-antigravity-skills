## Sync Spec

### Goal:
- Sync 1M+ records without overloading server.

### Constraints:
- Multiple POS sync concurrently.
- Browser storage is IndexedDB.
- Network may drop anytime.

### Strategy:
- Server builds snapshot.
- Client downloads snapshot in parts.
- Client applies deltas incrementally.

### Rules:
