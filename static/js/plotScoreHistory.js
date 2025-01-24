let currentChart = null;   // for tracking the current chart instance

export function plotScoreHistory(ctx, historyData, predictionDate) {

    const labels = [];
    const dataPoints = [];

    // Parse predictionDate
    const endDate = new Date(predictionDate);
    const startDate = new Date(endDate.getTime() - 24 * 60 * 60 * 1000);

    // Populate labels and dataPoints from historyData
    historyData.forEach(entry => {
        const dataDate = new Date(entry.dateTime);

        // Include only data within the 24-hour range
        if (dataDate >= startDate && dataDate <= endDate) {
            // labels.push(dataDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }));
            labels.push(dataDate.toISOString()); // Use ISO strings for compatibility with time scale
            dataPoints.push(entry.value);
        }
    });

    // Destroy the existing chart if it exists
    if (currentChart) {
        currentChart.destroy();
    }

    // Create the chart
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Septic Shock Risk',
                data: dataPoints,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                pointRadius: 4
            }]
        },
        options: {
            // Note: A warning "Ignoring resolver passed as options for scale: x/y" is generated.
            // I am ignoring the warning.
            // This warning does not impact functionality, as all parameters are honored.
            // The issue may be related to internal resolver handling in Chart.js (version 4.4.7).
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        displayFormats: {
                            hour: 'h:mm a' // Format the time as "1:00 PM"
                        }
                    },
                    ticks: {
                        callback: function (value, index, values) {
                            const date = new Date(value);
                            const hour = date.getHours();
                            const minutes = date.getMinutes();
            
                            // Format the time as HH:MM AM/PM
                            let timeLabel = `${hour === 0 ? 12 : hour > 12 ? hour - 12 : hour}:00 ${hour >= 12 ? 'PM' : 'AM'}`;
            
                            // Add a date boundary if the time is midnight (00:00)
                            // Currently dissabled by 1 == 2
                            if (hour === 0 && minutes === 0 && 1 == 2) {
                                const month = date.toLocaleString('en-US', { month: 'short' }).toUpperCase(); // JAN, FEB, etc.
                                const day = String(date.getDate()).padStart(2, '0'); // Ensure 2-digit day
                                timeLabel += ` (${month}-${day})`;  // This is appending, can just set to = instead of +=
                                // timeLabel = ` ${month}-${day}`;
                            }
            
                            // Show the label only if the hour is divisible by 2 (or 4)
                            if (hour % 4 === 0) { // Adjust for 4-hour intervals: if (hour % 4 === 0)
                                return timeLabel;
                            }
            
                            // Skip labels for other hours
                            return '';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    min: 0,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Risk'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false,
                    position: 'top'
                }
            }
        }
    });

    // Return the chart object
    return currentChart;
}
