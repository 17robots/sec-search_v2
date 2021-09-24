import os
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from interface.component import Component


class SearchUI(Component):
    def __init__(self, props):
        self.state = {
            'programInfo': props['programInfo'],
            'messageLog': props['messageLog'],
            'regionTable': props['regionTable']
        }
    
    def render(self):
        program_info = Table.grid()
        program_info.add_column('Program Options')
        for key in self.state['programInfo']:
            program_info.add_row(f"{key}: {self.state['programInfo'][key]}")
        
        region_status = Table.grid()
        region_status.add_column('Region')
        region_status.add_column('Completed')
        for key in self.state['regionTable']:
            region_status.add_row(key, f"{self.state['regionTable'][key]['completed']}/{self.state['regionTable'][key]['total']}")

        output = Table.grid()
        output.add_column('')
        view_height = os.get_terminal_size().lines - 2
        for message in self.state['messageLog'][-view_height:] if len(self.state['messageLog']) > view_height else self.state['messageLog']:
            output.add_row(message)
        
        layout = Layout()
        layout.split_row(
            Layout(name='sidebar'),
            Layout(name='output', ratio=3)
        )

        layout['sidebar'].split_column(
            Layout(name='programInfo'),
            Layout(name='status')
        )

        layout['programInfo'].update(Panel(program_info))
        layout['status'].update(Panel(region_status))
        layout['output'].update(Panel(output))

        return layout
