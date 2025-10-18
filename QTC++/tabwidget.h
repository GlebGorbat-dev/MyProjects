
#ifndef OMISLAB2_TABWIDGET_H
#define OMISLAB2_TABWIDGET_H

#include <QTabWidget>
#include <QTabBar>

class TabWidget : public QTabWidget {
Q_OBJECT

public:
    explicit TabWidget(QWidget *parent = nullptr);

protected:
    void mousePressEvent(QMouseEvent *event) override;

private slots:
    void onTabContextMenuRequested(const QPoint &pos);
    void closeCurrentTab();
    void closeOtherTabs();
    void closeAllTabs();
};

#endif //OMISLAB2_TABWIDGET_H
