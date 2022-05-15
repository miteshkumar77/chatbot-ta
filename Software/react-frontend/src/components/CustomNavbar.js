import React from "react";
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import { Link } from "react-router-dom";

const CustomNavbar = () => (
    <Navbar sticky="top" variant="dark" bg="dark">
        <Container>
            <Navbar.Brand>Design Lab's Capstone Chatbot</Navbar.Brand>
            <Nav className="me-auto">
                <Nav.Link href="/">Chat</Nav.Link>
                <Nav.Link href="/search">Search</Nav.Link>
            </Nav>
            <Nav className="ml-auto">
                <Nav.Link href="/login">Instructor Login</Nav.Link>
                <Nav.Link href="/instructor">Bypass</Nav.Link>
                <Nav.Link href="/node_graph">Node Graph</Nav.Link>
            </Nav>
        </Container>
    </Navbar>
);

export default CustomNavbar;