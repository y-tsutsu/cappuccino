import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.3
import QtQuick.Layouts 1.0

ToolTip {
    id: tool_tip

    signal accepted()
    property alias message: label.text

    width: 250
    height: 150
    modal: true
    focus: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

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
            spacing: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Button {
                id: buttonCancel
                text: qsTr("CANCEL")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: tool_tip.close()
            }

            Button {
                id: buttonOk
                text: qsTr("OK")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: {
                    tool_tip.accepted()
                    tool_tip.close()
                }
            }
        }
    }

    function show(parentSize) {
        tool_tip.x = (parentSize.width - tool_tip.width) / 2
        tool_tip.y = (parentSize.height - tool_tip.height) / 2
        tool_tip.visible = true
    }
}
