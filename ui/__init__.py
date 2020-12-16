import wx

class MainFrame(wx.Frame):
    """ The application's main window """
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, title="Libraille", size=(800, 600))
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)

class App(wx.App):
    """ Represents the  entire GUI application """
    def OnInit(self):
        # Construct the main window and set it as the app's toplevel
        frame = MainFrame()
        self.SetTopWindow(frame)
        # Return True to indicate success to WXPython
        return True

if __name__ == "__main__":
    # Create and start the app and it's event loop
    app = App(False)
    app.MainLoop()
