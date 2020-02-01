import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Component } from "react";
import {
  Navbar,
  Nav,
  NavItem,
  NavDropdown,
  MenuItem,
  Container,
  Form,
  FormControl,
  Button
} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="#home">Tech Together Boston</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="#home">About Us</Nav.Link>
              <Nav.Link href="#link">Story</Nav.Link>
            </Nav>
            
          </Navbar.Collapse>
        </Navbar>
        <h1>German Grammer Checker</h1>
        <form>
            <textarea type="text" name="name" rows="10" cols="100"/>
        </form>
        <input type="submit" value="Submit"/>
      </div>
    );
  }
}

export default App;
