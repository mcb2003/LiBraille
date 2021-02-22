import wx

from .preference_value import PreferenceValue

class PreferencesEditor(wx.PreferencesEditor):
    def __init__(self, config):
        # Initialise the superclass
        super().__init__()
        # Create and add the pages
        self.general = GeneralPreferencesPage(config)
        self.AddPage(self.general)

class GeneralPreferencesPage(wx.StockPreferencesPage):
    def __init__(self, config):
        super().__init__(wx.StockPreferencesPage.Kind_General)
        self.config = config

    def CreateWindow(self, parent):
        # THe main container window
        panel = wx.Panel(parent)
        # Create a grid bag sizer to lay out our components
        grid = wx.GridBagSizer(hgap=5, vgap=5) # hgap and vgap add spacing between items
        # Wrap width:
        wr_lbl1 = wx.StaticText(panel, label="Braille Wrap Width")
        # This is a SpinCtrl because is *must* be an integer
        wr_val = wx.SpinCtrl(panel)
        # Mirror the currently set width from saved settings
        wr_val.SetValue(self.config.ReadInt("engine/wrap-width", 40))
        # Update settings when the SpinCtrl is changed
        wr_val.Bind(wx.EVT_SPINCTRL, self.on_wr_update)
        wr_val.SetMin(2)
        wr_lbl2 = wx.StaticText(panel, label="characters")
        # Register all the widgets with the sizer
        grid.Add(wr_lbl1, pos=(0, 0))
        grid.Add(wr_val, pos=(0, 1))
        grid.Add(wr_lbl2, pos=(0, 2))
        # Let the sizer recalculate the positions and sizes of all items
        panel.SetSizerAndFit(grid)

        return panel

    def on_wr_update(self, evt):
        """ Called when the user changes the wrap width. """
        self.config.WriteInt("engine/wrap-width", evt.GetPosition())
        evt.Skip()
