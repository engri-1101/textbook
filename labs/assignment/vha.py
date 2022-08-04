"""
Package for visualizing the Hungarian Algorithm to solve the assignment problem
"""
import numpy as np
from copy import deepcopy
from scipy import optimize
from ortools.linear_solver import pywraplp as OR
from bokeh.plotting import figure, show
from bokeh.models import Label, Range1d, CustomJS, Slider
from bokeh.layouts import column, row
from bokeh.core.validation import silence
from bokeh.core.validation.warnings import MISSING_RENDERERS


def min_cost_assignment(matrix):
    """
    Returns a dictionary representing the minimum cost assignment of matrix
    {row index: column index}

    Parameter matrix: a list of lists representing the cost matrix
    Returns: a dictionary of {row index: column index}
    """
    row_ind, col_ind = optimize.linear_sum_assignment(matrix)
    return {i: j for i,j in zip(row_ind, col_ind)}

class Step:
    """
    Used to represent a step of the Hungarian Algorithm for visualization


    Attribute matrix: list of lists representing the step's current matrix
    Attribute description: string describing the step of the algorithm shown
    Attribute row_mod: list of changes to each row as strings
    Attribute col_mod: list of changes to each column as strings
    Attribute cover: tuple of two lists of ints, ([rows to cover], [columns to cover])
    Attribute assignment: none or dictionary, gives the min cost assignment answer
    """
    def __init__(self, matrix, description, row_mod=None, col_mod=None, cover=None, assignment=None):
        self.matrix = [list(i) for i in matrix]
        self.description = description

        if row_mod is None:
            row_mod = ['' for _ in range(len(matrix))]
        self.row_mod = row_mod

        if col_mod is None:
            col_mod = ['' for _ in range(len(matrix.T))]
        self.col_mod = col_mod

        if cover is None:
            # First list is rows, second is columns
            cover = ([],[])
        self.cover = cover

        self.assignment = assignment

    def __str__(self):
        s = '\n' + '\n'.join(str(i) for i in self.matrix) + '\n'
        s += self.description + '\n'
        s += f'Row Modifiers: {self.row_mod}\n'
        s += f'Column Modifiers: {self.col_mod}\n'
        s += f'Rows Covered: {self.cover[0]}\n'
        s += f'Columns Covered: {self.cover[1]}\n'
        s += f'Final Assignment: {self.assignment}\n'
        return s

    def __repr__(self):
        return str(self)

def create_assignment_steps(matrix):
    """
    Given a matrix, returns a list of steps for finding the min cost assignment
    using the Hungarian Algorithm

    Parameter matrix: a list of lists representing the cost matrix
    Returns: a list of steps
    """
    original_matrix = deepcopy(matrix)
    matrix = np.array(matrix)

    step = Step(matrix, 'Our starting matrix.')
    steps = [step]

    # Enforce two dimensional matrix
    assert len(matrix.shape) == 2, 'Matrix must be 2D.'

    # Enforce positive elements
    assert len(matrix) > 0 and len(matrix.T) > 0, 'Matrix must contain at least one element.'

    # Enforce rectangular matrix
    assert all(len(matrix[i]) == len(matrix[0]) for i in range(len(matrix))), 'Matrix must be rectangular'

    computing = True
    while computing:
        # Remove from each row
        row_mod = []
        for row in matrix:
            m = np.amin(row)
            row_mod.append(f'-{m}')
            for i in range(len(row)):
                row[i] -= m

        step = Step(matrix, 'Subtract from each row.', row_mod=row_mod)
        if any(mod!='-0' for mod in row_mod):
            steps.append(step)

        # Remove from each column
        col_mod = []
        for column in matrix.T:
            m = np.amin(column)
            col_mod.append(f'-{m}')
            for i in range(len(column)):
                column[i] -= m

        step = Step(matrix, 'Subtract from each column.', col_mod=col_mod)
        if any(mod!='-0' for mod in col_mod):
            steps.append(step)

        # Check for zero assignment
        d = find_zero_assignment(matrix, original_matrix)
        if len(d) > 0:
            step = Step(matrix, 'Final matrix found.', assignment=d)
            steps.append(step)
            computing = False
        else:
            # Find zero cover
            rows, columns = find_zero_cover(matrix)
            step = Step(matrix, 'Find a zero cover.', cover=(rows, columns))
            steps.append(step)
            m = float('inf')
            for i in range(len(matrix)):
                for j in range(len(matrix.T)):
                    if i not in rows and j not in columns:
                        m = min(m, matrix[i,j])
            for i, row in enumerate(matrix):
                if i in rows:
                    continue
                for k in range(len(row)):
                    row[k] -= m
            for i, column in enumerate(matrix.T):
                if i not in columns:
                    continue
                for k in range(len(column)):
                    column[k] += m

            row_mod = ['-0'] * len(matrix)
            for i in range(len(matrix)):
                if i not in rows:
                    row_mod[i] = f'-{m}'
            col_mod = ['+0'] * len(matrix.T)
            for i in columns:
                col_mod[i] = f'+{m}'

            step = Step(matrix, f'Adjust the matrix by delta ({m})', row_mod=row_mod, col_mod=col_mod, cover=(rows,columns))
            steps.append(step)

    return steps


def find_zero_assignment(matrix, cost_matrix=None):
    """
    Given a cost matrix, returns a zero cost assignment if there is one or an empty
    dictionary if there isn't one

    Parameter matrix: an iterable of lists representing the cost matrix
    Returns: a dictionary of {row index: column index} representing the zero-cost
    assignment or an empty dictionary if no zero-cost assignment exists
    """
    matrix = np.array(matrix)
    if cost_matrix is None:
        cost_matrix = matrix

    m = create_za_model(matrix, cost_matrix)

    status = m.Solve()

    if status == OR.Solver.OPTIMAL:
        pairs = [tuple(var.name().split(',')) for var in m.variables() if not var.solution_value() < 0.99]
        return {int(pair[0]): int(pair[1]) for pair in pairs}
    elif status == OR.Solver.INFEASIBLE:
        return {}


def create_za_model(matrix, cost_matrix):
    """
    Given a cost matrix, creates an pywraplp model to find a zero-cost assignment

    Parameter matrix: an numpy array of lists representing the cost matrix
    Returns: a pywraplp model to find a zero-cost assignment of matrix
    """
    m = OR.Solver('zero_assignment', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    vars = {}

    for i in range(len(matrix)):
        for j in range(len(matrix.T)):
            if matrix[i,j] == 0:
                vars[i,j] = m.IntVar(0, 1, f'{i},{j}')

    m.Minimize(sum(vars[i,j] * cost_matrix[i][j] for i,j in vars))

    # No person can be assigned to more than one task
    for i in range(len(matrix)):
        m.Add(sum(vars[k,j] for k,j in vars if k == i) <= 1)

    # No task can have more than one person
    for i in range(len(matrix.T)):
        m.Add(sum(vars[k,j] for k,j in vars if j == i) <= 1)

    # The number of pairs is the minimum between the number of people and tasks
    total = min(len(matrix),len(matrix.T))
    m.Add(sum(vars[i,j] for i,j in vars) == total)

    return m


def find_zero_cover(matrix):
    """
    Given a cost matrix, returns the minimum zero cover of the matrix

    Parameter matrix: an iterable of lists representing the cost matrix
    Returns: a tuple of two lists of ints representing the zero cover ([row indices],[column indices])
    """
    matrix = np.array(matrix)

    m = create_zc_model(matrix)

    status = m.Solve()

    if status == OR.Solver.OPTIMAL:
        r = []
        c = []
        for var in m.variables():
            if var.solution_value() < 0.99:
                continue
            if var.name()[0] == 'r':
                r.append(int(var.name()[1:]))
            else:
                c.append(int(var.name()[1:]))
        return (r, c)
    else:
        assert False, 'No zero cover found.'

def create_zc_model(matrix):
    """
    Given a cost matrix, returns an pywraplp model to find the matrix's minimum zero cover

    Parameter matrix: a numpy array of lists representing the cost matrix
    Returns: a pywraplp model to find the minimum zero cover
    """
    m = OR.Solver('zero_cover', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    rows = {}
    columns = {}

    for i in range(len(matrix)):
        rows[i] = m.IntVar(0, 1, f'r{i}')

    for i in range(len(matrix.T)):
        columns[i] = m.IntVar(0, 1, f'c{i}')

    # Finds minimum zero cover
    m.Minimize(sum(j for i,j in list(rows.items()) + list(columns.items())))

    # Make sure all zeros are covered
    for i in range(len(matrix)):
        for j in range(len(matrix.T)):
            if matrix[i,j] == 0:
                m.Add(rows[i] + columns[j] >= 1)

    return m


def find_min_cost_assignment(matrix):
    """
    Given a cost matrix, finds the minimum cost assignment as a dictionary

    Parameter matrix: an iterable of lists representing the cost matrix
    Returns: a dictionary of minimum cost assignments in {row index: column index}
    """
    matrix = np.array(matrix)

    m = create_min_cost_model(matrix)

    status = m.Solve()

    pairs = [tuple(var.name().split(',')) for var in m.variables() if not var.solution_value() < 0.99]
    return {int(pair[0]): int(pair[1]) for pair in pairs}


def create_min_cost_model(matrix):
    """
    Given a cost matrix, returns a pywraplp model to find the minimum cost assignment

    Parameter matrix: a numpy array of lists representing the cost matrix
    Returns: a pywraplp model to find the minimum cost assignment
    """
    m = OR.Solver('min_cost', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    vars = {}

    for i in range(len(matrix)):
        for j in range(len(matrix.T)):
            vars[i,j] = m.IntVar(0, 1, f'{i},{j}')

    m.Minimize(sum(vars[i,j] * matrix[i,j] for i,j in vars))

    # No task can be assigned to more than one assignment
    for i in range(len(matrix)):
        m.Add(sum(vars[k,j] for k,j in vars if k == i) <= 1)

    # No assignment can have more than one task
    for i in range(len(matrix.T)):
        m.Add(sum(vars[k,j] for k,j in vars if j == i) <= 1)

    # The number of pairs is the minimum between the number of tasks and assignments
    m.Add(sum(vars[i,j] for i,j in vars) == min(len(matrix), len(matrix.T)))

    return m


def visualize_assignment(matrix):
    """
    Given a cost matrix, returns a bokeh figure visualizing the Hungarian
    Algorithm to find a minimum cost assignment

    The use of the slider to choose between figures comes from Stack Overflow:
    https://stackoverflow.com/questions/52415577/bokeh-widget-to-show-hide-figures

    Parameter matrix: a list of lists representing the cost matrix
    Returns: a bokeh figure to visualize the Hungarian Algorithm
    """
    steps = create_assignment_steps(matrix)

    # Controls the width of the window
    width = 350
    # Controls the height of the window
    height = 350
    # Controls the horizontal padding
    x_offset = 25
    # Controls the vertical padding
    y_offset = 25

    # Adds extra padding to the bottom to fit the description
    bottom_padding = 50

    # Calculate the position of a label given the matrix and its row (i) and column (j)
    def calc_pos(i, j, matrix):
        safe_width = width - 2 * x_offset
        safe_height = height - 2 * y_offset

        x = x_offset + (j / (len(matrix[0]))) * safe_width
        y = y_offset + (i / (len(matrix))) * safe_height

        if i == len(matrix):
            y = (height + calc_pos(i-1,j,matrix)[1] + x_offset) / 2
        if j == len(matrix[0]):
            x = (width + calc_pos(i,j-1,matrix)[0] + y_offset) / 2

        return x,y

    # Calculates the font size for the labels
    def calc_size(matrix):
        threesize = 30
        sevensize = 20
        size = min(len(matrix), len(matrix[0]))

        x = (3, 7)
        y = (threesize, sevensize)
        return f'{int(((y[1] - y[0])/(x[1] - x[0])) * (size - x[0]) + y[0])}px'

    # Takes a step, and returns a figure representing it
    def plot_step(step):
        p = figure(width = width, height = height)
        if step is None:
            p.toolbar.logo = None
            p.toolbar_location = None
            return p
        p.x_range = Range1d(0,width)
        p.y_range = Range1d(height+bottom_padding,0)
        p.axis.visible = False
        p.grid.visible = False

        font_size = calc_size(matrix)

        p.quad(color = '#ADE8F4', left=0, top=0, bottom=height+bottom_padding, right=width)
        p.quad(color='#00B4D8', left=0,top=0,bottom=y_offset+calc_pos(len(matrix)-1, 0, matrix)[1], right=x_offset+calc_pos(0,len(matrix[0])-1,matrix)[0])

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                num = str(step.matrix[i][j])
                if step.assignment is not None and i in step.assignment and step.assignment[i] == j:
                    num = '*' + num
                pos = calc_pos(i, j, matrix)
                label = Label(x=pos[0], y=pos[1], text=num, render_mode='css', background_fill_alpha=0.0,
                            text_align = 'center', text_baseline = 'middle', text_font_size = font_size)
                p.add_layout(label)

        for i, text in enumerate(step.row_mod):
            pos = calc_pos(i, len(matrix[0]), matrix)
            label = Label(x=pos[0], y=pos[1], text=text, render_mode='css', background_fill_alpha=0.0,
                        text_align = 'center', text_baseline = 'middle', text_color = 'red', text_font_size = font_size)
            p.add_layout(label)

        for i, text in enumerate(step.col_mod):
            pos = calc_pos(len(matrix), i, matrix)
            label = Label(x=pos[0], y=pos[1], text=text, render_mode='css', background_fill_alpha=0.0,
                        text_align = 'center', text_baseline = 'middle', text_color = 'red', text_font_size = font_size)
            p.add_layout(label)

        for row in step.cover[0]:
            # Find coords for first and last labels in the row
            pos1 = calc_pos(row, 0, matrix)
            pos2 = calc_pos(row, len(matrix[0])-1, matrix)
            x = [pos1[0], pos2[0]]
            y = [pos1[1], pos2[1]]
            p.line(x, y, line_width=2)

        for col in step.cover[1]:
            pos1 = calc_pos(0, col, matrix)
            pos2 = calc_pos(len(matrix)-1, col, matrix)
            x = [pos1[0], pos2[0]]
            y = [pos1[1], pos2[1]]
            p.line(x, y, line_width=2)

        label = Label(x=width/2,y=height+bottom_padding-y_offset,text=step.description, render_mode='css', background_fill_alpha=0.0, text_align='center', text_font_size='20px')
        p.add_layout(label)

        return p

    # Create all the figures
    plots = []
    # Allows us to create empty plots
    silence(MISSING_RENDERERS, True)
    for i in range(len(steps)):
        current_plot = plot_step(steps[i])
        plots.append(row(current_plot,plot_step(None)))
        if i+1 < len(steps):
            next_plot = plot_step(steps[i+1])
            plots.append(row(current_plot,next_plot))
    col = column(plots[0])

    # Create a slider to show plots used the Stack Overflow post below
    # https://stackoverflow.com/questions/52415577/bokeh-widget-to-show-hide-figures
    slider = Slider(bar_color='#00B4D8', title='Step', start=1, end=(len(plots)-1)/2+1, value=1, step=0.5)
    callback = CustomJS(args=dict(plots=plots,col=col,slider=slider), code="""
    const children = [plots[Math.round((slider.value-1)*2)]]
    col.children = children
    """)
    slider.js_on_change('value', callback)

    return column(slider,col)
