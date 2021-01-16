import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: window
    visible: false
    minimumWidth: 250
    minimumHeight: 150
    title: qsTr("Hello World")
    flags: Qt.Window | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint

    Material.theme: Material.Light
    Material.accent: Material.Purple

    Downloader {
        id: downloader
    }

    Component.onCompleted: {
        const h = Screen.height / 5
        width = h * 5 / 3
        height = h
        setX(Screen.width / 2 - width / 2)
        setY(Screen.height / 2 - height / 2)
        setVisible(true)
    }
}
