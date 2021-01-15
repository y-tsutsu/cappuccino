import QtQuick 2.12
import QtQuick.Window 2.14
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
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

        ColumnLayout {
            width: parent.width
            height: 60
            spacing: 20
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            Label {
                id: downloaderLabel
                text: qsTr("カプチーノを入れています．．．")
                font.family: "Yu Gothic UI"
                font.pointSize: 16
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            ProgressBar {
                id: downloaderProgressBar
                value: 0.5
                Layout.fillWidth: true
                Layout.rightMargin: 20
                Layout.leftMargin: 20
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
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
