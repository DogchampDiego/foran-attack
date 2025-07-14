class Table:
    @staticmethod
    def print_table(column, rows):
        print()
        column_widths = [max(len(str(row[i])) for row in rows + [column]) for i in range(len(column))]
        Table.print_row(column, column_widths)
        Table.print_separator(column_widths)
        for row in rows:
            Table.print_row(row, column_widths)

        print()

    @staticmethod
    def print_row(row, column_widths):
        formatted_row = [str(row[i]).ljust(column_widths[i]) for i in range(len(row))]
        print(" | ".join(formatted_row))

    @staticmethod
    def print_separator(column_widths):
        separator_row = ["-" * width for width in column_widths]
        print("-+-".join(separator_row))