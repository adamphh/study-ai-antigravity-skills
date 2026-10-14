---
name: Form Handling
description: Hướng dẫn xử lý Form trong React (Class và Function Component)
---

# Form Handling trong React

## Class Component - Controlled Form

```jsx
import React, { Component } from 'react';

class LoginForm extends Component {
    state = {
        email: '',
        password: '',
        rememberMe: false,
        role: 'user',
        errors: {}
    };

    handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        this.setState({
            [name]: type === 'checkbox' ? checked : value
        });
    };

    validate = () => {
        const errors = {};
        if (!this.state.email) {
            errors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(this.state.email)) {
            errors.email = 'Email is invalid';
        }
        if (!this.state.password) {
            errors.password = 'Password is required';
        }
        return errors;
    };

    handleSubmit = (e) => {
        e.preventDefault();
        const errors = this.validate();
        if (Object.keys(errors).length === 0) {
            console.log('Form data:', this.state);
            this.props.onSubmit(this.state);
        } else {
            this.setState({ errors });
        }
    };

    render() {
        const { email, password, rememberMe, role, errors } = this.state;

        return (
            <form onSubmit={this.handleSubmit}>
                <div>
                    <input
                        type="email"
                        name="email"
                        value={email}
                        onChange={this.handleChange}
                        placeholder="Email"
                    />
                    {errors.email && <span className="error">{errors.email}</span>}
                </div>

                <div>
                    <input
                        type="password"
                        name="password"
                        value={password}
                        onChange={this.handleChange}
                        placeholder="Password"
                    />
                    {errors.password && <span className="error">{errors.password}</span>}
                </div>

                <label>
                    <input
                        type="checkbox"
                        name="rememberMe"
                        checked={rememberMe}
                        onChange={this.handleChange}
                    />
                    Remember me
                </label>

                <select name="role" value={role} onChange={this.handleChange}>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                </select>

                <button type="submit">Login</button>
            </form>
        );
    }
}
```

## Function Component - Controlled Form

```jsx
import { useState } from 'react';

const LoginForm = ({ onSubmit }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        rememberMe: false
    });
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
        // Clear error when user types
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const validate = () => {
        const newErrors = {};
        if (!formData.email) newErrors.email = 'Email required';
        if (!formData.password) newErrors.password = 'Password required';
        return newErrors;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const newErrors = validate();
        if (Object.keys(newErrors).length === 0) {
            onSubmit(formData);
        } else {
            setErrors(newErrors);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
            />
            {errors.email && <span>{errors.email}</span>}

            <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
            />
            {errors.password && <span>{errors.password}</span>}

            <button type="submit">Submit</button>
        </form>
    );
};
```

## Custom useForm Hook

```jsx
import { useState, useCallback } from 'react';

const useForm = (initialValues, validate) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleChange = useCallback((e) => {
        const { name, value, type, checked } = e.target;
        setValues(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    }, []);

    const handleSubmit = useCallback((onSubmit) => (e) => {
        e.preventDefault();
        const validationErrors = validate ? validate(values) : {};
        setErrors(validationErrors);

        if (Object.keys(validationErrors).length === 0) {
            setIsSubmitting(true);
            onSubmit(values);
            setIsSubmitting(false);
        }
    }, [values, validate]);

    const reset = useCallback(() => {
        setValues(initialValues);
        setErrors({});
    }, [initialValues]);

    return { values, errors, isSubmitting, handleChange, handleSubmit, reset };
};

// Usage
const ContactForm = () => {
    const validate = (values) => {
        const errors = {};
        if (!values.name) errors.name = 'Name required';
        if (!values.email) errors.email = 'Email required';
        return errors;
    };

    const { values, errors, handleChange, handleSubmit } = useForm(
        { name: '', email: '', message: '' },
        validate
    );

    const onSubmit = (data) => {
        console.log('Submitted:', data);
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input name="name" value={values.name} onChange={handleChange} />
            {errors.name && <span>{errors.name}</span>}
            
            <input name="email" value={values.email} onChange={handleChange} />
            {errors.email && <span>{errors.email}</span>}
            
            <textarea name="message" value={values.message} onChange={handleChange} />
            
            <button type="submit">Send</button>
        </form>
    );
};
```

## Uncontrolled Form với useRef

```jsx
import { useRef } from 'react';

const UncontrolledForm = ({ onSubmit }) => {
    const emailRef = useRef();
    const passwordRef = useRef();

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            email: emailRef.current.value,
            password: passwordRef.current.value
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="email" ref={emailRef} defaultValue="" />
            <input type="password" ref={passwordRef} defaultValue="" />
            <button type="submit">Submit</button>
        </form>
    );
};
```

## File Upload

```jsx
const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState('');

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);

        // Preview image
        if (selectedFile && selectedFile.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onloadend = () => setPreview(reader.result);
            reader.readAsDataURL(selectedFile);
        }
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);
        await fetch('/api/upload', { method: 'POST', body: formData });
    };

    return (
        <div>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            {preview && <img src={preview} alt="Preview" />}
            <button onClick={handleUpload} disabled={!file}>Upload</button>
        </div>
    );
};
```
