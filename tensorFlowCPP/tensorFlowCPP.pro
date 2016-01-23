TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

INCLUDEPATH += /home/venefica/tensorflow/tensorflow/loader
#LIBS += -L/home/venefica/tensorflow/bazel-bin/tensorflow/loader/ -lloader
LIBS += /home/venefica/Documents/progTasks/tensorFlowCPP/libloader.a

SOURCES += main.cpp

