from textual.document._document import Selection
from textual.document._edit import Edit
from textual.document._syntax_aware_document import SyntaxAwareDocument
from textual.widgets import TextArea

from pgtui.messages import RunQuery
from pgtui.sql import find_query, format_sql


class SqlEditor(TextArea):
    BINDINGS = [
        ("ctrl+f", "format", "Format"),
        ("ctrl+p", "execute", "Execute"),
        ("ctrl+s", "select", "Select"),
    ]

    def __init__(self):
        super().__init__(language="sql")

    def action_execute(self):
        assert isinstance(self.document, SyntaxAwareDocument)
        if location := self.find_query():
            start, end = location
            query = self.text[start : end + 1]
            self.post_message(RunQuery(query))

    def action_format(self):
        assert isinstance(self.document, SyntaxAwareDocument)
        if location := self.find_query():
            start, end = location
            query = self.text[start : end + 1]
            formatted = format_sql(query)
            start_location = self.document.get_location_from_index(start)
            end_location = self.document.get_location_from_index(end)
            edit = Edit(formatted, start_location, end_location, maintain_selection_offset=False)
            self.edit(edit)

    def action_format_all(self):
        text = format_sql(self.text)
        last_line = self.document.line_count - 1
        length_of_last_line = len(self.document[last_line])
        start = (0, 0)
        end = (last_line, length_of_last_line)
        edit = Edit(text, start, end, maintain_selection_offset=False)
        self.edit(edit)

    def action_select(self):
        assert isinstance(self.document, SyntaxAwareDocument)
        if location := self.find_query():
            start, end = location
            start_location = self.document.get_location_from_index(start)
            end_location = self.document.get_location_from_index(end)
            self.selection = Selection(start_location, end_location)

    def find_query(self) -> tuple[int, int] | None:
        assert isinstance(self.document, SyntaxAwareDocument)

        # If a selection exists, return that
        if self.selected_text:
            if self.selected_text.strip():
                start = self.document.get_index_from_location(self.selection[0])
                end = self.document.get_index_from_location(self.selection[1])
                return start, end
            else:
                # Empty selection
                return None

        # Do nothing if cursor is on an empty line
        [row, _] = self.cursor_location
        line = self.document.get_line(row)
        if line.strip() == "":
            return None

        index = self.document.get_index_from_location(self.cursor_location)

        # If cursor is positioned just after a query, then move cursor to
        # include that query.
        if self.cursor_at_end_of_line and self.text[index - 1 : index] == ";":
            index -= 1

        start, end = find_query(self.text, index)
        query = self.text[start : end + 1].strip()
        if not query:
            return None

        return start, end
