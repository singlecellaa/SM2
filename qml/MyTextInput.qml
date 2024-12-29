import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Rectangle{
    id: root
    width: 100
    height: 25
    clip: true
    property string text_: ""
    property var wrap_mode: TextInput.NoWrap
    // color: "transparent"
    border.width: 0.5; border.color: "white"
    TextInput{
        id: textInput 
        anchors.fill: parent
        text: text_
        wrapMode: wrap_mode
    }
    Rectangle{
        anchors.bottom: parent.bottom
        height: textInput.activeFocus ? 2 : 0.8
        width: parent.width
        color: textInput.activeFocus ? "#066ed6" : "grey"
    }
}