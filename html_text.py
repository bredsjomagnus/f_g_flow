HTML_TEXT_1 = """
<html >
<body >
<h3>FLÖDESDIAGRAM</h3>
<script type = "text/javascript" src = "https://www.gstatic.com/charts/loader.js" > </script >

<div id = "sankey_multiple" style = "width: 900px;" > </div >
<div style="width: 100%;">
"""

HTML_TEXT_2 = """

</div>
<script type = "text/javascript" >
google.charts.load("current", {packages: ["sankey"]})
google.charts.setOnLoadCallback(drawChart)
function drawChart() {
    var data = new google.visualization.DataTable()
    data.addColumn('string', 'From')
    data.addColumn('string', 'To')
    data.addColumn('number', 'Weight')
    data.addRows(["""
       
HTML_TEXT_3 = """    ])

    var red = '#e81717'
    var green = '#26dc21'
    var blue = '#1722c2'

    var colors = [blue, green,  red, green, red, green, red]
    // Set chart options
    var options = {
        width: 1000,
        height: 500,
        sankey: {
                node: {
                    colors: colors
                },
               link: {
                    colorMode: 'gradient',
                    colors: colors
                }

        }
    }

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.Sankey(document.getElementById('sankey_multiple'))
    chart.draw(data, options)
}
</script >
</body >

</html >"""
