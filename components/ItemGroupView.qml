import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.0

Item {
    signal moveBack()
    signal showGroupDetail(int groupId)

    Rectangle{
        anchors.fill: parent
        color: "#333333"

        ColumnLayout{
            id: mainColumn
            anchors.fill: parent
            spacing:5

            Rectangle{
                Layout.preferredHeight: 170
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop

                gradient: Gradient
                {
                    GradientStop {position: 0.000;color: "#c8cacc";}
                    GradientStop {position: 1.000;color: "#333";}
                }

                ColumnLayout{
                    anchors.left: parent.left
                    anchors.right: parent.right

                    // #region USER INFORMATION
                    Text {
                        Layout.fillWidth: true
                        horizontalAlignment: Text.AlignHCenter
                        color:"#333"
                        padding: 2
                        font.pixelSize: 48
                        style: Text.Outline
                        styleColor:'orange'
                        font.bold: true
                        text: "Ahmet Yılmaz"
                    }

                    Text {
                        Layout.fillWidth: true
                        horizontalAlignment: Text.AlignHCenter
                        color:"#ddd"
                        padding: 2
                        font.pixelSize: 36
                        style: Text.Outline
                        styleColor:'black'
                        font.bold: false
                        text: "Bölüm: Boyahane"
                    }

                    Text {
                        Layout.fillWidth: true
                        horizontalAlignment: Text.AlignHCenter
                        color:"#ddd"
                        padding: 2
                        font.pixelSize: 36
                        style: Text.Outline
                        styleColor:'black'
                        font.bold: false
                        text: "Sicil: 19867"
                    }
                    // #endregion
                }
            }

            // SELECTED ITEM CATEGORY TEXT
            Rectangle{
                Layout.fillWidth: true
                Layout.preferredHeight:60
                color:"orange"
                Text {
                    width: parent.width
                    horizontalAlignment: Text.AlignHCenter
                    color:"#333"
                    padding: 2
                    font.pixelSize: 48
                    style: Text.Outline
                    styleColor:'#fff'
                    font.bold: true
                    text: "ELDİVEN"
                }
            }

            // ITEM GROUP ITEMS FLOW
            Rectangle{
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "transparent"

                Flow{
                    width: parent.width
                    padding: 10
                    spacing: 10

                    Button{
                        onClicked: showGroupDetail(1)
                        background:Rectangle {
                            border.width: 1
                            border.color: "orange"
                            color: "#fff"
                            radius: 4
                        }
                        contentItem: Label {
                            text:"Eldiven Marka 1"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            wrapMode: Label.Wrap
                        }
                        font.pixelSize: 36
                        font.bold: true
                        height:mainColumn.height / 5
                        width: mainColumn.width / 4

                        Image {
                            anchors.centerIn: parent
                            sourceSize.height: mainColumn.height / 5 - 10
                            sourceSize.width: mainColumn.width / 4 - 10
                            fillMode: Image.Stretch
                            source: "../asset/item-groups/gloves.jpg"
                        }
                    }

                    Button{
                        onClicked: showGroupDetail(2)
                        background:Rectangle {
                            border.width: 1
                            border.color: "orange"
                            color: "#fff"
                            radius: 4
                        }
                        contentItem: Label {
                            text:"Eldiven Marka 2"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            wrapMode: Label.Wrap
                        }
                        font.pixelSize: 36
                        font.bold: true
                        height:mainColumn.height / 5
                        width: mainColumn.width / 4

                        Image {
                            anchors.centerIn: parent
                            sourceSize.height: mainColumn.height / 5 - 10
                            sourceSize.width: mainColumn.width / 4 - 10
                            fillMode: Image.Stretch
                            source: "../asset/item-groups/gloves.jpg"
                        }
                    }
                }
            }

            // VIEW ACTION BUTTONS
            Rectangle{
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color:"#22FFA500"

                Button{
                    text: "Geri"
                    onClicked: moveBack()
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    id:control
                    font.pixelSize: 36
                    font.bold: true
                    padding: 10
                    leftPadding: 75
                    palette.buttonText: "#fa6000"
                    background: Rectangle {
                        border.width: control.activeFocus ? 2 : 1
                        border.color: "orange"
                        radius: 4
                        gradient: Gradient {
                            GradientStop { position: 0 ; color: control.pressed ? "#fac77a" : "#dedede" }
                            GradientStop { position: 1 ; color: control.pressed ? "#dedede" : "#fac77a" }
                        }
                    }

                    Image {
                        anchors.top: control.top
                        anchors.left: control.left
                        anchors.topMargin: 5
                        anchors.leftMargin: 10
                        sourceSize.width: 50
                        sourceSize.height: 50
                        fillMode: Image.Stretch
                        source: "../asset/back.png"
                    }
                }
            }
        }
    }
}
