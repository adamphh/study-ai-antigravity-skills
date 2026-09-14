---
name: Component Patterns
description: Các patterns phổ biến khi thiết kế React components
---

# Component Patterns

## 1. Container/Presentational Pattern

```jsx
// Container - handles logic
const UserListContainer = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUsers().then(setUsers).finally(() => setLoading(false));
    }, []);

    const handleDelete = (id) => {
        deleteUser(id).then(() => {
            setUsers(prev => prev.filter(u => u.id !== id));
        });
    };

    return <UserList users={users} loading={loading} onDelete={handleDelete} />;
};

// Presentational - only UI
const UserList = ({ users, loading, onDelete }) => {
    if (loading) return <Spinner />;
    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>
                    {user.name}
                    <button onClick={() => onDelete(user.id)}>Delete</button>
                </li>
            ))}
        </ul>
    );
};
```

## 2. Compound Components

```jsx
import { createContext, useContext, useState } from 'react';

const TabsContext = createContext();

const Tabs = ({ children, defaultTab }) => {
    const [activeTab, setActiveTab] = useState(defaultTab);
    
    return (
        <TabsContext.Provider value={{ activeTab, setActiveTab }}>
            <div className="tabs">{children}</div>
        </TabsContext.Provider>
    );
};

const TabList = ({ children }) => (
    <div className="tab-list">{children}</div>
);

const Tab = ({ id, children }) => {
    const { activeTab, setActiveTab } = useContext(TabsContext);
    return (
        <button 
            className={activeTab === id ? 'active' : ''}
            onClick={() => setActiveTab(id)}
        >
            {children}
        </button>
    );
};

const TabPanel = ({ id, children }) => {
    const { activeTab } = useContext(TabsContext);
    return activeTab === id ? <div>{children}</div> : null;
};

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs defaultTab="tab1">
    <Tabs.List>
        <Tabs.Tab id="tab1">Tab 1</Tabs.Tab>
        <Tabs.Tab id="tab2">Tab 2</Tabs.Tab>
    </Tabs.List>
    <Tabs.Panel id="tab1">Content 1</Tabs.Panel>
    <Tabs.Panel id="tab2">Content 2</Tabs.Panel>
</Tabs>
```

## 3. Render Props

```jsx
// Class Component
class MouseTracker extends Component {
    state = { x: 0, y: 0 };

    handleMouseMove = (e) => {
        this.setState({ x: e.clientX, y: e.clientY });
    };

    render() {
        return (
            <div onMouseMove={this.handleMouseMove}>
                {this.props.render(this.state)}
            </div>
        );
    }
}

// Function Component
const MouseTracker = ({ render }) => {
    const [position, setPosition] = useState({ x: 0, y: 0 });

    const handleMouseMove = (e) => {
        setPosition({ x: e.clientX, y: e.clientY });
    };

    return <div onMouseMove={handleMouseMove}>{render(position)}</div>;
};

// Usage
<MouseTracker render={({ x, y }) => (
    <p>Mouse position: {x}, {y}</p>
)} />

// Or with children
<MouseTracker>
    {({ x, y }) => <p>Position: {x}, {y}</p>}
</MouseTracker>
```

## 4. Higher-Order Components (HOC)

```jsx
// HOC - adds functionality to component
const withLoading = (WrappedComponent) => {
    return function WithLoadingComponent({ loading, ...props }) {
        if (loading) return <Spinner />;
        return <WrappedComponent {...props} />;
    };
};

const withAuth = (WrappedComponent) => {
    return function WithAuthComponent(props) {
        const { user } = useAuth();
        if (!user) return <Navigate to="/login" />;
        return <WrappedComponent {...props} user={user} />;
    };
};

// Usage
const UserProfile = ({ user }) => <div>{user.name}</div>;

const ProtectedUserProfile = withAuth(UserProfile);
const LoadableUserList = withLoading(UserList);

// Compose multiple HOCs
const EnhancedComponent = withAuth(withLoading(UserProfile));
```

## 5. Controlled vs Uncontrolled

```jsx
// Controlled - state managed by parent
const ControlledInput = ({ value, onChange }) => (
    <input value={value} onChange={e => onChange(e.target.value)} />
);

// Uncontrolled - state managed internally
const UncontrolledInput = ({ defaultValue, onSubmit }) => {
    const inputRef = useRef();
    
    const handleSubmit = () => {
        onSubmit(inputRef.current.value);
    };

    return (
        <>
            <input ref={inputRef} defaultValue={defaultValue} />
            <button onClick={handleSubmit}>Submit</button>
        </>
    );
};

// Hybrid - controlled with internal fallback
const FlexibleInput = ({ value, onChange, defaultValue = '' }) => {
    const [internalValue, setInternalValue] = useState(defaultValue);
    const isControlled = value !== undefined;
    const currentValue = isControlled ? value : internalValue;

    const handleChange = (e) => {
        if (!isControlled) setInternalValue(e.target.value);
        onChange?.(e.target.value);
    };

    return <input value={currentValue} onChange={handleChange} />;
};
```

## 6. Forwarding Refs

```jsx
import { forwardRef, useImperativeHandle, useRef } from 'react';

// Basic ref forwarding
const FancyInput = forwardRef((props, ref) => (
    <input ref={ref} className="fancy" {...props} />
));

// Usage
const Parent = () => {
    const inputRef = useRef();
    return <FancyInput ref={inputRef} />;
};

// Custom ref handle
const CustomInput = forwardRef((props, ref) => {
    const inputRef = useRef();

    useImperativeHandle(ref, () => ({
        focus: () => inputRef.current.focus(),
        clear: () => { inputRef.current.value = ''; },
        getValue: () => inputRef.current.value
    }));

    return <input ref={inputRef} {...props} />;
});

// Usage
const Form = () => {
    const customRef = useRef();

    const handleSubmit = () => {
        console.log(customRef.current.getValue());
        customRef.current.clear();
    };

    return <CustomInput ref={customRef} />;
};
```

## Pattern Comparison

| Pattern | Use Case |
|---------|----------|
| Container/Presentational | Separate logic from UI |
| Compound Components | Related components that share state |
| Render Props | Share behavior between components |
| HOC | Add reusable functionality |
| Controlled/Uncontrolled | Form input management |
| Forwarding Refs | Expose DOM refs from components |
