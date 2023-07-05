import panel as pn

project_list = []

def start_screen():
    """
    Creates the start screen layout.    
    Functionality:
    - Creates a button to add a new project.
    - Creates a list box to display existing projects.
    - Adds the new project button and list box to the main column.
    - Returns the column layout.
    """
    column = pn.Column(width = 300, align='center')

    lb = create_ListBox(project_list)
    box = pn.WidgetBox(lb, horizontal=True, align='center')

    new_project_button = pn.widgets.Button(name ='New Project', width = 300, align='center')
    new_project_button.on_click(new_project(column, lb))

    column.extend(objects= [new_project_button, box])
    return column

def create_ListBox(names):
    """
    Creates a list box with items for each name.
    
    Parameters:
    names (list): The list of names to display as list box items.
    
    Functionality: 
    - Loops through each name in the names list.
    - Creates a list box item for each name using create_ListBoxItem().
    - Adds each item to the items list.
    - Returns a column layout containing all the list box items.
    """
    items = []
    for name in names:
        item = create_ListBoxItem(text=name)
        items.append(item)
    return pn.Column(*items, align='center')

def create_ListBoxItem(text):
    """
    Creates a list box item with a label and open button.
    
    Parameters:
    text (str): The text to display in the label.
    
    Functionality:
    - Creates a button with the text "OPEN".
    - Creates a static text label with the provided text, aligned center.
    - Returns a row layout containing the label and open button.
    """
    open_button = pn.Column(pn.widgets.Button(name="OPEN", width=70, height=30, align=("end", "center")))
    label = pn.Column(pn.widgets.StaticText(value=text), align = ("center"), height = 30, margin = (0, 30, 0, 0))
    return pn.Row(label, open_button,  width = 300, align='start', styles={'background': 'lightgrey', 'align': 'end'})

def new_project(column: pn.Column, lb):
    """
    Creates a new project modal.
    
    Parameters:
    column (pn.Column): The main column layout.
    lb (pn.Column): The list box containing project names.
    
    Functionality:
    - Checks if the modal already exists in the column. If so, removes it.
    - Creates a new modal to enter the project name using create_modal().
    - Appends the new modal to the column.
    - Returns a callback function to show the modal.
    """
    modal = None
    def on_click(event):
        nonlocal modal
        if has(column, modal):
            column.remove(modal)
        modal = create_modal(column, lb)
        column.append(modal)
    return on_click

def has(main_column: pn.Column, modal: pn.Column) -> bool:
    """Checks if a modal exists in the main column."""
    try: 
        main_column.objects.index(modal)
        return True
    except ValueError:
        #logger.warning(f'{modal} not found in {main_column}.')
        return False

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
    ok_button = pn.widgets.Button(name='OK', button_type='primary', align = "center")
    ok_button.on_click(add_project(project_name, column, modal, lb))
    modal.append(ok_button)
    return modal

def add_project(name, column, modal, listBox):
    def on_click(event):
        list_item = create_ListBoxItem(name)
        listBox.append(list_item)
        column.remove(modal)
    return on_click