import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

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
        Row{
            spacing: 15
            MyRadioButton{id: enc_radio_button; content: "加密"; checked: true}
            MyRadioButton{id: dec_radio_button; content: "解密"}
        }
        Row{
            width: parent.width; height: 200
            // 参数
            Column{
                id: parameter_column
                width: parent.width / 2 - 100; height: 200
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
                    }
                    delegate: Row{
                        spacing: 10
                        height: 10
                        NativeText{text: model.name; width: 20}
                        MyTextInput{text_: model.content; radius: 2}
                    }
                }
            }
            // 文件路径
            Column{
                id: file_path_column
                width: parent.width / 2; height: 200
                Row{
                    id: intput_row
                    spacing: 5
                    NativeText{text: "输入路径"; y:2 }
                    MyTextInput{
                        id: input_path_textInput; width: 200; height: 20; y: 2
                        readOnly_: true
                    }
                    Button{
                        width: 30; height: 25
                        Icon{id: file_button_icon; icon_: "file_icon.png"; anchors.verticalCenter: parent.verticalCenter; x: 5; width: 20}
                        onClicked: fileDialog.open()
                    }
                    FileDialog{
                        id: fileDialog
                        title: "select a file"
                        onAccepted: {
                            input_path_textInput.text_ = String(selectedFile).substring(8)
                            backend.get_input_filepath(selectedFile)
                        }
                    }
                }
                Row{
                    id: output_row
                    spacing: 5
                    NativeText{text: "输出路径"; y:2 }
                    MyTextInput{
                        id: output_path_textInput; width: 200; height: 20; y: 2; text_: backend.output_path
                    }
                }
            }
        }
        NativeText{text: enc_radio_button.checked ? "输入（明文）" : "输入（密文）"}
        InputRect{id: input_rect; x: 20; radius: 5; text_: backend.input_content}
        NativeText{text: enc_radio_button.checked ? "输出（密文）" : "输出（明文）"}
        InputRect{id: output_rect; x: 20; radius: 5; text_: backend.output_content}
        OpButton{
            id: button
            width: 80
            height: 25
            operation: "处理"
            theColor: "#438cfa"
            x: main_column.width - width - 80
            y: main_column.height - height - 20
            onClicked: {
                backend.get_enc_or_dec_choice(dec_radio_button.checked)
                backend.start_process()
            }
        }
    }
}