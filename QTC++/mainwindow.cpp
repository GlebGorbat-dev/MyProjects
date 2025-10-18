#include "mainwindow.h"
#include "tabwidget.h"
#include "texteditor.h"
#include <QApplication>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    // Создание виджета вкладок
    tabWidget = new TabWidget(this);
    setCentralWidget(tabWidget);

    createActions();
    createMenus();
    createToolBars();
    createStatusBar();

    connect(tabWidget, &TabWidget::currentChanged, this, &MainWindow::currentTabChanged);
    connect(tabWidget, &TabWidget::tabCloseRequested, this, &MainWindow::closeTab);

    // Создать первую вкладку
    newFile();

    setWindowTitle("TextEditor - Untitled");
    resize(800, 600);
}

MainWindow::~MainWindow() {}

void MainWindow::createActions() {
    // Файл
    newAct = new QAction(tr("&New"), this);
    newAct->setShortcuts(QKeySequence::New);
    newAct->setStatusTip(tr("Create a new file"));
    connect(newAct, &QAction::triggered, this, &MainWindow::newFile);

    openAct = new QAction(tr("&Open..."), this);
    openAct->setShortcuts(QKeySequence::Open);
    openAct->setStatusTip(tr("Open an existing file"));
    connect(openAct, &QAction::triggered, this, &MainWindow::openFile);

    saveAct = new QAction(tr("&Save"), this);
    saveAct->setShortcuts(QKeySequence::Save);
    saveAct->setStatusTip(tr("Save the document to disk"));
    connect(saveAct, &QAction::triggered, this, &MainWindow::saveFile);

    saveAsAct = new QAction(tr("Save &As..."), this);
    saveAsAct->setShortcuts(QKeySequence::SaveAs);
    saveAsAct->setStatusTip(tr("Save the document under a new name"));
    connect(saveAsAct, &QAction::triggered, this, &MainWindow::saveAsFile);

    printAct = new QAction(tr("&Print..."), this);
    printAct->setShortcuts(QKeySequence::Print);
    printAct->setStatusTip(tr("Print the document"));
    connect(printAct, &QAction::triggered, this, &MainWindow::printFile);

    exitAct = new QAction(tr("E&xit"), this);
    exitAct->setShortcuts(QKeySequence::Quit);
    exitAct->setStatusTip(tr("Exit the application"));
    connect(exitAct, &QAction::triggered, this, &QWidget::close);

    // Правка
    cutAct = new QAction(tr("Cu&t"), this);
    cutAct->setShortcuts(QKeySequence::Cut);
    cutAct->setStatusTip(tr("Cut the current selection's contents to the clipboard"));
    connect(cutAct, &QAction::triggered, this, []() {
        if (QTextEdit *editor = qobject_cast<QTextEdit*>(QApplication::focusWidget())) {
            editor->cut();
        }
    });

    copyAct = new QAction(tr("&Copy"), this);
    copyAct->setShortcuts(QKeySequence::Copy);
    copyAct->setStatusTip(tr("Copy the current selection's contents to the clipboard"));
    connect(copyAct, &QAction::triggered, this, []() {
        if (QTextEdit *editor = qobject_cast<QTextEdit*>(QApplication::focusWidget())) {
            editor->copy();
        }
    });

    pasteAct = new QAction(tr("&Paste"), this);
    pasteAct->setShortcuts(QKeySequence::Paste);
    pasteAct->setStatusTip(tr("Paste the clipboard's contents into the current selection"));
    connect(pasteAct, &QAction::triggered, this, []() {
        if (QTextEdit *editor = qobject_cast<QTextEdit*>(QApplication::focusWidget())) {
            editor->paste();
        }
    });

    undoAct = new QAction(tr("&Undo"), this);
    undoAct->setShortcuts(QKeySequence::Undo);
    undoAct->setStatusTip(tr("Undo the last operation"));
    connect(undoAct, &QAction::triggered, this, []() {
        if (QTextEdit *editor = qobject_cast<QTextEdit*>(QApplication::focusWidget())) {
            editor->undo();
        }
    });

    redoAct = new QAction(tr("&Redo"), this);
    redoAct->setShortcuts(QKeySequence::Redo);
    redoAct->setStatusTip(tr("Redo the last operation"));
    connect(redoAct, &QAction::triggered, this, []() {
        if (QTextEdit *editor = qobject_cast<QTextEdit*>(QApplication::focusWidget())) {
            editor->redo();
        }
    });

    // Форматирование шрифта
    italicAct = new QAction(tr("&Italic"), this);
    italicAct->setShortcut(QKeySequence("Ctrl+I"));
    italicAct->setStatusTip(tr("Make selected text italic"));
    italicAct->setIcon(QIcon(":/icons/italic.png")); // Можно добавить иконку
    connect(italicAct, &QAction::triggered, this, &MainWindow::setItalic);

    timesNewRomanAct = new QAction(tr("&Times New Roman"), this);
    timesNewRomanAct->setShortcut(QKeySequence("Ctrl+T"));
    timesNewRomanAct->setStatusTip(tr("Change selected text to Times New Roman"));
    timesNewRomanAct->setIcon(QIcon(":/icons/times.png")); // Можно добавить иконку
    connect(timesNewRomanAct, &QAction::triggered, this, &MainWindow::setTimesNewRoman);

    // Справка
    aboutAct = new QAction(tr("&About"), this);
    aboutAct->setStatusTip(tr("Show the application's About box"));
    connect(aboutAct, &QAction::triggered, this, &MainWindow::about);
}

void MainWindow::createMenus() {
    fileMenu = menuBar()->addMenu(tr("&File"));
    fileMenu->addAction(newAct);
    fileMenu->addAction(openAct);
    fileMenu->addAction(saveAct);
    fileMenu->addAction(saveAsAct);
    fileMenu->addSeparator();
    fileMenu->addAction(printAct);
    fileMenu->addSeparator();
    fileMenu->addAction(exitAct);

    editMenu = menuBar()->addMenu(tr("&Edit"));
    editMenu->addAction(undoAct);
    editMenu->addAction(redoAct);
    editMenu->addSeparator();
    editMenu->addAction(cutAct);
    editMenu->addAction(copyAct);
    editMenu->addAction(pasteAct);

    helpMenu = menuBar()->addMenu(tr("&Help"));
    helpMenu->addAction(aboutAct);
}

void MainWindow::createToolBars() {
    fileToolBar = addToolBar(tr("File"));
    fileToolBar->addAction(newAct);
    fileToolBar->addAction(openAct);
    fileToolBar->addAction(saveAct);

    editToolBar = addToolBar(tr("Edit"));
    editToolBar->addAction(undoAct);
    editToolBar->addAction(redoAct);
    editToolBar->addSeparator();
    editToolBar->addAction(cutAct);
    editToolBar->addAction(copyAct);
    editToolBar->addAction(pasteAct);
    editToolBar->addSeparator();
    editToolBar->addAction(italicAct);
    editToolBar->addAction(timesNewRomanAct);
}

void MainWindow::createStatusBar() {
    statusBar()->showMessage(tr("Ready"));
}

void MainWindow::newFile() {
    TextEditor *editor = new TextEditor();
    int index = tabWidget->addTab(editor, tr("Untitled"));
    tabWidget->setCurrentIndex(index);
    connect(editor, &TextEditor::textChanged, this, &MainWindow::updateWindowTitle);
    updateWindowTitle();
}

void MainWindow::openFile() {
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"), "",
                                                    tr("Text Files (*.txt);;All Files (*)"));
    if (!fileName.isEmpty()) {
        QFile file(fileName);
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
            QMessageBox::warning(this, tr("Error"), tr("Cannot open file: %1").arg(file.errorString()));
            return;
        }

        QTextStream in(&file);
        TextEditor *editor = new TextEditor();
        editor->setPlainText(in.readAll());
        editor->setFilePath(fileName);

        int index = tabWidget->addTab(editor, QFileInfo(fileName).fileName());
        tabWidget->setCurrentIndex(index);
        connect(editor, &TextEditor::textChanged, this, &MainWindow::updateWindowTitle);

        file.close();
        updateWindowTitle();
    }
}

void MainWindow::saveFile() {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->currentWidget());
    if (!editor) return;

    if (editor->getFilePath().isEmpty()) {
        saveAsFile();
    } else {
        QFile file(editor->getFilePath());
        if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QMessageBox::warning(this, tr("Error"), tr("Cannot save file: %1").arg(file.errorString()));
            return;
        }

        QTextStream out(&file);
        out << editor->toPlainText();
        editor->setModified(false);
        file.close();

        updateWindowTitle();
        statusBar()->showMessage(tr("File saved"), 2000);
    }
}

void MainWindow::saveAsFile() {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->currentWidget());
    if (!editor) return;

    QString fileName = QFileDialog::getSaveFileName(this, tr("Save File"), "",
                                                    tr("Text Files (*.txt);;All Files (*)"));
    if (!fileName.isEmpty()) {
        editor->setFilePath(fileName);
        saveFile();
        tabWidget->setTabText(tabWidget->currentIndex(), QFileInfo(fileName).fileName());
    }
}

void MainWindow::printFile() {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->currentWidget());
    if (!editor) return;

    QPrinter printer;
    QPrintDialog dialog(&printer, this);
    if (dialog.exec() == QDialog::Accepted) {
        editor->print(&printer);
    }
}

void MainWindow::closeTab(int index) {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->widget(index));
    if (editor && editor->isModified()) {
        QMessageBox::StandardButton ret = QMessageBox::warning(this, tr("Unsaved Changes"),
                                                               tr("The document has been modified.\nDo you want to save your changes?"),
                                                               QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);

        if (ret == QMessageBox::Save) {
            if (editor->getFilePath().isEmpty()) {
                saveAsFile();
            } else {
                saveFile();
            }
        } else if (ret == QMessageBox::Cancel) {
            return;
        }
    }

    tabWidget->removeTab(index);
    delete editor;

    if (tabWidget->count() == 0) {
        newFile();
    }
}

void MainWindow::currentTabChanged(int index) {
    updateWindowTitle();
}

void MainWindow::updateWindowTitle() {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->currentWidget());
    if (editor) {
        QString title = editor->getFilePath().isEmpty() ? "Untitled" : QFileInfo(editor->getFilePath()).fileName();
        if (editor->isModified()) {
            title += "*";
        }
        setWindowTitle(tr("TextEditor - %1").arg(title));
    }
}

void MainWindow::setItalic() {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->currentWidget());
    if (!editor) return;

    QTextCursor cursor = editor->textCursor();
    if (!cursor.hasSelection()) return;

    // Применяем курсив к выделенному тексту
    QTextCharFormat format;
    format.setFontItalic(true);
    cursor.mergeCharFormat(format);
    
    // Перемещаем курсор в конец выделения и сбрасываем форматирование
    cursor.clearSelection();
    QTextCharFormat defaultFormat;
    defaultFormat.setFontItalic(false);
    cursor.setCharFormat(defaultFormat);
    
    // Устанавливаем обновленный курсор
    editor->setTextCursor(cursor);
}

void MainWindow::setTimesNewRoman() {
    TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->currentWidget());
    if (!editor) return;

    QTextCursor cursor = editor->textCursor();
    if (!cursor.hasSelection()) return;

    // Применяем Times New Roman к выделенному тексту
    QTextCharFormat format;
    format.setFontFamilies(QStringList() << "Times New Roman");
    cursor.mergeCharFormat(format);
    
    // Перемещаем курсор в конец выделения и сбрасываем форматирование
    cursor.clearSelection();
    QTextCharFormat defaultFormat;
    // Не устанавливаем конкретное семейство шрифтов, чтобы использовать шрифт по умолчанию
    cursor.setCharFormat(defaultFormat);
    
    // Устанавливаем обновленный курсор
    editor->setTextCursor(cursor);
}

void MainWindow::about() {
    QMessageBox::about(this, tr("About TextEditor"),
                       tr("<b>TextEditor</b> v1.0<br/><br/>"
                          "A simple text editor with multi-document support.<br/>"
                          "Built with Qt6 for macOS."));
}

void MainWindow::closeEvent(QCloseEvent *event) {
    if (maybeSave()) {
        event->accept();
    } else {
        event->ignore();
    }
}

bool MainWindow::maybeSave() {
    for (int i = 0; i < tabWidget->count(); ++i) {
        TextEditor *editor = qobject_cast<TextEditor*>(tabWidget->widget(i));
        if (editor && editor->isModified()) {
            tabWidget->setCurrentIndex(i);
            QMessageBox::StandardButton ret = QMessageBox::warning(this, tr("Unsaved Changes"),
                                                                   tr("The document has been modified.\nDo you want to save your changes?"),
                                                                   QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);

            if (ret == QMessageBox::Save) {
                if (editor->getFilePath().isEmpty()) {
                    saveAsFile();
                } else {
                    saveFile();
                }
                // Проверяем, сохранился ли файл
                if (editor->isModified()) {
                    return false; // Пользователь отменил сохранение
                }
            } else if (ret == QMessageBox::Cancel) {
                return false;
            }
        }
    }
    return true;
}