#include "texteditor.h"

TextEditor::TextEditor(QWidget *parent) : QTextEdit(parent) {
    setAcceptRichText(true); // Включаем поддержку форматированного текста
    setFont(QFont("Monaco", 12)); // macOS-шрифт
}