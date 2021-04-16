import panel as pn

ECHART = {
        "xAxis": {
            "type": 'category',
            "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [{
            "data": [820, 932, 901, 934, 1290, 1330, 1320],
            "type": 'line'
        }]
    }

def test_echart():
    echart = ECHART
    pane = pn.pane.ECharts(echart, width=500, height=500)
    assert pane.object == echart

def manualtest_echart():
    echart = ECHART
    pane = pn.pane.ECharts(echart, width=500, height=500)
    assert pane.object == echart
    return pane

@pytest.mark.parametrize("event_config", 
    [
        {'click': 'series.tree'},
        {'click': None},
        {'click': {'name': 'Child Clickable'}},
        {'click': {'query': 'series.tree', 'base_url': 'https://www.TEST.de/AssetDetail.aspx?AssetId=',
            'identifier': 'id'}},
        {'click': {'query': 'series.tree', 'handler': 'e => console.log("I got an event:", e)'}},
        {'cluck': 'series.tree'}
    ], ids=[
        "echart_event_simple_query",
        "echart_event_no_query",
        "echart_event_complex_query",
        "echart_event_browser_tab",
        "echart_event_custom_handler",
        "echart_event_wrong_event"
    ]
)
def test_echart_event(event_config):
    echart = ECHART
    pane = pn.pane.ECharts(echart, event_config=event_config, width=500, height=500)
    assert pane.object == echart
    
    @pn.depends(event=echart.param.event, watch=True)
    def update_info(event):
        print(event)

def get_pyechart():
    from pyecharts import options as opts
    from pyecharts.charts import Bar

    bar = (
        Bar()
        .add_xaxis(["A", "B", "C", "D", "E", "F", "G"])
        .add_yaxis("Series1", [114, 55, 27, 101, 125, 27, 105])
        .add_yaxis("Series2", [57, 134, 137, 129, 145, 60, 49])
        .set_global_opts(title_opts=opts.TitleOpts(title="PyeCharts"))
    )
    pane = pn.pane.ECharts(bar, width=500, height=500)
    assert pane.object == bar
    return pane

def get_pyechart2():
    from pyecharts.charts import Bar

    import panel as pn

    bar1 = pn.widgets.IntSlider(start=1, end=100, value=50)
    bar2 = pn.widgets.IntSlider(start=1, end=100, value=50)

    @pn.depends(bar1.param.value, bar2.param.value)
    def plot(bar1, bar2):
        my_plot= (Bar()
            .add_xaxis(['Bar1', 'Bar2'])
            .add_yaxis('Values', [bar1, bar2])
        )
        return pn.pane.ECharts(my_plot, width=500, height=250)
    return pn.Row(pn.Column(bar1, bar2), plot)

if pn.state.served:
    # manualtest_echart().servable()
    get_pyechart2().servable()
if __name__.startswith("__main__"):
    manualtest_echart().show(port=5007)
    get_pyechart().show(port=5007)
