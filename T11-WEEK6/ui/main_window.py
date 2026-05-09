import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
    QStackedWidget, QLineEdit, QTextEdit, QComboBox, QMessageBox,
    QListWidget, QFormLayout, QGroupBox, QStatusBar, QFrame
)
from PySide6.QtCore import Qt, Slot

from api.post_api import (
    FetchPostsWorker, FetchPostDetailWorker, CreatePostWorker,
    UpdatePostWorker, DeletePostWorker
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Post Manager")
        self.resize(1000, 600)
        
        self.current_worker = None
        self.selected_post_id = None
        self.current_mode = "view" # "view", "add", "edit"
        
        self.init_ui()
        self.load_posts()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left Panel (Table)
        left_panel = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_add = QPushButton("Add Post")
        self.btn_add.setObjectName("btn_add")
        self.btn_edit = QPushButton("Edit Post")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_delete = QPushButton("Delete Post")
        self.btn_delete.setObjectName("btn_delete")
        
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        
        self.btn_refresh.clicked.connect(self.load_posts)
        self.btn_add.clicked.connect(self.show_add_form)
        self.btn_edit.clicked.connect(self.show_edit_form)
        self.btn_delete.clicked.connect(self.delete_post_confirm)
        
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_table_selection)
        
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(self.table)
        
        # Right Panel
        self.right_stack = QStackedWidget()
        
        # Index 0: Placeholder
        placeholder = QLabel("Select a post or click 'Add Post'")
        placeholder.setAlignment(Qt.AlignCenter)
        self.right_stack.addWidget(placeholder)
        
        # Index 1: Detail View
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        
        self.lbl_detail_title = QLabel()
        self.lbl_detail_title.setObjectName("lbl_detail_title")
        self.lbl_detail_title.setWordWrap(True)
        
        self.lbl_detail_info = QLabel()
        self.lbl_detail_info.setWordWrap(True)
        
        self.lbl_detail_body = QTextEdit()
        self.lbl_detail_body.setReadOnly(True)
        
        self.list_comments = QListWidget()
        
        detail_layout.addWidget(self.lbl_detail_title)
        detail_layout.addWidget(self.lbl_detail_info)
        detail_layout.addWidget(QLabel("Body:"))
        detail_layout.addWidget(self.lbl_detail_body)
        detail_layout.addWidget(QLabel("Comments:"))
        detail_layout.addWidget(self.list_comments)
        
        self.right_stack.addWidget(detail_widget)
        
        # Index 2: Form View
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        self.form_group = QGroupBox("Post Form")
        flayout = QFormLayout(self.form_group)
        
        self.txt_title = QLineEdit()
        self.txt_author = QLineEdit()
        self.txt_slug = QLineEdit()
        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["published", "draft"])
        self.txt_body = QTextEdit()
        
        flayout.addRow("Title:", self.txt_title)
        flayout.addRow("Author:", self.txt_author)
        flayout.addRow("Slug:", self.txt_slug)
        flayout.addRow("Status:", self.cmb_status)
        flayout.addRow("Body:", self.txt_body)
        
        self.lbl_form_error = QLabel()
        self.lbl_form_error.setStyleSheet("color: red;")
        self.lbl_form_error.setWordWrap(True)
        self.lbl_form_error.hide()
        flayout.addRow("", self.lbl_form_error)
        
        btn_save = QPushButton("Save")
        btn_save.setObjectName("btn_save")
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("btn_cancel")
        btn_save.clicked.connect(self.save_post)
        btn_cancel.clicked.connect(self.cancel_form)
        
        f_btn_layout = QHBoxLayout()
        f_btn_layout.addWidget(btn_save)
        f_btn_layout.addWidget(btn_cancel)
        
        form_layout.addWidget(self.form_group)
        form_layout.addLayout(f_btn_layout)
        
        self.right_stack.addWidget(form_widget)
        
        main_layout.addLayout(left_panel, 6)
        main_layout.addWidget(self.right_stack, 4)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def set_loading(self, is_loading, message="Loading..."):
        if is_loading:
            self.status_bar.showMessage(message)
            self.btn_refresh.setEnabled(False)
            self.btn_add.setEnabled(False)
            self.table.setEnabled(False)
            self.right_stack.setEnabled(False)
        else:
            self.status_bar.clearMessage()
            self.btn_refresh.setEnabled(True)
            self.btn_add.setEnabled(True)
            self.table.setEnabled(True)
            self.right_stack.setEnabled(True)

    def abort_current_worker(self):
        if self.current_worker and self.current_worker.isRunning():
            try:
                self.current_worker.disconnect()
            except Exception:
                pass
            
            if not hasattr(self, 'running_workers'):
                self.running_workers = []
            self.running_workers.append(self.current_worker)
            
            worker = self.current_worker
            worker.finished.connect(lambda: self.cleanup_running_worker(worker))
            worker.error.connect(lambda: self.cleanup_running_worker(worker))
            
            self.current_worker = None

    def cleanup_running_worker(self, worker):
        if hasattr(self, 'running_workers') and worker in self.running_workers:
            self.running_workers.remove(worker)

    def on_table_selection(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            post_id = self.table.item(row, 0).text()
            self.selected_post_id = post_id
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
            
            if self.current_mode == "view":
                self.load_post_detail(post_id)
        else:
            self.selected_post_id = None
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)

    def cancel_form(self):
        self.current_mode = "view"
        self.lbl_form_error.hide()
        if self.selected_post_id:
            self.load_post_detail(self.selected_post_id)
        else:
            self.right_stack.setCurrentIndex(0)

    def load_posts(self):
        self.set_loading(True, "Fetching posts...")
        self.abort_current_worker()
        self.current_worker = FetchPostsWorker()
        self.current_worker.finished.connect(self.on_posts_loaded)
        self.current_worker.error.connect(self.on_api_error)
        self.current_worker.start()

    @Slot(list)
    def on_posts_loaded(self, posts):
        self.set_loading(False)
        self.table.setRowCount(0)
        for post in posts:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(post.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(post.get("title", "")))
            self.table.setItem(row, 2, QTableWidgetItem(post.get("author", "")))
            self.table.setItem(row, 3, QTableWidgetItem(post.get("status", "")))
        
        self.table.clearSelection()
        self.selected_post_id = None
        self.current_mode = "view"
        self.right_stack.setCurrentIndex(0)

    def load_post_detail(self, post_id):
        self.set_loading(True, f"Fetching details for Post {post_id}...")
        self.abort_current_worker()
        self.current_worker = FetchPostDetailWorker(post_id)
        self.current_worker.finished.connect(self.on_post_detail_loaded)
        self.current_worker.error.connect(self.on_api_error)
        self.current_worker.start()

    @Slot(dict)
    def on_post_detail_loaded(self, post):
        self.set_loading(False)
        self.right_stack.setCurrentIndex(1)
        self.current_mode = "view"
        
        self.lbl_detail_title.setText(post.get("title", ""))
        info = f"ID: {post.get('id', '')} | Author: {post.get('author', '')} | Status: {post.get('status', '')}\nSlug: {post.get('slug', '')}"
        self.lbl_detail_info.setText(info)
        self.lbl_detail_body.setPlainText(post.get("body", ""))
        
        self.list_comments.clear()
        comments = post.get("comments", [])
        if comments:
            for comment in comments:
                item = f"{comment.get('name', 'Anonymous')}: {comment.get('body', '')}"
                self.list_comments.addItem(item)
        else:
            self.list_comments.addItem("No comments.")

    def show_add_form(self):
        self.current_mode = "add"
        self.form_group.setTitle("Add New Post")
        self.txt_title.clear()
        self.txt_author.clear()
        self.txt_slug.clear()
        self.txt_body.clear()
        self.cmb_status.setCurrentIndex(0)
        self.lbl_form_error.hide()
        
        self.table.clearSelection()
        self.selected_post_id = None
        self.right_stack.setCurrentIndex(2)

    def show_edit_form(self):
        if not self.selected_post_id:
            return
        self.current_mode = "edit"
        self.form_group.setTitle(f"Edit Post {self.selected_post_id}")
        self.lbl_form_error.hide()
        
        self.set_loading(True, "Fetching post data for editing...")
        self.abort_current_worker()
        self.current_worker = FetchPostDetailWorker(self.selected_post_id)
        self.current_worker.finished.connect(self.on_edit_data_loaded)
        self.current_worker.error.connect(self.on_api_error)
        self.current_worker.start()

    @Slot(dict)
    def on_edit_data_loaded(self, post):
        self.set_loading(False)
        self.txt_title.setText(post.get("title", ""))
        self.txt_author.setText(post.get("author", ""))
        self.txt_slug.setText(post.get("slug", ""))
        self.txt_body.setPlainText(post.get("body", ""))
        status = post.get("status", "draft")
        index = self.cmb_status.findText(status)
        if index >= 0:
            self.cmb_status.setCurrentIndex(index)
        
        self.right_stack.setCurrentIndex(2)

    def save_post(self):
        self.lbl_form_error.hide()
        data = {
            "title": self.txt_title.text().strip(),
            "author": self.txt_author.text().strip(),
            "slug": self.txt_slug.text().strip(),
            "status": self.cmb_status.currentText(),
            "body": self.txt_body.toPlainText().strip()
        }
        
        if not data["title"] or not data["author"] or not data["slug"] or not data["body"]:
            QMessageBox.warning(self, "Validation Error", "All fields are required!")
            return
            
        self.abort_current_worker()
        if self.current_mode == "add":
            self.set_loading(True, "Creating post...")
            self.current_worker = CreatePostWorker(data)
            self.current_worker.finished.connect(self.on_post_created)
        else:
            self.set_loading(True, f"Updating Post {self.selected_post_id}...")
            self.current_worker = UpdatePostWorker(self.selected_post_id, data)
            self.current_worker.finished.connect(self.on_post_updated)
            
        self.current_worker.error.connect(self.on_api_error)
        self.current_worker.validation_error.connect(self.on_validation_error)
        self.current_worker.start()

    @Slot(dict)
    def on_post_created(self, data):
        self.set_loading(False)
        post_id = data.get('id', 'Unknown')
        QMessageBox.information(self, "Success", f"Post created successfully!\nID: {post_id}")
        self.load_posts()

    @Slot(dict)
    def on_post_updated(self, data):
        self.set_loading(False)
        QMessageBox.information(self, "Success", "Post updated successfully!")
        self.load_posts()

    def delete_post_confirm(self):
        if not self.selected_post_id:
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete Post ID {self.selected_post_id}? This will also delete its comments.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.set_loading(True, f"Deleting Post {self.selected_post_id}...")
            self.abort_current_worker()
            self.current_worker = DeletePostWorker(self.selected_post_id)
            self.current_worker.finished.connect(self.on_post_deleted)
            self.current_worker.error.connect(self.on_api_error)
            self.current_worker.start()

    @Slot(bool)
    def on_post_deleted(self, success):
        self.set_loading(False)
        QMessageBox.information(self, "Success", "Post deleted successfully!")
        self.load_posts()

    @Slot(str)
    def on_api_error(self, message):
        self.set_loading(False)
        QMessageBox.critical(self, "Error", message)

    @Slot(dict)
    def on_validation_error(self, errors):
        self.set_loading(False)
        err_msg = "Validation Error:\n"
        for field, messages in errors.items():
            if isinstance(messages, list):
                err_msg += f"- {field}: {', '.join(messages)}\n"
            else:
                err_msg += f"- {field}: {messages}\n"
        self.lbl_form_error.setText(err_msg)
        self.lbl_form_error.show()
