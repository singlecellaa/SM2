import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

RadioButton {
    id: root
    property string content
    indicator: Rectangle {
        id: rect
        width: 12; height: width; radius: width/2
        x: 7; y: 9
        color: root.checked ? "#066ed6" : "transparent"
        border.width: 1; border.color: root.checked ? "transparent":"grey"
        Rectangle {
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: 0.5
            anchors.verticalCenterOffset: 0.5
            width: rect.width * 42 / 100; height: width; radius: width/2
            color: root.checked ? "white" : "transparent"
        }
    }
    contentItem: Text{
        text: root.content
        anchors.left: rect.right
        anchors.leftMargin: 5
        renderType: Text.NativeRendering
    }
}