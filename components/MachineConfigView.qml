import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Styles 1.0
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.0

Item {
    signal completed()
    signal moveServiceView()

    // BACKEND SIGNALS & SLOTS
    Connections {
        target: backend

        function onConfigSaved(result){
            if (result)
                completed();
            else
                warningDialog.visible = true;
        }

        function onGetMachineConfig(result){
            if (result){
                var configObj = JSON.parse(result);
                txtMachineCode.text = configObj['Code'];
                txtApiAddr.text = configObj['ApiAddr'];
                if (configObj['ModbusType'] == 'RTU')
                    cmbModbusType.incrementCurrentIndex();
                txtModbusServerAddr.text = configObj['ModbusServerAddr'];
                txtDealerCode.text = configObj['DealerCode'];
                txtPlantCode.text = configObj['PlantCode'];
            }
        }
    }

    // UI FUNCTIONS
    function trySave(){
        backend.saveMachineConfig(JSON.stringify({
            machineCode: txtMachineCode.text,
            apiAddr: txtApiAddr.text,
            modbusType: cmbModbusType.currentValue,
            modbusServerAddr: txtModbusServerAddr.text,
            dealerCode: txtDealerCode.text,
            plantCode: txtPlantCode.text,
        }));
    }

    function closeApp(){
        backend.closeApp();
    }

    MessageDialog {
        id: warningDialog
        title: "UYARI"
        text: "LÜTFEN KONFİGÜRASYON BİLGİLERİNİ EKSİKSİZ DOLDURUNUZ."
        icon: StandardIcon.Warning
        onAccepted: {
            warningDialog.visible = false;
        }
    }

    // ON LOAD EVENT
    Component.onCompleted: function(){
        backend.requestMachineConfig()
    }

    // VIEW LAYOUT
    Rectangle{
        anchors.fill: parent
        color: "#333333"

        ColumnLayout{
            id: mainColumn
            anchors.fill: parent
            spacing:5

            // HEADER TEXT
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
                    text: "MAKİNE BAŞLANGIÇ AYARLARI"
                }
            }

            // CONFIGURATION FORM
            Rectangle{
                id: flowRect
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "transparent"

                RowLayout{
                    anchors.fill: parent

                    Rectangle{
                        Layout.preferredWidth: parent.width / 2
                        Layout.fillHeight: true
                        color:"transparent"

                        ColumnLayout{
                            anchors.fill: parent
                            spacing:0

                            // machine code
                            Rectangle{
                                Layout.alignment: Qt.AlignTop
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: "transparent"

                                RowLayout{
                                    anchors.fill: parent
                                    Label {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        horizontalAlignment: Qt.AlignRight
                                        text: "Makine Kodu: "
                                        color: "#FFF"
                                        font.pixelSize: 24
                                    }

                                    TextField {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        id: txtMachineCode
                                        font.pixelSize: 24
                                        horizontalAlignment: Qt.AlignLeft
                                        onFocusChanged: function(){
                                            backend.requestOsk(focus);
                                        }
                                    }
                                }
                            }

                            // api address
                            Rectangle{
                                Layout.alignment: Qt.AlignTop
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: "transparent"

                                RowLayout{
                                    anchors.fill: parent
                                    Label {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        horizontalAlignment: Qt.AlignRight
                                        text: "Api Adresi: "
                                        color: "#FFF"
                                        font.pixelSize: 24
                                    }

                                    TextField {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        id: txtApiAddr
                                        font.pixelSize: 24
                                        horizontalAlignment: Qt.AlignLeft
                                        onFocusChanged: function(){
                                            backend.requestOsk(focus);
                                        }
                                    }
                                }
                            }

                            // modbus type
                            Rectangle{
                                Layout.alignment: Qt.AlignTop
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: "transparent"

                                RowLayout{
                                    anchors.fill: parent
                                    Label {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        horizontalAlignment: Qt.AlignRight
                                        text: "Haberleşme Türü: "
                                        color: "#FFF"
                                        font.pixelSize: 24
                                    }

                                    ComboBox {
                                        id: cmbModbusType
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        
                                        font.pixelSize: 24
                                        model: ListModel {
                                            ListElement { text: "TCP" }
                                            ListElement { text: "RTU" }
                                        }
                                    }
                                }
                            }

                            // modbus server address
                            Rectangle{
                                Layout.alignment: Qt.AlignTop
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: "transparent"

                                RowLayout{
                                    anchors.fill: parent
                                    Label {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        horizontalAlignment: Qt.AlignRight
                                        text: "Server Adresi: "
                                        color: "#FFF"
                                        font.pixelSize: 24
                                    }

                                    TextField {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        id: txtModbusServerAddr
                                        font.pixelSize: 24
                                        horizontalAlignment: Qt.AlignLeft
                                        onFocusChanged: function(){
                                            backend.requestOsk(focus);
                                        }
                                    }
                                }
                            }

                            // dealer code
                            Rectangle{
                                Layout.alignment: Qt.AlignTop
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: "transparent"

                                RowLayout{
                                    anchors.fill: parent
                                    Label {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        horizontalAlignment: Qt.AlignRight
                                        text: "Bayi Kodu: "
                                        color: "#FFF"
                                        font.pixelSize: 24
                                    }

                                    TextField {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        id: txtDealerCode
                                        font.pixelSize: 24
                                        horizontalAlignment: Qt.AlignLeft
                                        onFocusChanged: function(){
                                            backend.requestOsk(focus);
                                        }
                                    }
                                }
                            }

                            // plant code
                            Rectangle{
                                Layout.alignment: Qt.AlignTop
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: "transparent"

                                RowLayout{
                                    anchors.fill: parent
                                    Label {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        horizontalAlignment: Qt.AlignRight
                                        text: "Fabrika Kodu: "
                                        color: "#FFF"
                                        font.pixelSize: 24
                                    }

                                    TextField {
                                        Layout.preferredWidth: parent.width / 2 - 30
                                        id: txtPlantCode
                                        font.pixelSize: 24
                                        horizontalAlignment: Qt.AlignLeft
                                        onFocusChanged: function(){
                                            backend.requestOsk(focus);
                                        }
                                    }
                                }
                            }

                            // empty view buffer
                            Rectangle{
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                color: "transparent"
                            }
                        }
                    }

                    // right part of the form for empty slots
                    Rectangle{
                        Layout.preferredWidth: parent.width / 2
                        Layout.fillHeight: true
                        color:"transparent"

                        ColumnLayout{
                            anchors.fill: parent

                            // empty view buffer
                            Rectangle{
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                color: "transparent"
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

                 // GOTO SERVICE BUTTON
                Button{
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    onClicked: moveServiceView()
                    text: "SERVİS"
                    id:serviceButton
                    font.pixelSize: 36
                    font.bold: true
                    padding: 10
                    palette.buttonText: "#fefefe"
                    background: Rectangle {
                        border.width: serviceButton.activeFocus ? 2 : 1
                        border.color: "green"
                        radius: 4
                        gradient: Gradient {
                            GradientStop { position: 0 ; color: serviceButton.pressed ? "blue" : "#dedede" }
                            GradientStop { position: 1 ; color: serviceButton.pressed ? "#dedede" : "blue" }
                        }
                    }
                }

                // CLOSE BUTTON
                Button{
                    anchors.centerIn: parent
                    onClicked: closeApp()
                    text: "ÇIKIŞ"
                    id:controlClose
                    font.pixelSize: 36
                    font.bold: true
                    padding: 10
                    palette.buttonText: "#fefefe"
                    background: Rectangle {
                        border.width: controlClose.activeFocus ? 2 : 1
                        border.color: "green"
                        radius: 4
                        gradient: Gradient {
                            GradientStop { position: 0 ; color: controlClose.pressed ? "red" : "#dedede" }
                            GradientStop { position: 1 ; color: controlClose.pressed ? "#dedede" : "red" }
                        }
                    }
                }

                // CONFIRM BUTTON
                Button{
                    anchors.rightMargin:10
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    onClicked: trySave()
                    text: "KAYDET"
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
