import streamlit.components.v1 as components
import json
import uuid


def my_chart_component(data, chart_type="bar", key=None, height=400):
    # Generate a unique ID for the canvas element
    unique_id = uuid.uuid4().hex
    canvas_id = f"myChart-{unique_id}"

    # Convert the data to JSON format
    data_json = json.dumps(data)

    # JavaScript code to initialize the chart, with dynamic options based on the chart type
    js_code = """
    function createChart(chartData, chartType, canvasId) {
        var options = {
            scales: {
                y: {
                    beginAtZero: true,
                    display: chartType === 'bar' || chartType === 'line', // Display Y-axis for bar and line charts only
                }
            },
            plugins: {
                legend: {
                    display: true, // Adjust legend display as needed
                }
            }
        };

        // Customize options for doughnut chart
        if (chartType === 'doughnut') {
            options = {
                cutout: '60%', // Adjusts the doughnut chart's thickness
                plugins: {
                    legend: {
                        display: true, // Adjust legend display as needed
                    }
                }
            };
        }

        var ctx = document.getElementById(canvasId).getContext('2d');
        var myChart = new Chart(ctx, {
            type: chartType,
            data: chartData,
            options: options
        });
    }
    """

    # HTML to inject into the Streamlit app
    component_html = f"""
    <canvas id='{canvas_id}' width='400' height='{height}'></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        {js_code}
        createChart({data_json}, '{chart_type}', '{canvas_id}');
    </script>
    """
    components.html(
        component_html, height=height + 20
    )  # Adjust height as needed for spacing
