#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTabWidget>
#include <QMenu>
#include <QMenuBar>
#include <QToolBar>
#include <QStatusBar>
#include <QAction>
#include <QMessageBox>
#include <QFileDialog>
#include <QTextStream>
#include <QCloseEvent>
#include <QFileInfo>
#include <QPrinter>
#include <QPrintDialog>

class TabWidget;
class TextEditor;

class MainWindow : public QMainWindow {
Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    void closeEvent(QCloseEvent *event) override;

private slots:
    void newFile();
    void openFile();
    void saveFile();
    void saveAsFile();
    void closeTab(int index);
    void currentTabChanged(int index);
    void updateWindowTitle();
    void about();
    void printFile();
    void setItalic();
    void setTimesNewRoman();

private:
    void createActions();
    void createMenus();
    void createToolBars();
    void createStatusBar();
    bool maybeSave();

    TabWidget *tabWidget;

    // Меню
    QMenu *fileMenu;
    QMenu *editMenu;
    QMenu *viewMenu;
    QMenu *helpMenu;

    // Панель инструментов
    QToolBar *fileToolBar;
    QToolBar *editToolBar;

    // Действия
    QAction *newAct;
    QAction *openAct;
    QAction *saveAct;
    QAction *saveAsAct;
    QAction *printAct;
    QAction *exitAct;
    QAction *cutAct;
    QAction *copyAct;
    QAction *pasteAct;
    QAction *undoAct;
    QAction *redoAct;
    QAction *italicAct;
    QAction *timesNewRomanAct;
    QAction *aboutAct;
};

#endif // MAINWINDOW_H