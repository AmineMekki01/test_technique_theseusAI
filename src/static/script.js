// script.js

// Get the submit button, question input field, file input, and error message element
const submitButton = document.getElementById("submit-button");
const questionInput = document.getElementById("question");
const fileInput = document.getElementById("file-input");
const errorMessage = document.getElementById("error-message");

let question = ''; // A variable to store the question

// Add an event listener to the submit button
submitButton.addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent default form submission behavior

    // Validate the form inputs
    if (!isFormValid()) {
        errorMessage.textContent = "Please enter a question and upload a file.";
        return;
    }

    // If a file has already been uploaded, send the question
    if (fileInput.value !== '') {
        await sendQuestion();
    }
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

    // If a question has already been entered, send it
    if (question !== '') {
        await sendQuestion();
    }
});

// Add an event listener for the question input field
questionInput.addEventListener("input", () => {
    question = questionInput.value;
    validateForm();
});

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

// Function to send a question
async function sendQuestion() {
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
}
