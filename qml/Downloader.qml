import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
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
            font.pointSize: 13
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
