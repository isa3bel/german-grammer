class TextService {

//    url =
//    'https://wbdv-generic-server.herokuapp.com/api/isabelbolger/users';
   url = "http://causal-shell-266901.appspot.com";
   
    sendTextAreaInput(val) {
        return fetch(this.url, {
            method: 'POST',
            body: JSON.stringify(val),
            headers: {
                "content-type": "application/json",
            },
            mode: "no-cors",
            
        }).then(response => response.json());
        
    }

   
}

export default TextService;