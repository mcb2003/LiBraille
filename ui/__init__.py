""" Contains all code to create and manage the graphical user interface (GUI), and allow it to interface with the
backend engine. """

import wx

from .main_frame import MainFrame

class App(wx.App):
    """ Represents the  entire GUI application """
    def OnInit(self):
        """ Called by WXPython itself, hence the interCapitalisation. """
        # Load the app's configuration
        config = wx.Config("Libraille", "Blind Computing")
        # Set some app metadata
        self.SetAppName("libraille")
        self.SetAppDisplayName("Libraille")
        self.SetVendorName("blindcomputing.org")
        self.SetVendorDisplayName("Blind Computing")
        # Construct the main window, passing along the app config, and set it as the app's toplevel
        frame = MainFrame(config)
        self.SetTopWindow(frame)
        # Return True to indicate success to WXPython
        return True
