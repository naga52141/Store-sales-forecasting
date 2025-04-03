async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        console.error("No file selected.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        console.log("Uploading file...");
        let response = await fetch("http://localhost:4000/upload", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            console.error("Upload failed:", response.statusText);
            return;
        }

        let data = await response.json();
        console.log("Forecast result:", data);

        if (!data || Object.keys(data).length === 0) {
            console.error("No forecast data received.");
            return;
        }

        // ✅ Plot forecast & actual sales
        plotSalesChart(data);
        displayTable(data);

    } catch (error) {
        console.error("Fetch error:", error);
    }
}

// ✅ Function to plot sales chart
function plotSalesChart(data) {
    const ctx = document.getElementById("salesChart").getContext("2d");

    // ✅ Destroy existing chart to prevent lag
    if (window.salesChartInstance) {
        window.salesChartInstance.destroy();
    }

    window.salesChartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: [...data.actual_dates, ...data.dates],
            datasets: [
                {
                    label: "Actual Sales",
                    data: data.actual_sales,
                    borderColor: "blue",
                    backgroundColor: "transparent",
                },
                {
                    label: "Forecasted Sales",
                    data: [...Array(data.actual_sales.length).fill(null), ...data.forecast],
                    borderColor: "red",
                    backgroundColor: "transparent",
                    borderDash: [5, 5],
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: { title: { display: true, text: "Sales" } }
            }
        }
    });
}

// ✅ Function to display forecast & actual sales in table
function displayTable(data) {
    const table = document.getElementById("dataTable");
    table.innerHTML = "<tr><th>Date</th><th>Actual Sales</th><th>Forecast</th></tr>";

    data.dates.forEach((date, index) => {
        let row = table.insertRow();
        row.insertCell(0).innerText = date;
        row.insertCell(1).innerText = data.actual_sales[index] || "-";
        row.insertCell(2).innerText = data.forecast[index];
    });
}
