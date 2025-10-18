#include "tabwidget.h"
#include <QMouseEvent>
#include <QMenu>
#include <QMessageBox>

TabWidget::TabWidget(QWidget *parent) : QTabWidget(parent) {
    setTabsClosable(true);
    setMovable(true);
    setDocumentMode(true);

    tabBar()->setContextMenuPolicy(Qt::CustomContextMenu);
    connect(tabBar(), &QTabBar::customContextMenuRequested,
            this, &TabWidget::onTabContextMenuRequested);
}

void TabWidget::mousePressEvent(QMouseEvent *event) {
    if (event->button() == Qt::MiddleButton) {
        int tabIndex = tabBar()->tabAt(event->pos());
        if (tabIndex >= 0) {
            emit tabCloseRequested(tabIndex);
        }
    }
    QTabWidget::mousePressEvent(event);
}

void TabWidget::onTabContextMenuRequested(const QPoint &pos) {
    int tabIndex = tabBar()->tabAt(pos);
    if (tabIndex < 0) return;

    QMenu menu;
    menu.addAction(tr("Close Tab"), this, [this, tabIndex]() {
        emit tabCloseRequested(tabIndex);
    });
    menu.addAction(tr("Close Other Tabs"), this, &TabWidget::closeOtherTabs);
    menu.addAction(tr("Close All Tabs"), this, &TabWidget::closeAllTabs);

    menu.exec(tabBar()->mapToGlobal(pos));
}

void TabWidget::closeCurrentTab() {
    emit tabCloseRequested(currentIndex());
}

void TabWidget::closeOtherTabs() {
    int current = currentIndex();
    for (int i = count() - 1; i >= 0; --i) {
        if (i != current) {
            emit tabCloseRequested(i);
        }
    }
}

void TabWidget::closeAllTabs() {
    for (int i = count() - 1; i >= 0; --i) {
        emit tabCloseRequested(i);
    }
}