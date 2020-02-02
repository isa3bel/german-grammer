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
import TextService from "./services/TextService";

class App extends React.Component {

  constructor() {
    super();
    //this.service = new TextService();
    this.state = {
      value: '',
      formData: {
        data: "test",
      },
      result: '',
    }
  }

  submitHappened = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://localhost:5000/#home/', 
        {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*',
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
        });
      });
      $('#readonly').val(this.state.result);
  }

  handleChange(event) {
    const value = event.target.value;
    var formData = this.state.formData;
    formData['data'] = value;
    this.setState({
      formData
    });
  }  
    
  

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
            <textarea type="text" id="inputText" onChange={this.handleChange.bind(this)} name="name" rows="10" cols="50" style={{"borderRadius": "10px"}}/>
        </form>
        <form>
            <p>Grammer result</p>
            <textarea type="text" id="readonly" value={this.state.result} spellCheck="true" readOnly name="name" rows="10" cols="50" style={{"border-radius": "10px"}}/>
        </form>
        </div>
        <div>
          <Button variant="success" onClick={this.submitHappened}>Submit</Button>
          <Button variant="outline-primary">View English parts of speech</Button>
          <Button variant="outline-primary">View German parts of speech</Button>
          <Button variant="danger">Check for errors</Button>
        </div>
      </div>
    );
  }
}

export default App;
