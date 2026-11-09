// Define your backend URL dynamically or use your Render URL directly
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:8000' 
    : 'https://demandsense-exob.onrender.com';

let myChart = null;

async function uploadCSV() {
    const fileInput = document.getElementById('csvFile');
    if (!fileInput || fileInput.files.length === 0) {
        alert("Please select a CSV file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`${API_BASE_URL}/forecast/upload-csv/?periods=30`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate forecast from backend.");
        }

        const result = await response.json();
        renderChart(result.forecast);

    } catch (error) {
        alert("Error: " + error.message);
        console.error(error);
    }
}