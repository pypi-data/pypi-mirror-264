
def print_table_str(headers=list[str], values=list[list[str]], max_col_widths: list[int] = []) -> list[str]:
    '''Print a table with headers and values as strings. Return a list of strings, each representing a row of the table.'''
    # Find the maximum width of the columns
    column_widths = [len(header) for header in headers]
    for row in values:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(cell))

    # bound the column widths, if a max width is specified
    for i, col_width in enumerate(max_col_widths):
        column_widths[i] = min(column_widths[i], col_width)

    # Create the table
    table = []
    # Header rows
    table.append(" | ".join([header.ljust(column_widths[i])
                 for i, header in enumerate(headers)]))
    table.append("-" * (sum(column_widths) + len(headers) * 3 - 1))
    # Rows
    for row in values:
        # format cell strings
        row_strings = []
        for i, cell in enumerate(row):
            cell_str = str(cell)
            col_width = column_widths[i]
            if len(cell_str) > col_width:
                cell_str = '...' + cell_str[-(col_width - 3):]
            row_strings.append(cell_str.ljust(col_width))

        table.append(" | ".join(row_strings))

    return table
