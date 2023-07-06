import panel as pn

#pn.config.template = 'fast'

debug = True

debug_style = {'border': '2px solid red'}
border_style = {'border': '2px solid red'}

def Button(name, align = ("start"), **params):
    style = debug_style if debug else {}
    return pn.widgets.Button(name=name, button_type='primary', align=align, styles=style, **params)

def Row(*args, **kwargs):
    style = debug_style if debug else {}
    return pn.Row(*args, styles = style, **kwargs)

def Column(*args, **kwargs):
    style = debug_style if debug else {}
    return pn.Column(*args, styles = style, **kwargs)

def Spacer(sizing_mode='stretch_width', **params):
    style = debug_style if debug else {}
    return pn.Spacer(sizing_mode=sizing_mode, styles=style, **params)

def gui1():
    return Column(
        Row( Spacer,Button("Button 1"), Spacer),
        Button("Button 2", align="center")
    )

gui1().servable(title="SAM-GPT", target='main')