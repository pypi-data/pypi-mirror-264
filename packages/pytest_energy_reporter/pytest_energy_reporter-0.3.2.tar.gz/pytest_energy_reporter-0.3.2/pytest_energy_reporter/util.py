
def print_table_str(headers=list[str], values=list[list[str]]) -> list[str]:
    '''Print a table with headers and values as strings. Return a list of strings, each representing a row of the table.'''
    # Find the maximum width of the columns
    column_widths = [len(header) for header in headers]
    for row in values:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    # Create the table
    table = []
    # Header rows
    table.append(" | ".join([header.ljust(column_widths[i])
                 for i, header in enumerate(headers)]))
    table.append("-" * (sum(column_widths) + len(headers) * 3 - 1))
    # Rows
    for row in values:
        table.append(" | ".join(
            [str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)]))

    return table
