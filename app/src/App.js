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
import $ from 'jquery';
import Tree from "./images/tree.png";

class App extends React.Component {

  render() {
    return (
      <div className="App">
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="#home"><img src={Tree} width="70"
          height="70"/></Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="#home">About Us</Nav.Link>
              <Nav.Link href="#link">Story</Nav.Link>
            </Nav>
            
          </Navbar.Collapse>
        </Navbar>
        <h1>German Grammer Checker</h1>
        <div className="row justify-content-center">
        <form>
            <p>Input</p>
            <textarea type="text" id="inputText" name="name" rows="10" cols="50" style={{"border-radius": "10px"}}/>
        </form>
        <form>
            <p>Grammer result</p>
            <textarea type="text" id="readonly" spellcheck="true" readOnly name="name" rows="10" cols="50" style={{"border-radius": "10px"}}/>
        </form>
        </div>
        <input type="submit" value="Submit"/>
      </div>
    );
  }
}

export default App;
