import panel as pn

project_list = []

def create_ListBox(names):
    items = []
    for name in names:
        item = create_ListBoxItem(text=name)
        items.append(item)
    return pn.Column(*items)

def create_ListBoxItem(text):
    open_button = pn.widgets.Button(name="OPEN", width=70, height=30)
    label = pn.widgets.StaticText(value=text, align="center")
    return pn.Row(label, open_button)

def start_screen():
    column = pn.Column()
    lb = create_ListBox(project_list)
    box = pn.Row(lb, align="center")
    new_project_button = pn.widgets.Button(name ='New Project', width = 300, )
    new_project_button.on_click(new_project(column, lb))
    column.extend(objects= [new_project_button, box])
    return column

def new_project(column: pn.Column, lb):
    modal = None
    def on_click(event):
        nonlocal modal
        if has(column, modal):
            column.remove(modal)
        modal = create_modal(column, lb)
        column.append(modal)
    return on_click

def has(panel, widget: pn.Column):
    for child in panel:
        if child is widget:
            return True

def create_modal(column, lb):
    config = {
        "headerControls": {
            "close": "remove"
        },
        "position": "center"
    }
    project_name = pn.widgets.TextInput(name='Project Name')
    modal = pn.layout.FloatPanel(project_name, name='New Project',
        width=400,
        height=None,
        sizing_mode='stretch_height',
        contained = False,
        config=config)
    ok_button = pn.widgets.Button(name='OK', button_type='primary')
    ok_button.on_click(add_project(project_name, column, modal, lb))
    modal.append(ok_button)
    return modal

def add_project(name, column, modal, listBox):
    def on_click(event):
        list_item = create_ListBoxItem(name)
        listBox.append(list_item)
        column.remove(modal)
    return on_click