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

    property bool isDownload: mmodel.is_download

    Item {
        id: item
        anchors.fill: parent

        Downloader {
            id: downloader
            visible: false
        }

        ImageViewer {
            id: viewer
            visible: false
        }

        states: [
            State {
                when: window.isDownload
                PropertyChanges {
                    target: downloader
                    visible: true
                }
                PropertyChanges {
                    target: viewer
                    visible: false
                }
            },
            State {
                when: !window.isDownload
                PropertyChanges {
                    target: downloader
                    visible: false
                }
                PropertyChanges {
                    target: viewer
                    visible: true
                }
            }
        ]
    }

    MessageToolTip {
        id: message
        message: qsTr("Delete all image ?")
        onAccepted: mmodel.clear()
    }

    Menu {
        id: menu

        MenuItem {
            text: "TOP"
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
            text: "HIDE"
            onTriggered: window.showMinimized()
        }

        MenuItem {
            text: "CLEAR"
            onTriggered: {
                message.show(Qt.size(window.width, window.height))
            }
        }

        MenuItem {
            text: "EXIT"
            onTriggered: {
                viewer.release()
                window.release()
                window.close()
            }
        }
    }

    MouseArea {
        id: marea

        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        property point pressPoint: Qt.point(0, 0)

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

        onDoubleClicked: {
            if (mouse.button === Qt.LeftButton) {
                window.showMinimized()
            }
        }

        onPressed: {
            if (mouse.button === Qt.LeftButton) {
                marea.pressPoint = Qt.point(mouse.x, mouse.y)
            }
        }

        onPositionChanged: {
            var gpos = mapToGlobal(mouse.x, mouse.y)
            var mpos = Qt.point(gpos.x - marea.pressPoint.x, gpos.y - marea.pressPoint.y)
            window.setX(mpos.x)
            window.setY(mpos.y)
        }

        onReleased: {
            if (mouse.button === Qt.LeftButton) {
                marea.pressPoint = Qt.point(0, 0)
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

    function release() {
        window.isDownload = null    // QtのBugのようだが先にBindingを切らないとエラーになる
    }
}
