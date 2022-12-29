import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QListWidget,
    QVBoxLayout,
    QLabel,
)
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtCore import QUrl
import requests


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a title label
        title_label = QLabel("GitHub Word Search")
        title_label.setFont(QFont("Helvetica", 18, QFont.Bold))

        # Create a text box for the search query
        self.query_edit = QLineEdit()
        self.query_edit.returnPressed.connect(self.search)

        # Create a search instruction label
        instruction_label = QLabel("Enter term and press Enter to search")
        instruction_label.setFont(QFont("Helvetica", 8))
        instruction_label.setStyleSheet("color: gray")

        # Create a list widget for the search results
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.open_url)

        # Create a vertical layout to hold the widgets
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.query_edit)
        layout.addWidget(instruction_label)
        layout.addWidget(self.results_list)
        self.setLayout(layout)

    def search(self):
        # Get the search query from the text box
        query = self.query_edit.text()

        # Search for repositories containing the specified term
        repos = self.search_repos(query)

        # Clear the list widget
        self.results_list.clear()

        # Add the URLs of the repositories to the list widget
        for repo in repos:
            self.results_list.addItem(repo["html_url"])

    def open_url(self, item):
        # Create a QUrl object from the URL string
        url = QUrl(item.text())

        # Open the URL in the user's default web browser
        QDesktopServices.openUrl(url)

    def search_repos(self, query):
        # Set the base URL for the GitHub API
        base_url = "https://api.github.com"

        # Set the endpoint for searching repositories
        endpoint = "/search/repositories"

        # Set the parameters for the search
        params = {"q": query, "sort": "updated", "order": "desc", "per_page": 20}

        # Send the request to the GitHub API
        response = requests.get(base_url + endpoint, params=params)

        # Check the status code of the response
        if response.status_code == 200:
            # If the request was successful, return the list of repositories
            return response.json()["items"]
        else:
            # If the request was unsuccessful, print an error message
            print("An error occurred:")
            print(response.status_code, response.reason)
            return None


# Create the application and search widget
app = QApplication(sys.argv)
widget = SearchWidget()
widget.show()

# Run the application loop
sys.exit(app.exec_())
