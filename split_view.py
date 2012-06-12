import sublime, sublime_plugin


class SplitView(sublime_plugin.TextCommand):
    def split_layout(self, vertical=False):
        window = self.view.window()
        group, index = window.get_view_index(self.view)
        layout = window.get_layout()
        # cell = layout["cells"][index]
        # TODO: more flexible/intelligent splitting
        if vertical:
            layout["cols"] = [0.0, 0.5, 1.0]
            layout["rows"] = [0.0, 1.0]
            layout["cells"] = [[0, 0, 1, 1], [1, 0, 2, 1]]
        else:
            layout["cols"] = [0.0, 1.0]
            layout["rows"] = [0.0, 0.5, 1.0]
            layout["cells"] = [[0, 0, 1, 1], [0, 1, 1, 2]]
        window.set_layout(layout)

    def clone_view(self, group, index):
        orig_view = self.view
        window = self.view.window()
        window.run_command("clone_file")
        new_view = window.active_view()

        window.set_view_index(new_view, group, index)
        window.focus_view(orig_view)
        window.focus_view(new_view)

        def scroll():
            new_view.set_viewport_position(orig_view.viewport_position())
            for region in orig_view.sel():
                new_view.sel().add(region)
        sublime.set_timeout(scroll, 0)

    def run(self, edit, vertical=False):
        self.split_layout(vertical)
        self.clone_view(1, 0)
