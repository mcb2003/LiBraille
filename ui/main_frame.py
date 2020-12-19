from os.path import basename

import wx
import engine

def tb_add_tool(tb, id, name, img, description):
    """ Helper method for adding tools to a toolbar, mainly due to the need to use the OS's native icons. """
    tb.AddTool(id, name, wx.ArtProvider.GetBitmap(img), description)

class MainFrame(wx.Frame):
    """ The application's main window """
    def __init__(self, parent = None, doc = None, *args, **kwargs):
        super().__init__(parent, title="Untitled - Libraille", size=(800, 600))
        self._doc = None
        self._file_name = None
        self.modified = False
        self.CreateStatusBar()
        # Create and attach the MenuBar and ToolBar
        self.menu_bar = self.create_menu_bar()
        self.SetMenuBar(self.menu_bar)
        self.tool_bar = self.create_tool_bar()
        self.SetToolBar(self.tool_bar)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.register_events()
        self.Show(True)

    def create_menu_bar(self):
        file = wx.Menu()
        file.Append(wx.ID_NEW, "&New\tCtrl-n", "Create a new braille document")
        file.Append(wx.ID_OPEN, "&Import\tCtrl-o", "Import and convert a print document")
        file.AppendSeparator()
        file.Append(wx.ID_SAVE, "&Save\tCtrl-s", "Save the current braille document")
        file.Append(wx.ID_SAVEAS, "Save &As\tCtrl-Shift-s", "Save the current braille document under a new name")
        file.AppendSeparator()
        file.Append(wx.ID_EXIT, "E&xit\t\tCtrl-q", "Close this program")
        edit = wx.Menu()
        edit.Append(wx.ID_UNDO, "&Undo\tCtrl-z", "Undoes the last operation")
        edit.Append(wx.ID_REDO, "&Redo\tCtrl-y", "Redoes the last operation")
        edit.AppendSeparator()
        edit.Append(wx.ID_CUT, "&Cut\tCtrl-x", "Move text to the clipboard")
        edit.Append(wx.ID_COPY, "Cop&y\tCtrl-c", "Copies text to the clipboard")
        edit.Append(wx.ID_PASTE, "&Paste\tCtrl-v", "Insert text from the clipboard")
        menu = wx.MenuBar()
        menu.Append(file, "&File")
        menu.Append(edit, "&Edit")
        return menu

    def create_tool_bar(self):
        tb = self.CreateToolBar(wx.TB_DEFAULT_STYLE, wx.ID_ANY, "Main")
        tb_add_tool(tb, wx.ID_NEW, "New", wx.ART_NEW, "Create a new braille document")
        tb_add_tool(tb, wx.ID_OPEN, "Import", wx.ART_FILE_OPEN, "Import and convert a print document")
        tb.AddSeparator()
        tb_add_tool(tb, wx.ID_SAVE, "Save", wx.ART_FILE_SAVE, "Save the current braille document")
        tb_add_tool(tb, wx.ID_SAVEAS, "Save As", wx.ART_FILE_SAVE_AS, "Save the current braille document under a new name")
        tb.AddSeparator()
        tb_add_tool(tb, wx.ID_UNDO, "Undo", wx.ART_UNDO, "Undo the last operation")
        tb_add_tool(tb, wx.ID_REDO, "Redo", wx.ART_REDO, "Redo the last operation")
        tb.AddSeparator()
        tb_add_tool(tb, wx.ID_CUT, "Cut", wx.ART_CUT, "Move text to the clipboard")
        tb_add_tool(tb, wx.ID_COPY, "Copy", wx.ART_COPY, "Copy text to the clipboard")
        tb_add_tool(tb, wx.ID_PASTE, "Copy", wx.ART_PASTE, "Insert text from the clipboard")
        tb.Realize()
        return tb

    def register_events(self):
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MENU, self.on_exit, None, wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_open, None, wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_save, None, wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.on_save_as, None, wx.ID_SAVEAS)
        self.Bind(wx.EVT_TEXT, self.on_text_change, self.text)
        self.Bind(wx.EVT_MENU, self.on_undo, None, wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self.on_redo, None, wx.ID_REDO)
        self.Bind(wx.EVT_MENU, self.on_cut, None, wx.ID_CUT)
        self.Bind(wx.EVT_MENU, self.on_copy, None, wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.on_paste, None, wx.ID_PASTE)

    ## EVENT HANDLERS ##
    
    def on_open(self, evt):
        open_dlg = wx.FileDialog(self, "Select a file to convert", style=wx.FD_OPEN)
        if open_dlg.ShowModal() == wx.ID_OK:
            self.SetRepresentedFilename(open_dlg.GetFilename())
            self.file_name = None # This is the name of the braille file, which hasn't been saved yet
            self._doc = engine.Document(open_dlg.GetPath())
            self.text.SetValue(str(self._doc))
            evt.Skip()

    def get_save_path(self):
        """ Ask the user to save and return the path. """
        save_dlg = wx.FileDialog(self, "Save braille document", style=wx.FD_SAVE, wildcard="BRF File (*.brf)|*.brf|BRL File (*.brl)|*.brl")
        if save_dlg.ShowModal() == wx.ID_OK:
            return save_dlg.GetPath()
        else:
            return None

    def on_save(self, evt):
        if self.file_name is None:
            self.file_name = self.get_save_path()
        if self.file_name is not None:
            with open(self.file_name, "w") as f:
                f.write(self.text.GetValue())
            self.modified  = False

    def on_save_as(self, evt):
        file_name = self.get_save_path()
        if file_name is not None:
            self.file_name = file_name
        with open(self.file_name, "w") as f:
            f.write(self.text.GetValue())
            self.modified  = False

    def on_close(self, evt):
        if evt.CanVeto() and self.modified:
            fname = basename(self.file_name) if self.file_name is not None else "Untitled"
            result = wx.MessageBox(f"Want to save your changes to \"{fname}\"?", "Save changes?", wx.CANCEL | wx.NO | wx.YES, self)
            if result == wx.CANCEL:
                evt.Veto()
                return
            elif result == wx.YES:
                self.on_save_as(None)
        evt.Skip()
            
    def on_text_change(self, evt):
        self.modified = True

    def on_exit(self, evt):
        wx.CallAfter(self.Close)

    def on_undo(self, evt):
        self.text.Undo()
        evt.Skip()

    def on_redo(self, evt):
        self.text.Redo()
        evt.Skip()

    def on_cut(self, evt):
        self.text.Cut()
        evt.Skip()

    def on_copy(self, evt):
        self.text.Copy()
        evt.Skip()

    def on_paste(self, evt):
        self.text.Paste()
        evt.Skip()

## PROPERTIES ##

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, val):
        self._file_name = val
        if val is not None:
            self.SetTitle(basename(val)[:val.rfind(".")] + " - Libraille")
        else:
            self.SetTitle("Unsaved - Libraille")
