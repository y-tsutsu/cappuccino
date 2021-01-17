import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.3
import QtQuick.Layouts 1.0

ApplicationWindow {
    id: window

    signal accepted()
    property alias message: label.text

    width: 250
    height: 150
    minimumHeight: height
    maximumHeight: height
    minimumWidth: width
    maximumWidth: width

    visible: false
    flags: Qt.Tool

    ColumnLayout {
        anchors.fill: parent

        Label {
            id: label
            Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
            font.family: "Yu Gothic UI"
            font.pointSize: 12
        }

        RowLayout {
            id: rowLayout
            width: 100
            height: 100
            spacing: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Button {
                id: button
                text: qsTr("CANCEL")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: window.close()
            }

            Button {
                id: button1
                text: qsTr("OK")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: {
                    window.accepted()
                    window.close()
                }
            }
        }
    }

    function show() {
        window.visible = true
        window.requestActivate()
    }
}
