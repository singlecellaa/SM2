import QtQuick
import QtQuick.Controls

ApplicationWindow{
    id: root 
    width: 600
    height: 800
    maximumWidth: 600; minimumWidth: 600
    maximumHeight: 800; minimumHeight: 800
    visible: true
    title: "SM2 软件加密系统"
    Rectangle{
        anchors.fill: parent
        color: "lightGrey"
    }
    Column{
        id: main_column
        x: root.width / 2 - input_rect.width / 2 - 20; y: 40
        spacing: 20
        width: parent.width
        Column{
            id: parameter_column
            width: parent.width; height: 200
            ListView{
                id: parameter_listview
                width: parent.width; height: parent.height
                spacing: 18
                model: ListModel{
                    id: parameter_model
                    ListElement{name: "p"; content: ""}
                    ListElement{name: "a"; content: ""}
                    ListElement{name: "b"; content: ""}
                    ListElement{name: "G"; content: ""}
                    ListElement{name: "n"; content: ""}
                    ListElement{name: "h"; content: ""}
                    ListElement{name: "公钥/私钥"; content: ""}
                }
                delegate: Row{
                    spacing: 10
                    height: 10
                    NativeText{text: model.name; width: 60}
                    MyTextInput{text_: model.content; radius: 2}
                }
            }
        }
        NativeText{text: "输入（明文/密文)"}
        InputRect{id: input_rect; x: 20; radius: 5}
        NativeText{text: "输出（密文/明文）"}
        InputRect{id: output_rect; x: 20; radius: 5; readOnly_: true}
        OpButton{
            id: button
            width: 80
            height: 25
            operation: "处理"
            theColor: "#438cfa"
            x: main_column.width - width - 80
            y: main_column.height - height - 20
            onClicked: {
                output_rect.outputText = input_rect.inputText
            }
        }
    }
}