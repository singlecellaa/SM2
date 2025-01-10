import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Rectangle{
    id: root
    property string text_

    width: parent.width - 100
    height: 200
    focus: true

    Flickable{
        id: flickable
        anchors.fill: parent
        anchors.leftMargin: 20; anchors.rightMargin: 20
        anchors.topMargin: 10; anchors.bottomMargin: 10
        clip: true
        function ensureVisible(r){
            if(contentY >= r.y)
                contentY >= r.y 
            else if (contentY + height <= r.y + r.height)
                contentY = r.y + r.height - height
        }
        TextEdit{
            id: textInput
            text: root.text_
            readOnly: true
            anchors.fill: parent
            cursorVisible: false
            wrapMode: TextEdit.Wrap
            onCursorRectangleChanged: flickable.ensureVisible(cursorRectangle)
        }
    }
}