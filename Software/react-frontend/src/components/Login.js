import React from "react";
import Form from 'react-bootstrap/Form';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Button from 'react-bootstrap/Button';
import { useState } from 'react';
import { Router } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  function handleUsernameChange(e) {
    setUsername(e.target.value);
  }
  function handlePasswordChange(e) {
    setPassword(e.target.value);
  }

  function login(){
    if (username === "raor3" && password === "password"){
      this.props.history.push('/instructor');
    }
  }


  return(
  <Form className="centered-form">
    <Form.Group className="mb-3">
      <FloatingLabel controlId="floatingInput" label="Username">
        <Form.Control type="input" placeholder="Username" onChange={handleUsernameChange}/>
      </FloatingLabel>
    </Form.Group>

    <Form.Group className="mb-3">
      <FloatingLabel controlId="floatingPassword" label="Password">
        <Form.Control type="password" placeholder="Password" onChange={handlePasswordChange}/>
      </FloatingLabel>
    </Form.Group>
    <div className="d-grid gap-2">
      
      <Button variant="primary" size="lg" onClick={login}>Log In</Button>
    </div>
  </Form>
  )}
