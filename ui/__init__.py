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
        menu = wx.MenuBar()
        menu.Append(file, "&File")
        return menu

    def create_tool_bar(self):
        tb = self.CreateToolBar(wx.TB_DEFAULT_STYLE, wx.ID_ANY, "Main")
        tb_add_tool(tb, wx.ID_NEW, "New", wx.ART_NEW, "Create a new braille document")
        tb_add_tool(tb, wx.ID_OPEN, "Import", wx.ART_FILE_OPEN, "Import and convert a print document")
        tb.AddSeparator()
        tb_add_tool(tb, wx.ID_SAVE, "Save", wx.ART_FILE_SAVE, "Save the current braille document")
        tb_add_tool(tb, wx.ID_SAVEAS, "Save As", wx.ART_FILE_SAVE_AS, "Save the current braille document under a new name")
        tb.Realize()
        return tb

    def register_events(self):
        self.Bind(wx.EVT_MENU, self.on_open, None, wx.ID_OPEN)

    ## EVENT HANDLERS ##
    
    def on_open(self, evt):
        open_dlg = wx.FileDialog(self, "Select a file to convert", style=wx.FD_OPEN)
        if open_dlg.ShowModal() == wx.ID_OK:
            self.SetRepresentedFilename(open_dlg.GetFilename())
            self.file_name = None # This is the name of the braille file, which hasn't been saved yet
            self._doc = engine.Document(open_dlg.GetPath())
            self.text.SetValue(str(self._doc))
            evt.Skip()
            
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

class App(wx.App):
    """ Represents the  entire GUI application """
    def OnInit(self):
        """ Called by WXPython itself, hence the interCapitalisation. """
        # Set some app metadata
        self.SetAppName("libraille")
        self.SetAppDisplayName("Libraille")
        self.SetVendorName("blindcomputing.org")
        self.SetVendorDisplayName("Blind Computing")
        # Construct the main window and set it as the app's toplevel
        frame = MainFrame()
        self.SetTopWindow(frame)
        # Return True to indicate success to WXPython
        return True
