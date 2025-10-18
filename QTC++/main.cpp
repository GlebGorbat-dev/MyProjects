#include <QApplication>
#include <QStyleFactory>
#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // Настройка для macOS
    app.setAttribute(Qt::AA_DontShowIconsInMenus, false);
    app.setStyle(QStyleFactory::create("Fusion"));

    // Настройка информации о приложении
    app.setApplicationName("TextEditor");
    app.setApplicationVersion("1.0");
    app.setOrganizationName("YourCompany");

    MainWindow window;
    window.show();

    return app.exec();
}