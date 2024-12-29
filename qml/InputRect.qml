import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Rectangle{
    id: root
    property string inputText
    property string outputText
    property bool readOnly_: false

    width: parent.width - 100
    height: 100
    focus: true

    Flickable{
        id: flickable
        anchors.fill: parent
        anchors.leftMargin: 20
        anchors.topMargin: 8
        anchors.rightMargin: 100
        anchors.bottomMargin: 45
        clip: true
        function ensureVisible(r){
            if(contentY >= r.y)
                contentY >= r.y 
            else if (contentY + height <= r.y + r.height)
                contentY = r.y + r.height - height
        }
        TextEdit{
            id: textInput
            text: root.outputText
            readOnly: root.readOnly_
            anchors.fill: parent
            cursorVisible: false
            wrapMode: TextEdit.Wrap
            onCursorRectangleChanged: flickable.ensureVisible(cursorRectangle)
            onEditingFinished: root.inputText = text
        }
    }
}