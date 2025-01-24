from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt


class CustomWebEnginePage(QWebEnginePage):
    """Custom QWebEnginePage to handle right-click and middle-click for opening links in new tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def createWindow(self, web_window_type):
        """Handle requests to open a new window."""
        if web_window_type == QWebEnginePage.WebBrowserTab:
            new_tab = self.parent.create_new_tab()
            return new_tab.page()
        return super().createWindow(web_window_type)

    def context_menu_event(self, event):
        """Override the context menu to add a custom 'Open in New Tab' option."""
        context_menu = QMenu()
        open_in_new_tab_action = QAction("Open Link in New Tab", context_menu)
        open_in_new_tab_action.triggered.connect(lambda: self.open_link_in_new_tab(event))
        context_menu.addAction(open_in_new_tab_action)
        context_menu.exec_(event.globalPos())

    def open_link_in_new_tab(self, event):
        """Open the link under the cursor in a new tab."""
        link_url = self.contextMenuData().linkUrl()
        if link_url.isValid():
            self.parent.add_new_tab(link_url, "New Tab")


class PotionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Potion.")
        self.resize(1600, 1200)

        # Enable dark mode
        self.apply_dark_mode()

        # Create a tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setMovable(True)

        # Add a custom event filter for mouse middle-click to close tabs
        self.tabs.tabBar().installEventFilter(self)

        self.setCentralWidget(self.tabs)

        # Create the default browser profile with Linux user agent
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

        # Open the first tab with Notion
        self.add_new_tab(QUrl("https://www.notion.so"), "Notion")

    def apply_dark_mode(self):
        """Apply a dark mode theme to the application and web content."""
        # Set the app's dark theme
        dark_theme = """
        QMainWindow { background-color: #2b2b2b; color: #ffffff; }
        QTabWidget::pane { border: 1px solid #444; }
        QTabBar::tab { background: #3c3c3c; color: #ffffff; padding: 10px; }
        QTabBar::tab:selected { background: #555555; }
        """
        QApplication.instance().setStyleSheet(dark_theme)

    def inject_dark_mode_css(self, webview):
        """Inject dark mode CSS into the web page."""
        dark_css = """
        body, html {
            background-color: #121212 !important;
            color: #e0e0e0 !important;
        }
        a {
            color: #bb86fc !important;
        }
        """
        script = f"""
        var style = document.createElement('style');
        style.type = 'text/css';
        style.appendChild(document.createTextNode("{dark_css.replace('"', '\\"')}".replace(/\\n/g, '')));
        document.head.appendChild(style);
        """
        webview.page().runJavaScript(script)

    def add_new_tab(self, url, title="New Tab"):
        """Add a new tab with the specified URL."""
        webview = QWebEngineView()
        webview.setPage(CustomWebEnginePage(self))

        # Enable JavaScript and plugins
        webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        # Connect the titleChanged signal to dynamically update tab titles
        webview.titleChanged.connect(lambda new_title: self.update_tab_title(webview, new_title))

        # Inject dark mode CSS after loading the page
        webview.loadFinished.connect(lambda: self.inject_dark_mode_css(webview))

        # Load the specified URL
        webview.load(url)

        # Add the web view as a new tab
        self.tabs.addTab(webview, title)
        self.tabs.setCurrentWidget(webview)

        return webview

    def create_new_tab(self):
        """Create and return a new web view for a new tab."""
        webview = self.add_new_tab(QUrl("about:blank"), "New Tab")
        return webview

    def close_tab(self, index):
        """Close the specified tab."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def update_tab_title(self, webview, new_title):
        """Update the title of the tab when it changes."""
        index = self.tabs.indexOf(webview)
        if index != -1:
            self.tabs.setTabText(index, new_title)

    def eventFilter(self, source, event):
        """Handle middle mouse click events to close tabs."""
        if source == self.tabs.tabBar() and event.type() == event.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                index = self.tabs.tabBar().tabAt(event.pos())
                if index != -1:
                    self.close_tab(index)
        return super().eventFilter(source, event)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    notion_app = PotionApp()
    notion_app.show()
    sys.exit(app.exec_())
