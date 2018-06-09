import os
import wx

class CheckboxComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.sampleList = ['zero', 'one']
        self.curitem = -1
    
    def Create(self, parent):
        self.clb = wx.CheckListBox(parent, -1, choices = self.sampleList)
        self.clb.Bind(wx.EVT_MOTION, self.OnMotion)
        self.clb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True
    
    def GetControl(self):
        return self.clb
    
    def OnMotion(self, evt):
        item = self.clb.HitTest(evt.GetPosition())
        if item >= 0:
            self.clb.SetSelection(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        checked = self.clb.IsChecked(self.curitem)
        self.clb.Check(self.curitem, not checked)
        self.Dismiss()
    
    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        # this part is unnecessary since the selection has
        # been set in OnMotion
        if self.curitem >= 0:
            self.clb.SetSelection(self.curitem)

    # Return a string representation of the selected item(s)
    def GetStringValue(self):
        return ','.join(self.clb.GetCheckedStrings())

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

class ListCtrlComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None

    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)


class TestPanel_CheckedListBox(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        fgs = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)

        cc = wx.ComboCtrl(self, size = (250, -1))
        tcp = CheckboxComboPopup()
        cc.SetPopupControl(tcp)
        fgs.Add(cc)
        fgs.Add((10,10))
        fgs.Add(wx.StaticText(self, -1, "Checkbox Combo"))

        box = wx.BoxSizer()
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, 20)
        self.SetSizer(box)

class TestPanel_ListCtrl(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        fgs = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)

        cc = wx.ComboCtrl(self, size = (250, -1))
        tcp = ListCtrlComboPopup()
        cc.SetPopupControl(tcp)
        fgs.Add(cc)
        fgs.Add((10,10))
        fgs.Add(wx.StaticText(self, -1, "ListCtrl Combo"))

        tcp.AddItem("First Item")
        tcp.AddItem("Second Item")
        tcp.AddItem("Third Item")

        box = wx.BoxSizer()
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, 20)
        self.SetSizer(box)

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = TestPanel_CheckedListBox(self, None)        
        #panel = TestPanel_ListCtrl(self, None)        

if __name__=="__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
