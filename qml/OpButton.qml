import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Button{
    id: root
    property string operation
    property string theColor: "#2c51f5"
    property int radius: 4
    width: 50
    height: 30
    background: Rectangle{
        width: root.width
        height: root.height
        radius: root.radius
        color: theColor
        Text{
            text: operation
            color: "white"
            anchors.centerIn: parent     
        }
    }
}