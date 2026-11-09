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
        const response = await fetch("http://127.0.0.1:8000/forecast/upload-csv/?periods=30", {
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

function renderChart(forecastData) {
    // Mapped to match your backend's exact response keys: date, predicted_units, lower_bound, upper_bound
    const labels = forecastData.map(item => item.date);
    const yhat = forecastData.map(item => item.predicted_units);
    const yhatLower = forecastData.map(item => item.lower_bound);
    const yhatUpper = forecastData.map(item => item.upper_bound);

    const ctx = document.getElementById('forecastChart').getContext('2d');

    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Predicted Demand',
                    data: yhat,
                    borderColor: 'rgb(37, 99, 235)',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Upper Bound',
                    data: yhatUpper,
                    borderColor: 'rgba(156, 163, 175, 0.5)',
                    borderDash: [5, 5],
                    fill: false
                },
                {
                    label: 'Lower Bound',
                    data: yhatLower,
                    borderColor: 'rgba(156, 163, 175, 0.5)',
                    borderDash: [5, 5],
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}