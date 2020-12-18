import wx
import engine

class MainFrame(wx.Frame):
    """ The application's main window """
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, title="Libraille", size=(800, 600))
        self.CreateStatusBar()
        # Create and attach the MenuBar
        self.menu_bar = self.create_menu_bar()
        self.SetMenuBar(self.menu_bar)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
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

class App(wx.App):
    """ Represents the  entire GUI application """
    def OnInit(self):
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
