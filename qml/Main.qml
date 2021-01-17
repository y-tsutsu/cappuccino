import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: window
    visible: false
    minimumWidth: 250
    minimumHeight: 150
    title: qsTr("cappuccino")
    flags: Qt.Window | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint

    Material.theme: Material.Light
    Material.accent: Material.Purple

    Downloader {
        id: downloader
    }

    MessageDialog {
        id: message_dialog
        title: window.title
        message: qsTr("Delete all image ?")
        onAccepted: mmodel.clear()
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onClicked: {
            if (mouse.button === Qt.RightButton) {
                menu.popup(mouse.x, mouse.y)
            }
        }

        onPressAndHold: {
            if (mouse.source === Qt.MouseEventNotSynthesized) {
                menu.popup(mouse.x, mouse.y)
            }
        }

        Menu {
            id: menu

            MenuItem {
                text: "Top"
                checkable: true
                checked: true
                onTriggered: {
                    if (checked) {
                        window.flags |= Qt.WindowStaysOnTopHint
                    } else {
                        window.flags &= ~Qt.WindowStaysOnTopHint
                    }
                }
            }

            MenuItem {
                text: "Hide"
                onTriggered: window.showMinimized()
            }

            MenuItem {
                text: "Clear"
                onTriggered: {
                    message_dialog.show()
                }
            }

            MenuItem {
                text: "Exit"
                onTriggered: window.close()
            }
        }
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
