---
name: Class Component Basics
description: Hướng dẫn tạo Class Component trong React
---

# Class Component trong React

## Cấu trúc cơ bản

```jsx
import React, { Component } from 'react';

class MyComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            count: 0,
            name: ''
        };
        // Bind methods
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        this.setState({ count: this.state.count + 1 });
    }

    render() {
        return (
            <div>
                <h1>Hello, {this.props.title}</h1>
                <p>Count: {this.state.count}</p>
                <button onClick={this.handleClick}>Increment</button>
            </div>
        );
    }
}

export default MyComponent;
```

## Arrow Function Methods (không cần bind)

```jsx
class MyComponent extends Component {
    state = {
        count: 0
    };

    // Arrow function - auto-bound
    handleClick = () => {
        this.setState({ count: this.state.count + 1 });
    };

    render() {
        return <button onClick={this.handleClick}>Click</button>;
    }
}
```

## Lifecycle Methods

```jsx
class LifecycleComponent extends Component {
    // 1. Mounting - Component được tạo
    constructor(props) {
        super(props);
        console.log('1. Constructor');
    }

    static getDerivedStateFromProps(props, state) {
        // Sync state với props
        console.log('2. getDerivedStateFromProps');
        return null;
    }

    componentDidMount() {
        // Component đã mount - fetch data, subscribe events
        console.log('4. componentDidMount');
    }

    // 2. Updating - Props hoặc State thay đổi
    shouldComponentUpdate(nextProps, nextState) {
        // Return false để ngăn re-render
        console.log('shouldComponentUpdate');
        return true;
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        // Capture thông tin trước khi DOM update
        console.log('getSnapshotBeforeUpdate');
        return null;
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // Sau khi update - so sánh props/state cũ với mới
        console.log('componentDidUpdate');
        if (prevProps.id !== this.props.id) {
            this.fetchData(this.props.id);
        }
    }

    // 3. Unmounting - Component bị remove
    componentWillUnmount() {
        // Cleanup - unsubscribe, clear timers
        console.log('componentWillUnmount');
    }

    render() {
        console.log('3. Render');
        return <div>Lifecycle Demo</div>;
    }
}
```

## setState Chi tiết

```jsx
class StatefulComponent extends Component {
    state = { count: 0, items: [] };

    // 1. Object form
    incrementBasic = () => {
        this.setState({ count: this.state.count + 1 });
    };

    // 2. Functional form (an toàn với async)
    incrementSafe = () => {
        this.setState((prevState) => ({
            count: prevState.count + 1
        }));
    };

    // 3. Với callback sau khi update
    incrementWithCallback = () => {
        this.setState(
            { count: this.state.count + 1 },
            () => {
                console.log('State updated:', this.state.count);
            }
        );
    };

    // 4. Merge state (chỉ update count, giữ nguyên items)
    updatePartial = () => {
        this.setState({ count: 10 }); // items không bị ảnh hưởng
    };
}
```

## Handling Events

```jsx
class EventComponent extends Component {
    handleChange = (event) => {
        this.setState({ value: event.target.value });
    };

    handleSubmit = (event) => {
        event.preventDefault();
        console.log('Submitted:', this.state.value);
    };

    // Passing arguments
    handleItemClick = (id) => (event) => {
        console.log('Item clicked:', id);
    };

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <input 
                    type="text" 
                    value={this.state.value} 
                    onChange={this.handleChange} 
                />
                <button type="submit">Submit</button>
                
                {this.state.items.map(item => (
                    <div key={item.id} onClick={this.handleItemClick(item.id)}>
                        {item.name}
                    </div>
                ))}
            </form>
        );
    }
}
```

## Refs trong Class Component

```jsx
class RefComponent extends Component {
    constructor(props) {
        super(props);
        this.inputRef = React.createRef();
    }

    focusInput = () => {
        this.inputRef.current.focus();
    };

    render() {
        return (
            <>
                <input ref={this.inputRef} type="text" />
                <button onClick={this.focusInput}>Focus</button>
            </>
        );
    }
}
```
