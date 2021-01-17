import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: item
    anchors.fill: parent

    property string image_url: imodel.image_url

    Image {
        id: image
        anchors.fill: parent
        source: item.image_url
        fillMode: Image.PreserveAspectFit
    }

    onVisibleChanged: {
        if (item.visible) {
            imodel.start_view()
        }
    }

    function release() {
        image_url = null
    }
}
