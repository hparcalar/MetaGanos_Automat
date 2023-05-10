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

    property bool spiralIsProcessing: false
    property bool creditsVisible: true
    property var selectedSpiralObject: null

    // BACKEND SIGNALS & SLOTS
    Connections {
        target: backend

        function onGetUserData(userStr){
            var userData = JSON.parse(userStr);
            if (userData){
                // txtUserCode.text = 'Sicil: ' + userData['employeeCode'];
                txtUserName.text = userData['employeeName'];
                txtDepartmentName.text = userData['departmentName'];
            }
        }

        function onGetProperSpirals(spirals){
            const spiralDesign = JSON.parse(spirals);
            txtItemName.text = spiralDesign['ItemName'];
            createSpirals(spiralDesign.Rows, spiralDesign.Cols, spiralDesign.RelatedSpirals, spiralDesign.AllSpirals);
        }

        function onResponseCreditsVisible(isCreditsVisible){
            creditsVisible = isCreditsVisible;
        }

        function onGetActiveCredit(creditInfo){
            if (creditInfo){
                const creditObj = JSON.parse(creditInfo);

                const rangeObj = creditObj['CreditRange'];
                if (rangeObj && rangeObj['RangeType'].length > 0){
                    txtRangeOfCredit.text = rangeObj['RangeType'] + ' İstihkak: ' + rangeObj['RangeCredit'];
                    pnlRangeOfCredit.visible = true;
                }
                else
                    pnlRangeOfCredit.visible = false;

                txtRemainingCredit.text = 'Kalan İstihkak: ' + creditObj['ActiveCredit'].toString();
            }
        }

        function onGetPushSpiralResult(spiralInfo){
            spiralIsProcessing = false;
        }
    }

    function clickSpiral(spiralNo, isRelated){
        spiralIsProcessing = true;
        if (isRelated == false){
            warningDialog.visible = true;
            tmrWarning.running = true;
        }
        else{
            selectSpiral(spiralNo)
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

    MessageDialog {
        id: warningDialog
        title: "HATALI SEÇİM"
        text: "LÜTFEN YEŞİL YANAN BÖLÜMLER İÇERİSİNDEN BİR SEÇİM YAPINIZ"
        icon: StandardIcon.Warning
        onAccepted: {
            warningDialog.visible = false;
        }
    }   

    // PUSH ITEM ERROR DIALOG
    Timer {
        id: tmrPushError
        interval: 3000
        repeat: false
        running: false
        onTriggered: {
            pushErrorDialog.visible = false;
        }
    }

    Timer { id: tmrSpiral }

    MessageDialog {
        id: pushErrorDialog
        title: "İLETİŞİM HATASI"
        text: "ÜRÜN TESLİM EDİLEMEDİ"
        icon: StandardIcon.Warning
        onAccepted: {
            pushErrorDialog.visible = false;
        }
    }

    // SPIRAL CIRCLE DYNAMIC COMPONENT
    Component{
        id: spiralCircle

        Button{
            property string buttonText
            property int buttonSize
            property bool isRelated: false

            onClicked: function(){
                this.enabled = false
                selectedSpiralObject = this;
                clickSpiral(parseInt(buttonText), isRelated)
                tmrSpiral.interval = 3000 
                tmrSpiral.triggered.connect(callback)
                tmrSpiral.start()
            }

            function callback(event) {
                tmrSpiral.triggered.disconnect(callback)
                if (selectedSpiralObject != null)
                    selectedSpiralObject.enabled = true
            }

            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: buttonSize
            Layout.preferredWidth: buttonSize

            background:Rectangle {
                border.width: 3
                border.color: isRelated ? "orange" : "transparent"
                color: isRelated ? "#32CD32" : "transparent"
                radius: width * 0.5
            }
            contentItem: Label {
                text: isRelated ? buttonText : ""
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Label.Wrap
                fontSizeMode: Text.Fit
            }
            // enabled: !spiralIsProcessing
            font.bold: true
            height: buttonSize
            width: buttonSize
        }
    }

    // ON LOAD EVENT
    Component.onCompleted: function(){
        backend.requestCreditsVisible();
        backend.requestUserData()
        backend.requestProperSpirals()
        backend.requestActiveCredit()
    }

    // UI FUNCTIONS
    function createSpirals(rows, cols, relatedOnes, allSpirals){
        spiralFlow.rows = rows;
        spiralFlow.columns = cols;

        let minimumFit = (flowRect.height) / (rows + 1)
        let widthFit = (flowRect.width) / (cols + 1)
        if (minimumFit > widthFit)
            minimumFit = widthFit

        let spiralIndex = 0;
        for (let i = 0; i < rows * cols; i++) {
            try {
                var spiralData = allSpirals[spiralIndex];
                spiralCircle.createObject(spiralFlow, { 
                    buttonText: spiralData['posOrders'].toString(),
                    buttonSize: minimumFit,
                    isRelated: relatedOnes.some(m => parseInt(m['posOrders']) == parseInt(spiralData['posOrders']))
                });
            } catch (error) {
                
            }
            spiralIndex++;
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
                            visible: false
                        }
                        // #endregion
                    }

                }
            }

            // SELECTED ITEM TEXT
            Rectangle{
                Layout.fillWidth: true
                Layout.preferredHeight:60
                color:"orange"
                Text {
                    id: txtItemName
                    width: parent.width
                    horizontalAlignment: Text.AlignHCenter
                    color:"#333"
                    padding: 2
                    font.pixelSize: 48
                    style: Text.Outline
                    styleColor:'#fff'
                    font.bold: true
                    text: ""
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

            // CREDIT INFORMATION PANEL
            Rectangle{
                visible: creditsVisible
                id: pnlRangeOfCredit
                Layout.fillWidth: true
                Layout.preferredHeight: creditsVisible ? 60 : 0
                color:"#c8cacc"

                Text {
                    visible: creditsVisible
                    id: txtRangeOfCredit
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color:"#333"
                    padding: 2
                    // font.pixelSize: 48
                    font.pointSize: 36
                    font.bold: true
                    fontSizeMode: Text.Fit
                    style: Text.Outline
                    styleColor:'#fff'
                    text: "Aylık İstihkak: 20"
                }
            }

            Rectangle{
                visible: creditsVisible
                Layout.fillWidth: true
                Layout.preferredHeight: creditsVisible ? 60 : 0
                color:"#52c908"

                Text {
                    visible: creditsVisible
                    id: txtRemainingCredit
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color:"#333"
                    padding: 2
                    // font.pixelSize: 48
                    font.pointSize: 36
                    font.bold: true
                    fontSizeMode: Text.Fit
                    style: Text.Outline
                    styleColor:'#fff'
                    text: "Kalan: "
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
