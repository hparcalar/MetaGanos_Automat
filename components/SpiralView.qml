import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Styles 1.0
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.0

Item {
    signal moveBack()
    signal selectSpiral(int spiralNo)

    // BACKEND SIGNALS & SLOTS
    Connections {
        target: backend

        function onGetSpirals(spirals){
            const spiralDesign = JSON.parse(spirals)
            createSpirals(spiralDesign.Rows, spiralDesign.Cols, spiralDesign.RelatedSpirals);
        }
    }

    // CHECK SPIRAL IS RELATED AND WARNING
    Timer {
        id: tmrWarning
        interval: 3000
        repeat: false
        running: false
        onTriggered: {
            warningDialog.visible = false;
        }
    }

    function clickSpiral(spiralNo, isRelated){
        if (isRelated == false){
            warningDialog.visible = true;
            tmrWarning.running = true;
        }
        else{
            selectSpiral(spiralNo)
        }
    }

    MessageDialog {
        id: warningDialog
        title: "HATALI SEÇİM"
        text: "LÜTFEN YEŞİL YANAN BÖLÜMLER İÇERİSİNDEN BİR SEÇİM YAPINIZ"
        icon: StandardIcon.Warning
        onAccepted: {
            warningDialog.visible = false;
        }
    }

    // SPIRAL CIRCLE VISUAL COMPONENT
    Component{
        id: spiralCircle

        Button{
            property string buttonText
            property int buttonSize
            property bool isRelated: false

            onClicked: clickSpiral(parseInt(this.text), isRelated)

            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: buttonSize
            Layout.preferredWidth: buttonSize

            background:Rectangle {
                border.width: 3
                border.color: "orange"
                color: isRelated ? "#32CD32" : "#DFDFDF"
                radius: width * 0.5
            }
            contentItem: Label {
                text: buttonText
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Label.Wrap
            }
            font.pixelSize: 36
            font.bold: true
            height: buttonSize
            width: buttonSize
        }
    }

    // ON LOAD EVENT
    Component.onCompleted: function(){
        backend.callSpirals()
    }

    // UI FUNCTIONS
    function createSpirals(rows, cols, relatedOnes){
        spiralFlow.rows = rows;
        spiralFlow.columns = cols;

        let minimumFit = (flowRect.height) / (rows + 1)
        let widthFit = (flowRect.width) / (cols + 1)
        if (minimumFit > widthFit)
            minimumFit = widthFit

        for (let i = 0; i < rows * cols; i++) {
            spiralCircle.createObject(spiralFlow, { 
                buttonText: (i + 1).toString(),
                buttonSize: minimumFit,
                isRelated: relatedOnes.some(m => m == (i + 1))
            });
        }
    }

    // VIEW LAYOUT
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
                    }

                }
            }

            // SELECTED ITEM TEXT
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
                    text: "ELDİVEN A 24x24 LARGE"
                }
            }

            // MACHINE SPIRALS FLOW
            Rectangle{
                id: flowRect
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "transparent"

                GridLayout{
                    id: spiralFlow
                    width: parent.width
                    columns:1
                    rows:1
                    columnSpacing:5
                    rowSpacing:10
                    anchors.topMargin:10
                    anchors.top: parent.top
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

                Rectangle{
                    id: itemRationInfo
                    width: parent.width / 3
                    anchors.rightMargin:10
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 5
                    Layout.alignment: Qt.AlignRight

                    ColumnLayout{
                        Text {
                            width: itemRationInfo.width
                            horizontalAlignment: Text.AlignRight
                            color:"#ddd"
                            padding: 2
                            font.pixelSize: 22
                            style: Text.Outline
                            styleColor:'black'
                            font.bold: true
                            text: "Aylık İstihkak: 12"
                        }

                        Text {
                            width: itemRationInfo.width
                            horizontalAlignment: Text.AlignRight
                            color:"#ddd"
                            padding: 2
                            font.pixelSize: 22
                            style: Text.Outline
                            styleColor:'black'
                            font.bold: true
                            text: "Kalan: 4"
                        }
                    }
                }
            }
        }
    }
}
