---
name: WebPOS Component and Reducer
description: Hướng dẫn tạo Component, Reducer và Menu trong WebPOS
---

# WebPOS Component và Reducer

## Cấu trúc Extension

```
src/extension/{extension_name}/
├── etc/
│   └── config.js           # Config chính
├── view/
│   ├── index.js            # Export component
│   ├── container.js        # Container component
│   ├── component.js        # Presentational component
│   └── reducer.js          # Redux reducer
├── locales/
│   └── vi_vn/
│       └── translations.json
└── package.json            # Dependencies (optional)
```

## Đăng ký Reducer

`etc/config.js`

```js
import HelloWorld from "../view/reducer";
import ModuleConfigAbstract from "../../ModuleConfigAbstract";

class HelloWorldConfig extends ModuleConfigAbstract {
    module = ['helloworld'];
    reducer = { HelloWorld };
}

export default (new HelloWorldConfig());
```

`view/reducer.js`

```js
const initialState = {
    items: [],
    loading: false,
    error: null
};

const HelloWorld = (state = initialState, action) => {
    switch (action.type) {
        case 'HELLOWORLD_LOAD_REQUEST':
            return { ...state, loading: true };
            
        case 'HELLOWORLD_LOAD_SUCCESS':
            return { ...state, loading: false, items: action.payload };
            
        case 'HELLOWORLD_LOAD_FAILURE':
            return { ...state, loading: false, error: action.error };
            
        default:
            return state;
    }
};

export default HelloWorld;
```

## Đăng ký Menu

`etc/config.js`

```js
import { HelloWorldContainerConnection } from '../view';
import ModuleConfigAbstract from "../../ModuleConfigAbstract";

class HelloWorldConfig extends ModuleConfigAbstract {
    module = ['helloworld'];
    
    menu = {
        helloworld: {
            id: "helloworld",
            title: "Hello World",
            path: "/helloworld",
            component: HelloWorldContainerConnection,
            className: "item-helloworld",
            sortOrder: 50,
            // icon: "icon-class-name"
        }
    };
}

export default (new HelloWorldConfig());
```

## Tạo Container và Component

`view/index.js`

```js
import { connect } from 'react-redux';
import HelloWorldContainer from './container';

const mapStateToProps = (state) => ({
    items: state.extension.HelloWorld.items,
    loading: state.extension.HelloWorld.loading
});

const mapDispatchToProps = (dispatch) => ({
    loadItems: () => dispatch({ type: 'HELLOWORLD_LOAD_REQUEST' }),
    addItem: (item) => dispatch({ type: 'HELLOWORLD_ADD_ITEM', payload: item })
});

export const HelloWorldContainerConnection = connect(
    mapStateToProps,
    mapDispatchToProps
)(HelloWorldContainer);
```

`view/container.js`

```js
import React, { Component } from 'react';
import HelloWorldComponent from './component';

class HelloWorldContainer extends Component {
    componentDidMount() {
        this.props.loadItems();
    }

    render() {
        return (
            <HelloWorldComponent
                items={this.props.items}
                loading={this.props.loading}
                onAddItem={this.props.addItem}
            />
        );
    }
}

export default HelloWorldContainer;
```

`view/component.js`

```js
import React from 'react';

const HelloWorldComponent = ({ items, loading, onAddItem }) => {
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="helloworld-page">
            <h1>Hello World</h1>
            <ul>
                {items.map(item => (
                    <li key={item.id}>{item.name}</li>
                ))}
            </ul>
            <button onClick={() => onAddItem({ id: Date.now(), name: 'New Item' })}>
                Add Item
            </button>
        </div>
    );
};

export default HelloWorldComponent;
```

## Translations

`locales/vi_vn/translations.json`

```json
{
    "Hello World": "Xin chào",
    "Loading...": "Đang tải...",
    "Add Item": "Thêm mục"
}
```

## Additional Packages

`package.json`

```json
{
    "dependencies": {
        "@material-ui/pickers": "3.2.10",
        "@date-io/moment": "1.3.13"
    }
}
```

Chạy để cài packages:
```bash
npm install
npm run upgrade
```

## Các cách đăng ký Component

| Cách | Use Case |
|------|----------|
| `menu` | Tạo menu item mới |
| `layout` | Thêm UI vào customize point |
| `rewrite` | Replace component có sẵn |
| `plugin` | Modify method của component |
| `event` | Listen event và render |
