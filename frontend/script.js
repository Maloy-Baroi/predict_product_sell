async function fetchPrediction(productName) {
    const response = await fetch('http://localhost:8000/api/v1/predict-next-sell', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_name: productName })
    });

    console.log(response);

    if (!response.ok) {
        throw new Error('Failed to fetch prediction');
    }

    const data = await response.json();
    return data;
}

function renderChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['June', 'July', 'August'],
            datasets: [{
                label: 'Predicted Sales',
                data: [data.may_sell, data.next_1, data.next_2],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: true
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

const formSubmission = () => {
    let productNameId = document.getElementById('productNameId');
    const productName = productNameId.value; // Replace with actual product name or get it dynamically
    console.log(productName);
    fetchPrediction(productName)
        .then(data => renderChart(data))
        .catch(error => console.error('Error fetching prediction:', error));
}

// document.addEventListener('DOMContentLoaded', () => {
    
// });
