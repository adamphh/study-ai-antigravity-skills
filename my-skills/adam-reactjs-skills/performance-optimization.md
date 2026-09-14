---
name: Performance Optimization
description: Hướng dẫn tối ưu performance trong React
---

# Performance Optimization

## Class Component - shouldComponentUpdate

```jsx
import React, { Component, PureComponent } from 'react';

// Manual optimization
class OptimizedComponent extends Component {
    shouldComponentUpdate(nextProps, nextState) {
        // Only re-render if specific props/state changed
        return (
            nextProps.id !== this.props.id ||
            nextState.count !== this.state.count
        );
    }

    render() {
        return <div>{this.props.name}</div>;
    }
}

// PureComponent - shallow comparison automatically
class PureListItem extends PureComponent {
    render() {
        console.log('Rendering:', this.props.name);
        return <li>{this.props.name}</li>;
    }
}
```

## Function Component - React.memo

```jsx
import React, { memo, useMemo, useCallback } from 'react';

// Basic memo - shallow comparison
const ListItem = memo(({ name, onClick }) => {
    console.log('Rendering:', name);
    return <li onClick={onClick}>{name}</li>;
});

// Custom comparison function
const ExpensiveComponent = memo(
    ({ data, config }) => {
        return <div>{/* expensive render */}</div>;
    },
    (prevProps, nextProps) => {
        // Return true to skip re-render
        return prevProps.data.id === nextProps.data.id;
    }
);
```

## useMemo - Cache Computed Values

```jsx
const ProductList = ({ products, filter, sortBy }) => {
    // Without useMemo - recalculates every render
    // const filteredProducts = products.filter(p => p.category === filter);

    // With useMemo - only recalculates when dependencies change
    const filteredProducts = useMemo(() => {
        console.log('Filtering products...');
        return products
            .filter(p => p.category === filter)
            .sort((a, b) => a[sortBy] - b[sortBy]);
    }, [products, filter, sortBy]);

    // Cache expensive object creation
    const chartData = useMemo(() => ({
        labels: filteredProducts.map(p => p.name),
        values: filteredProducts.map(p => p.price)
    }), [filteredProducts]);

    return (
        <div>
            {filteredProducts.map(p => <ProductCard key={p.id} product={p} />)}
            <Chart data={chartData} />
        </div>
    );
};
```

## useCallback - Cache Functions

```jsx
const ParentComponent = () => {
    const [count, setCount] = useState(0);
    const [items, setItems] = useState([]);

    // Without useCallback - new function every render
    // const handleClick = (id) => console.log(id);

    // With useCallback - same function reference
    const handleClick = useCallback((id) => {
        console.log('Clicked:', id);
    }, []); // No dependencies = never changes

    const handleDelete = useCallback((id) => {
        setItems(prev => prev.filter(item => item.id !== id));
    }, []); // Uses functional update, no external deps

    const handleAdd = useCallback((item) => {
        setItems(prev => [...prev, { ...item, addedAt: count }]);
    }, [count]); // Depends on count

    return (
        <div>
            <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
            {items.map(item => (
                <MemoizedItem 
                    key={item.id} 
                    item={item}
                    onClick={handleClick}
                    onDelete={handleDelete}
                />
            ))}
        </div>
    );
};

const MemoizedItem = memo(({ item, onClick, onDelete }) => {
    console.log('Rendering item:', item.id);
    return (
        <div onClick={() => onClick(item.id)}>
            {item.name}
            <button onClick={() => onDelete(item.id)}>Delete</button>
        </div>
    );
});
```

## Lazy Loading Components

```jsx
import { lazy, Suspense, useState } from 'react';

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const AdminPanel = lazy(() => import('./AdminPanel'));

const App = () => {
    const [showChart, setShowChart] = useState(false);

    return (
        <div>
            <button onClick={() => setShowChart(true)}>Load Chart</button>
            
            {showChart && (
                <Suspense fallback={<div>Loading chart...</div>}>
                    <HeavyChart />
                </Suspense>
            )}

            {/* Multiple lazy components */}
            <Suspense fallback={<div>Loading...</div>}>
                <AdminPanel />
            </Suspense>
        </div>
    );
};
```

## Virtualized Lists

```jsx
import { FixedSizeList } from 'react-window';

const VirtualizedList = ({ items }) => {
    const Row = ({ index, style }) => (
        <div style={style}>
            {items[index].name}
        </div>
    );

    return (
        <FixedSizeList
            height={400}
            width={300}
            itemCount={items.length}
            itemSize={50}
        >
            {Row}
        </FixedSizeList>
    );
};
```

## Code Splitting by Route

```jsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Products = lazy(() => import('./pages/Products'));
const Admin = lazy(() => import('./pages/Admin'));

const App = () => (
    <Suspense fallback={<div>Loading...</div>}>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
            <Route path="/admin/*" element={<Admin />} />
        </Routes>
    </Suspense>
);
```

## Performance Tips

| Technique | When to Use |
|-----------|-------------|
| `React.memo` | Prevent re-render of child components |
| `useMemo` | Cache expensive calculations |
| `useCallback` | Cache callbacks passed to children |
| `lazy/Suspense` | Code split heavy components |
| `react-window` | Render large lists efficiently |
| `PureComponent` | Class component shallow comparison |
