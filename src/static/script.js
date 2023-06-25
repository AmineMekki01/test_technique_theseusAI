// script.js

// Get the submit button, question input field, file input, and error message element
const submitButton = document.getElementById("submit-button");
const questionInput = document.getElementById("question");
const fileInput = document.getElementById("file-input");
const errorMessage = document.getElementById("error-message");

// Add an event listener to the submit button
submitButton.addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent default form submission behavior

    // Get the user's question
    const question = questionInput.value;

    // Validate the form inputs
    if (!isFormValid()) {
        errorMessage.textContent = "Please enter a question and upload a file.";
        return;
    }

    // Send a POST request to the /get_answer endpoint
    const response = await fetch("/get_answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    // Get the response data
    const data = await response.json();

    // Display the answer
    const answerElement = document.getElementById("answer");
    answerElement.textContent = data.answer;
});

errorMessage.style.textAlign = "center";
errorMessage.style.color = "red";
// Add an event listener to the file input
fileInput.addEventListener("change", async () => {
    // Get the uploaded file
    const file = fileInput.files[0];

    // Validate the file input
    if (!file) {
        errorMessage.textContent = "Please upload a file.";
        return;
    }

    // Create a FormData object and append the file
    const formData = new FormData();
    formData.append("file", file);

    // Send a POST request to the /upload_file endpoint
    const response = await fetch("/upload_file", {
        method: "POST",
        body: formData
    });

    // Get the response data
    const data = await response.json();
    console.log(data); // Optional: Log the response data
});

// Add event listeners for input changes
questionInput.addEventListener("input", validateForm);

// Function to validate the form
function validateForm() {
    const questionValue = questionInput.value;
    const fileValue = fileInput.value;

    // Enable or disable the submit button based on field values
    if (questionValue.trim() !== "" && fileValue !== "") {
        submitButton.disabled = false;
        errorMessage.textContent = ""; // Clear the error message
    } else {
        submitButton.disabled = true;
    }
}

// Function to check if the form is valid
function isFormValid() {
    const questionValue = questionInput.value;
    const fileValue = fileInput.value;

    return questionValue.trim() !== "" && fileValue !== "";
}
