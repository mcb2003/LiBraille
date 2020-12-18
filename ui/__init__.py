import wx
import engine

class MainFrame(wx.Frame):
    """ The application's main window """
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, title="Libraille", size=(800, 600))
        self.CreateStatusBar()
        # Create and attach the MenuBar
        self.menu_bar = self.createMenuBar()
        self.SetMenuBar(self.menu_bar)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)

    def createMenuBar(self):
        file = wx.Menu()
        file.Append(wx.ID_OPEN, "&Import", "Import and convert a print document")
        file.AppendSeparator()
        file.Append(wx.ID_EXIT, "E&xit", "Close this program")
        menu = wx.MenuBar()
        menu.Append(file, "&File")
        return menu

class App(wx.App):
    """ Represents the  entire GUI application """
    def OnInit(self):
        # Construct the main window and set it as the app's toplevel
        frame = MainFrame()
        self.SetTopWindow(frame)
        # Return True to indicate success to WXPython
        return True
