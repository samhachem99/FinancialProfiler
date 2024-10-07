import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QLabel

# Custom class for enabling drag-and-drop on QLabel
class DragDropWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)  # Load your .ui file

        # Find the existing label by name and enable drag-and-drop
        self.dragDropLabel = self.findChild(QtWidgets.QLabel, "DragnDrop")
        if self.dragDropLabel:
            self.dragDropLabel.setAcceptDrops(True)
            self.dragDropLabel.dragEnterEvent = self.dragEnterEvent
            self.dragDropLabel.dropEvent = self.dropEvent
            self.dragDropLabel.setAlignment(Qt.AlignCenter)
            self.dragDropLabel.setText("Drag and Drop Here")

        # Other widgets
        self.browseButton = self.findChild(QtWidgets.QPushButton, "Browse")
        self.processButton = self.findChild(QtWidgets.QPushButton, "Process")
        self.displayTextBox = self.findChild(QtWidgets.QTextBrowser, "Display")
        
        # Connect Browse button to open file dialog
        self.browseButton.clicked.connect(self.open_file_dialog)
        
        # Process button - placeholder for further functionality
        self.processButton.clicked.connect(self.process_file)

    def handle_file(self, file_path):
        # Display the file path in the text box
        if self.displayTextBox:
            self.displayTextBox.setText(f"File selected: {file_path}")
        else:
            print("Error: Display widget not found for displaying the file path.")

    def open_file_dialog(self):
        # Open file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            self.handle_file(file_path)

    def process_file(self):
        # Placeholder function to handle the processing of the file
        if self.displayTextBox:
            current_text = self.displayTextBox.toPlainText()
            if current_text:
                # Example action - you can replace this with your actual processing
                self.displayTextBox.append("Processing the file...")

    # Drag-and-drop event handlers
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            # Process each file dropped onto the label
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.handle_file(file_path)
        else:
            event.ignore()

app = QtWidgets.QApplication(sys.argv)
window = DragDropWidget()
window.show()
app.exec_()
