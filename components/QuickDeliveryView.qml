import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Styles 1.0
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.0

Item {
    signal moveBack()
    signal confirmQuickDelivery(int spiralNo)

    function spiralPadPressed(padValue){
        if (padValue == '-'){
            if (txtSpiralNo.text.length > 0)
                txtSpiralNo.text = txtSpiralNo.text.substr(0, txtSpiralNo.text.length - 1);
        }
        else
            txtSpiralNo.text += padValue;
    }

    // ON LOAD EVENT
    Component.onCompleted: function(){
        backend.requestUserData()
    }

    // BACKEND SIGNALS & SLOTS
    Connections {
        target: backend

        function onGetUserData(userStr){
            var userData = JSON.parse(userStr);
            if (userData){
                txtUserCode.text = 'Sicil: ' + userData['employeeCode'];
                txtUserName.text = userData['employeeName'];
                txtDepartmentName.text = userData['departmentName'];
            }
        }
    }

    Component{
        id: numpadStyle
        Rectangle {
            implicitWidth: 100
            implicitHeight: 25
            border.width: 2
            border.color: "#fa6000"
            radius: 4
            color: "orange"
        }
    }

    Rectangle{
        anchors.fill: parent
        color: "#333333"

        ColumnLayout{
            id: mainColumn
            anchors.fill: parent
            spacing:5

            // USER INFORMATION PANEL
            Rectangle{
                Layout.preferredHeight: 170
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop

                gradient: Gradient
                {
                    GradientStop {position: 0.000;color: "#c8cacc";}
                    GradientStop {position: 1.000;color: "#333";}
                }

                GridLayout{
                    anchors.left: parent.left
                    anchors.right: parent.right
                    rows: 1
                    columns: 1
                    
                    ColumnLayout{
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredWidth: parent.width / 3 - 20
                        
                        // #region USER INFORMATION
                        Text {
                            id: txtUserName
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignHCenter
                            color:"#333"
                            padding: 2
                            font.pixelSize: 48
                            style: Text.Outline
                            styleColor:'orange'
                            font.bold: true
                            text: ""
                        }

                        Text {
                            id: txtDepartmentName
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignHCenter
                            color:"#ddd"
                            padding: 2
                            font.pixelSize: 36
                            style: Text.Outline
                            styleColor:'black'
                            font.bold: false
                            text: ""
                        }

                        Text {
                            id: txtUserCode
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignHCenter
                            color:"#ddd"
                            padding: 2
                            font.pixelSize: 36
                            style: Text.Outline
                            styleColor:'black'
                            font.bold: false
                            text: ""
                        }
                        // #endregion
                    }

                }
            }

            // QUICK DELIVERY TITLE
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
                    text: "HIZLI ÜRÜN AL"
                }
            }

            // QUICK INTERACTION PANEL
            Rectangle{
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "transparent"

                ColumnLayout{
                    width: parent.width
                    height: parent.height

                    // SPIRAL NO INPUT TEXT FIELD
                    Rectangle{
                        Layout.fillWidth: true
                        Layout.preferredHeight: 100
                        color: "transparent"

                        RowLayout{
                            anchors.centerIn: parent
                            Label {
                                
                                horizontalAlignment: Qt.AlignHCenter
                                text: "Spiral No: "
                                color: "#FFF"
                                font.pixelSize: 38
                            }

                            TextField {
                                id: txtSpiralNo
                                font.pixelSize: 38
                                horizontalAlignment: Qt.AlignLeft
                            }
                        }
                    }

                    // SPIRAL NUMPAD
                    Rectangle{
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "transparent"

                        Grid {
                            anchors.centerIn: parent
                            columns: 3
                            columnSpacing: 16
                            rowSpacing: 16

                            signal buttonPressed

                            Button { 
                                text: "1"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "2"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "3"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "4"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "5"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "6"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "7"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "8"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                text: "9"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { text: " "; background: Rectangle{ color:"transparent" } font.pixelSize: 24; font.bold: true; padding: 30 }
                            Button { 
                                text: "0"
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()
                                onClicked: spiralPadPressed(this.text)
                            }
                            Button { 
                                id: btnBackspace
                                text: " "
                                font.pixelSize: 24
                                font.bold: true
                                padding: 30
                                background: numpadStyle.createObject()

                                Image {
                                    anchors.centerIn: parent
                                    sourceSize.width: parent.width / 2
                                    sourceSize.height: parent.width / 2
                                    fillMode: Image.Stretch
                                    source: "../asset/backspace.png"
                                }
                                onClicked: spiralPadPressed('-')
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

                // MOVE BACK BUTTON
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

                // CONFIRM DELIVERY BUTTON
                Button{
                    anchors.rightMargin:10
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    onClicked: confirmQuickDelivery(parseInt(txtSpiralNo.text))
                    text: "OK"
                    id:controlConfirm
                    font.pixelSize: 36
                    font.bold: true
                    padding: 10
                    leftPadding: 75
                    palette.buttonText: "#fefefe"
                    background: Rectangle {
                        border.width: controlConfirm.activeFocus ? 2 : 1
                        border.color: "green"
                        radius: 4
                        gradient: Gradient {
                            GradientStop { position: 0 ; color: controlConfirm.pressed ? "green" : "#dedede" }
                            GradientStop { position: 1 ; color: controlConfirm.pressed ? "#dedede" : "green" }
                        }
                    }

                    Image {
                        anchors.top: controlConfirm.top
                        anchors.left: controlConfirm.left
                        anchors.topMargin: 5
                        anchors.leftMargin: 10
                        sourceSize.width: 50
                        sourceSize.height: 50
                        fillMode: Image.Stretch
                        source: "../asset/ok.png"
                    }
                }
            }
        }
    }
}
