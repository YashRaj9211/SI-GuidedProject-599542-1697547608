let predic_result =""

function imgUp() {
    // Get the file from the file input
    console.log("Called imgUp")
    var fileInput = document.getElementById('file');
    var file = fileInput.files[0];
  
    // Check if a file was selected
    if (!file) {
      console.log("No file selected!");
      return;
    }
  
    // Create a FormData object and append the file to it
    var formData = new FormData();
    formData.append('image', file); // The 'image' key should match the name in your Flask route
  
    // Perform the fetch request to the Flask server
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData
    })
    .then(response => response.text()) // Assuming the server responds with text (change this if JSON response)
    .then(data => {
       predic_result = data
       output()
    })
    .catch(error => console.error('Error:', error));
  }


  function output(){
    window.location.href = `http://127.0.0.1:5000/predict?output=${predic_result}`
    console.log(predic_result)
  }
  