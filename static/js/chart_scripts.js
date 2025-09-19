function getBarChart(season, chartData) {
    const canvasId = `histChart_${season}`;
    const ctx = document.getElementById(canvasId);
    const labels = chartData.w.map((num, i) => i + 1)
    const data = {
        labels: labels,
        datasets: [{
            label: "W's",
            data: chartData.w,
            backgroundColor: [
                'rgba(88, 24, 69, 0.8)'
            ],
            borderColor: [
                'rgb(88, 24, 69)'

            ],
            borderDash: [2, 2]

        },
        {
            label: "L's",
            data: chartData.l,
            backgroundColor: 'rgba(211, 211, 211, 0.5)',
            borderColor: [
                'rgba(88, 24, 69, 0.8)'

            ],
            borderWidth: 0.5
        }]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    onClick: null
                }
            },
            scales: {
                x: {
                    stacked: true,
                    ticks: {
                        font: {
                            size: 6
                        }
                    }
                },
                y: {
                    stacked: true,
                    ticks: {
                        font: {
                            size: 8
                        }
                    }
                }
            }
        }
    });
}

function getPercentChart(season, chartData) {
    const canvasId = `percentChart_${season}`;
    const ctx = document.getElementById(canvasId);
    const labels = chartData.w.map((num, i) => i + 1)
    const data = {
        labels: labels,
        datasets: [{
            label: '%',
            data: chartData.percentage,
            backgroundColor: [
                'rgba(211, 211, 211, 0.5)'
            ],
            borderColor: [
                'rgba(88, 24, 69, 0.8)'
            ],
            borderWidth: 0.5
        }]
    };

    document.getElementById(`percentTotal_${season}`).innerText = `(Total: ${chartData.percent.toFixed(2)}%)`;

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    onClick: null
                },
                title: {
                    display: false,
                    text: data.percent, // Use the function to set the title
                    font: {
                        size: 10
                    }
                }
            },
            scales: {
                x: {
                    stacked: false,
                    ticks: {
                        font: {
                            size: 6
                        }
                    }
                },
                y: {
                    stacked: false,
                    ticks: {
                        font: {
                            size: 8
                        }
                    }
                }
            }
        }
    });
}

