from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Tuple

import wx
from wbBase.document import FileNameFromPath
from wx import aui
from wx.lib.mixins import treemixin

if TYPE_CHECKING:
    from wbBase.application import App
    from wbBase.document import Document
    from wbBase.document.manager import DocumentManager

__version__ = "0.0.3"

log = logging.getLogger(__name__)

name = "DocBrowser"


class DocTreeModel:
    """
    TreeModel holds the domain objects that are shown in the tree control.
    """

    @property
    def app(self) -> App:
        """
        :return: The running Workbench application.
        """
        return wx.GetApp()

    @property
    def documentManager(self) -> DocumentManager:
        """
        :return: The document manager of the running application.
        """
        return self.app.documentManager

    @property
    def items(self) -> List[Tuple[str, tuple, str]]:
        result = []
        doc: Document
        for doc in self.documentManager.documents:
            result.append(
                (
                    FileNameFromPath(doc.path),
                    tuple((v.frame.title, (), v.typeName) for v in list(doc.views)),
                    doc.typeName,
                )
            )
        return result

    def GetItem(self, indices: Tuple[int, ...]):
        # log.warning("GetItem(%r)", indices)
        text, children, typeName = "Hidden root", self.items, ""
        for index in indices:
            text, children, typeName = children[index]
        # log.warning("GetItem -> text: %r, children: %r", text, children)
        return text, children, typeName

    def GetText(self, indices: Tuple[int, ...]) -> str:
        return self.GetItem(indices)[0]

    def GetChildren(self, indices: Tuple[int, ...]):
        return self.GetItem(indices)[1]

    def GetChildrenCount(self, indices: Tuple[int, ...]) -> int:
        return len(self.GetChildren(indices))


class DocTreeMixin(treemixin.VirtualTree):
    """
    Mixin class for virtual TreeCtrl.
    """

    def __init__(self, *args, **kwargs):
        self.model = DocTreeModel()
        super().__init__(*args, **kwargs)
        # self.createImageList()

    @property
    def app(self) -> App:
        """
        :return: The running Workbench application.
        """
        return wx.GetApp()

    @property
    def documentManager(self) -> DocumentManager:
        """
        :return: The document manager of the running application.
        """
        return self.app.documentManager

    def createImageList(self) -> None:
        """
        Create an image list from all known document and view icons.
        """
        size = (16, 16)
        self.imageDict = {}
        self.imageList = wx.ImageList(*size)
        imageIndex = 0
        for template in self.documentManager.templates:
            if template.documentTypeName not in self.imageDict:
                self.imageList.Add(template.icon)
                self.imageDict[template.documentTypeName] = imageIndex
                imageIndex += 1
                for viewtype in template.viewTypes:
                    if viewtype.typeName not in self.imageDict:
                        icon = viewtype.getIcon()
                        if icon.IsOk():
                            self.imageList.Add(icon)
                            self.imageDict[viewtype.typeName] = imageIndex
                            imageIndex += 1

        self.AssignImageList(self.imageList)

    def OnGetItemText(self, indices: Tuple[int, ...], column: int = 0) -> str:
        """
        :return: The string for the item specified by indices
        """
        return self.model.GetText(indices)

    def OnGetChildrenCount(self, indices: Tuple[int, ...]) -> int:
        """
        :return: the number of child items of the item with the
            provided indices.
        """
        return self.model.GetChildrenCount(indices)

    def OnGetItemImage(
        self,
        indices: Tuple[int, ...],
        which: int = wx.TreeItemIcon_Normal,
        column: int = 0,
    ) -> int:
        """
        :return: The index in the image list of the image to be used
        """
        text, children, typeName = self.model.GetItem(indices)
        return self.imageDict.get(typeName, -1)


class DocTreeCtrl(DocTreeMixin, wx.TreeCtrl):
    """
    TreeCtrl to show all open documents and the associated views.
    """

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TR_DEFAULT_STYLE | wx.TR_SINGLE | wx.TR_TWIST_BUTTONS,
    ):
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_itemActivated)
        self.Bind(wx.EVT_UPDATE_UI, self.on_updateUI)
        self.oldItems = None

    def on_itemActivated(self, event: wx.TreeEvent):
        """
        Handle double click on item in tree control.
        """
        item = event.GetItem()
        indices = self.GetIndexOfItem(item)
        if len(indices) == 1:
            # it is a document
            return
        elif len(indices) == 2:
            # it is a view
            doc_index, view_index = indices
            self.documentManager.documents[doc_index].views[view_index].Activate()

    def on_updateUI(self, event):
        newItems = self.model.items
        if newItems == self.oldItems:
            return
        self.RefreshItems()
        self.oldItems = newItems


info = aui.AuiPaneInfo()
info.Name(name)
info.Caption(name)
info.Dock()
info.Bottom()
info.Resizable()
info.MaximizeButton(True)
info.MinimizeButton(True)
info.CloseButton(False)
info.FloatingSize(wx.Size(300, 400))
info.BestSize(wx.Size(300, 400))
info.MinSize(wx.Size(100, 100))
if wx.GetApp():
    # todo: define unique icon for DocBrowser
    info.Icon(wx.ArtProvider.GetBitmap("FILE_BROWSER", wx.ART_FRAME_ICON))

panels = [(DocTreeCtrl, info)]


def makeImageList(app: App):
    docTreeCtrl = app.panelManager.getWindowByCaption("DocBrowser")
    docTreeCtrl.createImageList()


wx.GetApp().AddPostInitAction(makeImageList)
