document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    console.log("Form submitted!");  // Add this at the beginning of the event listener
    e.preventDefault();

    const fileInput = document.getElementById("imageInput");
    const previewImage = document.getElementById("previewImage");
    const outputImage = document.getElementById("outputImage");
    const resultDiv = document.getElementById("result");
    const problemsDiv = document.getElementById("problems");
    const recommendationsDiv = document.getElementById("recommendations");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    const response = await fetch("/upload/", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();

    // Display results
    // problemsDiv.innerHTML = `<strong>Detected Problems:</strong> ${data.problems.join(", ")}`;
    // recommendationsDiv.innerHTML = `<strong>Recommendations:</strong> ${data.recommendations.flat().join(", ")}`;
    problemsDiv.innerHTML = `<h3>Detected Problems</h3><ul>${data.problems.map(problem => `<li>${problem}</li>`).join("")}</ul>`;
    recommendationsDiv.innerHTML = `<h3>Recommendations</h3><ul>${data.recommendations.flat().map(rec => `<li>${rec}</li>`).join("")}</ul>`;
    // Display annotated image
    previewImage.style.display = "none"; 
    outputImage.src = data.annotated_image_url;
    console.log( data.annotated_image_url)
    outputImage.style.display = "block";

    // Show result section
    resultDiv.classList.remove("hidden");
});

document.getElementById("imageInput").addEventListener("change", (e) => {
    const analyzeButton = document.getElementById("analyzeButton");
    analyzeButton.disabled = !e.target.files.length;
});

document.getElementById("imageInput").addEventListener("change", (e) => {
    const analyzeButton = document.getElementById("analyzeButton");
    analyzeButton.disabled = !e.target.files.length;

    // Update the preview image
    const previewImage = document.getElementById("previewImage");
    if (e.target.files.length) {
        previewImage.src = URL.createObjectURL(e.target.files[0]);  // Set the image source
        previewImage.style.display = "block";  // Make the image visible
    } else {
        previewImage.style.display = "none";  // Hide the image if no file is selected
    }
});