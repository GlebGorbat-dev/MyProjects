cmake_minimum_required(VERSION 3.16)
project(omisLAB2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Используем Qt6 из окружения fenicsx-env
set(Qt6_DIR "/opt/miniconda3/envs/fenicsx-env/lib/cmake/Qt6")
message(STATUS "Using Qt6 from fenicsx-env: ${Qt6_DIR}")

# Добавляем необходимые компоненты Qt
find_package(Qt6 REQUIRED COMPONENTS Core Widgets PrintSupport)

# Автоматическая обработка Qt файлов
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Настройка для macOS
if(APPLE)
    set(CMAKE_MACOSX_RPATH 1)
endif()

# Исходные файлы
set(SOURCES
        main.cpp
        mainwindow.cpp
        texteditor.cpp
        tabwidget.cpp
)

set(HEADERS
        mainwindow.h
        texteditor.h
        tabwidget.h
)

# Исполняемый файл
add_executable(omisLAB2
        ${SOURCES}
        ${HEADERS}
)

# Подключение Qt модулей
target_link_libraries(omisLAB2
        Qt6::Core
        Qt6::Widgets
        Qt6::PrintSupport
)

# Добавим пути к библиотекам из conda
target_link_directories(omisLAB2 PRIVATE /opt/miniconda3/lib)
target_link_directories(omisLAB2 PRIVATE /opt/miniconda3/envs/fenicsx-env/lib)

# Настройки для macOS
if(APPLE)
    target_link_libraries(omisLAB2 "-framework Cocoa")
endif()

# Включение директорий
target_include_directories(omisLAB2 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})