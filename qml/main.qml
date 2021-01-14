import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12

ApplicationWindow {
    id: window
    visible: false
    minimumWidth: 250
    minimumHeight: 150
    title: qsTr("Hello World")
    flags: Qt.Window | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint

    Material.theme: Material.Light
    Material.accent: Material.Purple

    Page {
        id: downloader
        visible: true
        anchors.fill: parent

        Control {
            id: downloaderControl
            width: parent.width
            height: 60
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            Label {
                id: downloaderLabel
                text: qsTr("カプチーノを入れています．．．")
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.family: "Yu Gothic UI"
                font.pointSize: 16
            }

            ProgressBar {
                id: downloaderProgressBar
                width: parent.width * 0.8
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                value: 0.5
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
