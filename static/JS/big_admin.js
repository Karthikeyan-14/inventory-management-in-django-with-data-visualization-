let charts = {};

function createChart(ctx, type, labels, data, title) {
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: title
            }
        }
    });
}

function updateCharts(data) {
    const categories = ['upcoming', 'ongoing', 'hold', 'closed'];
    const chartData = categories.map(category => 
        data.find(item => item.category === category)?.count || 0
    );

    if (charts.allPie) charts.allPie.destroy();
    charts.allPie = createChart(
        document.getElementById('all-pie-chart').getContext('2d'),
        'pie',
        categories.map(c => c.charAt(0).toUpperCase() + c.slice(1)),
        chartData,
        'All Tasks'
    );

    if (charts.allBar) charts.allBar.destroy();
    charts.allBar = createChart(
        document.getElementById('all-bar-chart').getContext('2d'),
        'bar',
        categories.map(c => c.charAt(0).toUpperCase() + c.slice(1)),
        chartData,
        'All Tasks'
    );

    if (charts.allLine) charts.allLine.destroy();
    charts.allLine = createChart(
        document.getElementById('all-line-chart').getContext('2d'),
        'line',
        categories.map(c => c.charAt(0).toUpperCase() + c.slice(1)),
        chartData,
        'All Tasks'
    );

    categories.forEach(category => {
        const count = data.find(item => item.category === category)?.count || 0;
        if (charts[category + 'Pie']) charts[category + 'Pie'].destroy();
        charts[category + 'Pie'] = createChart(
            document.getElementById(`${category}-pie-chart`).getContext('2d'),
            'pie',
            [category.charAt(0).toUpperCase() + category.slice(1)],
            [count],
            `${category.charAt(0).toUpperCase() + category.slice(1)} Tasks`
        );

        if (charts[category + 'Bar']) charts[category + 'Bar'].destroy();
        charts[category + 'Bar'] = createChart(
            document.getElementById(`${category}-bar-chart`).getContext('2d'),
            'bar',
            [category.charAt(0).toUpperCase() + category.slice(1)],
            [count],
            `${category.charAt(0).toUpperCase() + category.slice(1)} Tasks`
        );

        if (charts[category + 'Line']) charts[category + 'Line'].destroy();
        charts[category + 'Line'] = createChart(
            document.getElementById(`${category}-line-chart`).getContext('2d'),
            'line',
            [category.charAt(0).toUpperCase() + category.slice(1)],
            [count],
            `${category.charAt(0).toUpperCase() + category.slice(1)} Tasks`
        );
    });
}

function fetchData(fromDate, toDate) {
    let url = '/get-task-data/';
    if (fromDate && toDate) {
        url += `?from_date=${fromDate}&to_date=${toDate}`;
    }
    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
        })
        .catch(error => console.error(' Error fetching data:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    fetchData();

    const filterBtn = document.getElementById('filter-btn');
    filterBtn.addEventListener('click', function() {
        const fromDate = document.getElementById('from_date').value;
        const toDate = document.getElementById('to_date').value;
        fetchData(fromDate, toDate);
    });

    
});
document.getElementById('report-btn').addEventListener('click', function() {
    fetch('/generate-report/')
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'task_report.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
});