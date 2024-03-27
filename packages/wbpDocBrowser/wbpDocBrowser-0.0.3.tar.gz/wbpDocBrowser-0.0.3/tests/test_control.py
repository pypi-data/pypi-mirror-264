from wbBase.application import App
from wbBase.applicationInfo import ApplicationInfo, PluginInfo

appinfo = ApplicationInfo(
    Plugins=[PluginInfo(Name="docbrowser", Installation="default")]
)


def test_plugin():
    app = App(test=True, info=appinfo)
    assert "docbrowser" in app.pluginManager
    app.Destroy()

def test_LogListWindow_instance():
    app = App(test=True, info=appinfo)
    from wbpDocBrowser import DocTreeCtrl
    control = DocTreeCtrl(app.TopWindow)
    assert isinstance(control, DocTreeCtrl)
    app.Destroy()
