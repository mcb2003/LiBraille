import wx

class PreferencesEditor(wx.PreferencesEditor):
    def __init__(self, config):
        # Initialise the superclass
        super().__init__()
        # Save a reference to the configuration manager for reading and writing settings
        self.config = config
        # Create and add the pages
        self.general = GeneralPreferencesPage()
        self.AddPage(self.general)

class GeneralPreferencesPage(wx.StockPreferencesPage):
    def __init__(self):
        super().__init__(wx.StockPreferencesPage.Kind_General)

    def CreateWindow(self, parent):
        # THe main container window
        panel = wx.Panel(parent)
        # Create a grid bag sizer to lay out our components
        grid = wx.GridBagSizer(hgap=5, vgap=5) # hgap and vgap add spacing between items
        # Wrap width:
        wr_lbl1 = wx.StaticText(panel, label="Braille Wrap Width")
        # This is a SpinCtrl because is *m8st* be an integer
        wr_val = wx.SpinCtrl(panel)
        wr_val.SetMin(2)
        wr_lbl2 = wx.StaticText(panel, label="characters")
        # Register all the widgets with the sizer
        grid.Add(wr_lbl1, pos=(0, 0))
        grid.Add(wr_val, pos=(0, 1))
        grid.Add(wr_lbl2, pos=(0, 2))
        # Let the sizer recalculate the positions and sizes of all items
        panel.SetSizerAndFit(grid)

        return panel
