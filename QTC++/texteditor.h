
#ifndef OMISLAB2_TEXTEDITOR_H
#define OMISLAB2_TEXTEDITOR_H

#include <QTextEdit>
#include <QString>

class TextEditor : public QTextEdit {
Q_OBJECT

public:
    explicit TextEditor(QWidget *parent = nullptr);

    QString getFilePath() const { return filePath; }
    void setFilePath(const QString &path) { filePath = path; }

    bool isModified() const { return QTextEdit::document()->isModified(); }
    void setModified(bool modified) { QTextEdit::document()->setModified(modified); }

private:
    QString filePath;
};

#endif //OMISLAB2_TEXTEDITOR_H
