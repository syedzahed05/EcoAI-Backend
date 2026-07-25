/* ==========================================================
   EcoAI Dashboard
   Professional JavaScript
========================================================== */

/* ================= DASHBOARD DATA ================= */

const chartData = window.chartData;

const labels = chartData.labels;
const energy = chartData.energy;

const trendLabels = chartData.trendLabels;
const trendEnergy = chartData.trendEnergy;

/* ================= ECOAI COLOR PALETTE ================= */

const colors = [
    "#2E7D32",
    "#43A047",
    "#66BB6A",
    "#81C784",
    "#A5D6A7",
    "#1E88E5",
    "#26A69A",
    "#F9A825",
    "#EF6C00",
    "#8E24AA"
];

/* ================= COMMON OPTIONS ================= */

const commonOptions = {

    responsive: true,

    maintainAspectRatio: false,

    animation: {

        duration: 1800,

        easing: "easeOutQuart"

    },

    plugins: {

        tooltip: {

            backgroundColor: "#1b5e20",

            titleColor: "#ffffff",

            bodyColor: "#ffffff",

            padding: 12,

            cornerRadius: 8

        }

    }

};

/* ==========================================================
   BAR CHART
========================================================== */

const energyCanvas = document.getElementById("energyChart");

if (energyCanvas) {

    new Chart(energyCanvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Energy Consumption (kWh)",

                data: energy,

                backgroundColor: colors,

                borderRadius: 10,

                borderSkipped: false

            }]

        },

        options: {

            ...commonOptions,

            plugins: {

                ...commonOptions.plugins,

                legend: {

                    display: false

                },

                title: {

                    display: true,

                    text: "Room-wise Energy Consumption",

                    font: {

                        size: 18,

                        weight: "bold"

                    }

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        stepSize: 1

                    }

                }

            }

        }

    });

}
/* ==========================================================
   DOUGHNUT CHART
========================================================== */

const pieCanvas = document.getElementById("pieChart");

if (pieCanvas) {

    new Chart(pieCanvas, {

        type: "doughnut",

        data: {

            labels: labels,

            datasets: [{

                data: energy,

                backgroundColor: colors,

                borderColor: "#ffffff",

                borderWidth: 3,

                hoverOffset: 15

            }]

        },

        options: {

            ...commonOptions,

            cutout: "60%",

            plugins: {

                ...commonOptions.plugins,

                legend: {

                    position: "bottom",

                    labels: {

                        padding: 20,

                        font: {

                            size: 13

                        }

                    }

                },

                title: {

                    display: true,

                    text: "Energy Distribution",

                    font: {

                        size: 18,

                        weight: "bold"

                    }

                }

            }

        }

    });

}

/* ==========================================================
   TREND LINE CHART
========================================================== */

const trendCanvas = document.getElementById("trendChart");

if (trendCanvas) {

    new Chart(trendCanvas, {

        type: "line",

        data: {

            labels: trendLabels,

            datasets: [{

                label: "Energy Usage Trend (kWh)",

                data: trendEnergy,

                borderColor: "#2E7D32",

                backgroundColor: "rgba(46,125,50,0.15)",

                fill: true,

                tension: 0.4,

                pointRadius: 5,

                pointHoverRadius: 8,

                pointBackgroundColor: "#2E7D32",

                pointBorderColor: "#ffffff",

                pointBorderWidth: 2

            }]

        },

        options: {

            ...commonOptions,

            plugins: {

                ...commonOptions.plugins,

                legend: {

                    position: "top"

                },

                title: {

                    display: true,

                    text: "Energy Consumption Trend",

                    font: {

                        size: 18,

                        weight: "bold"

                    }

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        stepSize: 1

                    }

                }

            }

        }

    });

}

/* ==========================================================
   DASHBOARD INITIALIZATION
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    console.log("🌱 EcoAI Dashboard Loaded Successfully");

});

/* ==========================================================
   FUTURE FEATURES
========================================================== */

/*
Future Enhancements:

✓ Live Energy Monitoring
✓ Real-Time Sensor Data
✓ AI Prediction Graph
✓ Dark Mode
✓ Notifications
✓ PDF Report Generation
✓ Monthly Analytics
✓ Energy Efficiency Comparison
✓ IoT Device Integration

*/

/* ==========================================================
   END OF FILE
========================================================== */