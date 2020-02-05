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
      conllu: '',
      width: 483,
      height: 244
    }
  }

   parseReturn(response){
    var str = "";
    console.log(response);
    //this.state.conllu = response.conllu.replace('\t', '&emsp;');
    //this.state.conllu = this.state.conllu.replace('\n', '&NewLine;')
    //this.state.conllu = String.raw`./brattest.html?` + this.state.conllu;
    this.state.conllu = "./brattest.html?" + encodeURI(response.conllu) + "&" + encodeURI(response.conllu_eng);
    console.log(this.state.conllu);
    for(var i = 0; i < response.words.length; i++){
        if(response.words[i].notes.length > 0) { str += response.words[i].text + '\n'; }
        for(var j = 0; j < response.words[i].notes.length; j++){
          str += '\t' + response.words[i].notes[j] + '\n';
        }
    }
    return str;
  }

  submitHappened = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://localhost:5000/check', 
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
          result: this.parseReturn(response),
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
        <h1>Grammatik!</h1>
        <div className="row justify-content-center">
        <form>
            <p>Input</p>
            <textarea type="text" id="inputText" onChange={this.handleChange.bind(this)} name="name" rows="10" cols="50" style={{"borderRadius": "10px"}}/>
        </form>
        <form>
            <p>Grammar result</p>
            <iframe src={this.state.conllu} height={this.state.height} width={this.state.width}/>   
            <textarea type="text" id="readonly" value={this.state.result} spellCheck="true" readOnly name="name" rows="10" cols="70" style={{"border-radius": "10px"}}/> 
        </form>
        </div>
        <div>
          <Button variant="success" onClick={this.submitHappened}>Submit</Button>
        </div>
      </div>
    );
  }
}

export default App;
