import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2

Item {
    signal moveItemGroups(int groupId)
    signal moveQuickDelivery()
    signal moveCardRead()

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

            // ITEM CATEGORIES FLOW
            Rectangle{
                Layout.fillHeight: true
                Layout.fillWidth: true
                color:"transparent"

                ColumnLayout{
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    RowLayout{
                        Layout.fillWidth: true
                        Layout.preferredHeight: mainColumn.height / 3

                        Rectangle{
                            Layout.preferredWidth: mainColumn.width / 2
                            Button{
                                onClicked: moveItemGroups(1)
                                background:Rectangle {
                                    border.width: control.activeFocus ? 2 : 1
                                    border.color: "orange"
                                    color: "#fff"
                                    radius: 4
                                }
                                anchors.centerIn: parent
                                height:mainColumn.height / 5
                                width: mainColumn.width / 3

                                Image {
                                    anchors.centerIn: parent
                                    sourceSize.height: mainColumn.height / 5 - 10
                                    sourceSize.width: mainColumn.width / 3 - 10
                                    fillMode: Image.Stretch
                                    source: "../asset/item-groups/helmet.jpg"
                                }
                            }
                        }

                        Rectangle{
                            Layout.preferredWidth: mainColumn.width / 2
                            Button{
                                onClicked: moveItemGroups(2)
                                background:Rectangle {
                                    border.width: control.activeFocus ? 2 : 1
                                    border.color: "orange"
                                    color: "#fff"
                                    radius: 4
                                }
                                anchors.centerIn: parent
                                height:mainColumn.height / 5
                                width: mainColumn.width / 3

                                Image {
                                    anchors.centerIn: parent
                                    sourceSize.height: mainColumn.height / 5 - 10
                                    sourceSize.width: mainColumn.width / 3 - 10
                                    fillMode: Image.Stretch
                                    source: "../asset/item-groups/glass.jpg"
                                }
                            }
                        }
                    }

                    RowLayout{
                        Layout.fillWidth: true
                        Layout.preferredHeight: mainColumn.height / 4

                        Rectangle{
                            Layout.preferredWidth: mainColumn.width / 2
                            Button{
                                onClicked: moveItemGroups(3)
                                background:Rectangle {
                                    border.width: control.activeFocus ? 2 : 1
                                    border.color: "orange"
                                    color: "#fff"
                                    radius: 4
                                }
                                anchors.centerIn: parent
                                height:mainColumn.height / 5
                                width: mainColumn.width / 3

                                Image {
                                    anchors.centerIn: parent
                                    sourceSize.height: mainColumn.height / 5 - 10
                                    sourceSize.width: mainColumn.width / 3 - 10
                                    fillMode: Image.Stretch
                                    source: "../asset/item-groups/gloves.jpg"
                                }
                            }
                        }

                        Rectangle{
                            Layout.preferredWidth: mainColumn.width / 2
                            Button{
                                onClicked: moveItemGroups(4)
                                background:Rectangle {
                                    border.width: control.activeFocus ? 2 : 1
                                    border.color: "orange"
                                    color: "#fff"
                                    radius: 4
                                }
                                anchors.centerIn: parent
                                height:mainColumn.height / 5
                                width: mainColumn.width / 3

                                Image {
                                    anchors.centerIn: parent
                                    sourceSize.height: mainColumn.height / 5 - 10
                                    sourceSize.width: mainColumn.width / 3 - 10
                                    fillMode: Image.Stretch
                                    source: "../asset/item-groups/earplugs.jpg"
                                }
                            }
                        }
                    }
                }
            }

            // VIEW ACTION BUTTONS
            Rectangle{
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color:"#22FFA500"

                // CANCEL BUTTON
                Button{
                    text: "Vazgeç"
                    onClicked: moveCardRead()
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    id:controlBack
                    font.pixelSize: 36
                    font.bold: true
                    padding: 10
                    leftPadding: 75
                    palette.buttonText: "#000000"
                    background: Rectangle {
                        border.width: controlBack.activeFocus ? 2 : 1
                        border.color: "#000000"
                        radius: 4
                        gradient: Gradient {
                            GradientStop { position: 0 ; color: controlBack.pressed ? "#888" : "#dedede" }
                            GradientStop { position: 1 ; color: controlBack.pressed ? "#dedede" : "#888" }
                        }
                    }

                    Image {
                        anchors.top: controlBack.top
                        anchors.left: controlBack.left
                        anchors.topMargin: 5
                        anchors.leftMargin: 10
                        sourceSize.width: 50
                        sourceSize.height: 50
                        fillMode: Image.Stretch
                        source: "../asset/back.png"
                    }
                }

                // QUICK DELIVERY BUTTON
                Button{
                    anchors.rightMargin:10
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    onClicked: moveQuickDelivery()
                    text: "Hızlı Ürün Al"
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
                        source: "../asset/quick-delivery.png"
                    }
                }
            }
        }
    }
}
