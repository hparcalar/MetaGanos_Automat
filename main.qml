import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtMultimedia 5.12
import QtQuick.Dialogs 1.1
import "components"

ApplicationWindow {
    width: screen.desktopAvailableWidth
    height: screen.desktopAvailableHeight
    flags: Qt.WindowMaximized | Qt.FramelessWindowHint | Qt.Window
    visible: true
    title: qsTr("MetaGanos Otomat")
    onClosing: function(){
        backend.appIsClosing();
        return true;
    }

    // LOGIN WARNING MESSAGE
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
        title: "HATALI GİRİŞ"
        text: "KART BİLGİLERİNİZ GEÇERLİ DEĞİL"
        icon: StandardIcon.Warning
        onAccepted: {
            warningDialog.visible = false;
        }
    }

    // SPIRAL PUSH ERROR MESSAGE
    Timer {
        id: tmrPushError
        interval: 3000
        repeat: false
        running: false
        onTriggered: {
            pushErrorDialog.visible = false;
        }
    }

    MessageDialog {
        id: pushErrorDialog
        title: "HATA"
        text: ""
        icon: StandardIcon.Warning
        onAccepted: {
            pushErrorDialog.visible = false;
        }
    }

    // BACKEND SIGNALS & SLOTS
    Connections {
        target: backend

        function onCheckConfigResult(result){
            if (!result)
            {
                stack.replace(cardRead, machineConfig)
            }
        }

        function onCardLoggedIn(result){
            if (result){
                stack.replace(cardRead, userHome)
            }
            else{
                warningDialog.visible = true;
                tmrWarning.running = true;
            }
        }

        function onServiceScreenRequested(){
            stack.replace(stack.currentItem, serviceView)
        }

        function onGetPushSpiralResult(spiralInfo){
            var pushResult = JSON.parse(spiralInfo);
            if (pushResult.Result == true){
                popupLoading.close();
                stack.replace(stack.currentItem, endDelivery)
            }
            else
            {
                txtProcessResult.text = pushResult.ErrorMessage;
                // pushErrorDialog.text = pushResult.ErrorMessage;
                // pushErrorDialog.visible = true;
                // tmrPushError.running = true;
            }
        }
    }

    // ON LOAD EVENTS & UI FUNCTIONS
    Component.onCompleted: function(){
        backend.checkMachineConfig()
        //keyListenerRect.focus();
    }

    function showConfigView(){
        stack.replace(stack.currentItem, machineConfig)
    }

    Timer {
        id: tmrDelayHandler
    }

    function delay(delayTime, cb) {
        tmrDelayHandler.stop();
        tmrDelayHandler.interval = delayTime;
        tmrDelayHandler.repeat = false;
        tmrDelayHandler.triggered.connect(cb);
        tmrDelayHandler.start();
    }

    // COMPONENT DECLARATIONS

    // MACHINE CONFIG VIEW
    Component{
        id:machineConfig
        MachineConfigView{
            onCompleted: function(){
                stack.replace(machineConfig, cardRead)
            }
            onMoveServiceView: function(){
                stack.replace(stack.currentItem, serviceView);
            }
        }
    }

    // SERVICE VIEW
    Component{
        id:serviceView
        ServiceView{
            onMoveBack: function(){
                stack.replace(serviceView, cardRead)
            }
        }
    }

    // CARD READ & VIDEO VIEW
    Component{
        id:cardRead
        CardReadView{
            view: stack
            onMoveNextStep: function(){
                backend.cardReading('0477467401049');
                // stack.replace(cardRead, userHome)
            }
        }
    }

    // USER HOME VIEW
    Component{
        id:userHome
        UserHomeView{
            onMoveItemGroups: function(categoryId){
                backend.storeSelectedItemCategory(categoryId)
                stack.replace(userHome, itemGroups)
            }
            onMoveQuickDelivery: function(){
                stack.replace(userHome, quickDelivery)
            }
            onMoveCardRead: function(){
                stack.replace(userHome, cardRead)
            }
        }
    }

    // ITEM GROUPS VIEW
    Component{
        id:itemGroups
        ItemGroupView{
            onMoveBack: function(){
                stack.replace(itemGroups, userHome)
            }
            onShowGroupDetail: function(groupId){
                backend.storeSelectedItemGroup(groupId)
                stack.replace(itemGroups, itemsView)
            }
        }
    }

    // ITEMS VIEW
    Component{
        id: itemsView
        ItemView{
            onMoveBack: function(){
                stack.replace(itemsView, itemGroups)
            }
            onMoveSpiralView: function(itemId){
                backend.storeSelectedItem(itemId)
                stack.replace(itemsView, spiralView)
            }
        }
    }

    // SPIRAL VIEW
    Component{
        id: spiralView
        SpiralView{
            onMoveBack: function(){
                stack.replace(spiralView, itemsView)
            }
            onSelectSpiral: function(spiralNo){
                txtProcessResult.text = '';
                popupLoading.open();
                delay(500, function(){
                    try{
                        backend.requestPushSpiral(parseInt(spiralNo));
                    } catch(err){

                    }
                });
            }
        }
    }

    // END DELIVERY
    Component{
        id: endDelivery
        EndDeliveryView{
            onMoveHome: function(){
                stack.replace(endDelivery, cardRead)
                keyListenerRect.focus = true;
            }
        }
    }

    // QUICK DELIVERY
    Component{
        id: quickDelivery
        QuickDeliveryView{
            onMoveBack: function(){
                stack.replace(quickDelivery, userHome)
            }
            onConfirmQuickDelivery: function(spiralNo){
                txtProcessResult.text = '';
                popupLoading.open();
                delay(500, function(){
                    try {
                        backend.requestPushSpiral(parseInt(spiralNo));
                    } catch(err){

                    }
                });
            }
        }
    }

    // BUSY INDICATOR
    Popup {
        id: popupLoading
        modal: true
        dim: true
        Overlay.modal: Rectangle {
            color: "#aacfdbe7"
        }

        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        width: 300
        height: 300

        Label{
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            text:'İşleminiz Gerçekleştiriliyor'
            font.bold: true
        }

        BusyIndicator {
            id: loadingIndicator
            anchors.centerIn: parent
            running: true
        }

        Label{
            anchors.top: loadingIndicator.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            color:'red'
            id: txtProcessResult
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            anchors.topMargin: 10
            wrapMode: Label.Wrap
            text:''
            font.bold: true
        }

        Button{
            text: "TAMAM"
            visible: txtProcessResult.text.length > 0
            onClicked: function(){
                popupLoading.close();
            }
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: txtProcessResult.bottom
            anchors.topMargin: 10
            id:control
            font.pixelSize: 24
            font.bold: true
            padding: 5
        }
    }

    // MAIN LAYOUT
    Rectangle{
        id:keyListenerRect
        
        anchors.fill: parent
        color: "#c8cacc"
        focus: true
        Keys.onPressed: {
            try {
                if (stack.currentItem.toString().indexOf('CardReadView') > -1){
                    let readVal = event.text.match(/^[a-z0-9]+/i);
                    if (readVal && readVal.length > 0)
                        backend.cardReading(readVal);
                }
            } catch (error) {
                backend.cardReading(event.text);
            }
        }

        ColumnLayout{
            anchors.fill:parent

            RowLayout{
                Layout.fillWidth: true
                Layout.preferredHeight: 100

                Rectangle{
                    Layout.fillWidth: true
                    height:60
                    color: "transparent"
                    Image {
                        sourceSize.width: 350
                        sourceSize.height: 100
                        fillMode: Image.Stretch
                        source: "asset/appicon.png"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                showConfigView()
                            }
                        }
                    }
                }

                Text {
                    id: globalTime
                    Layout.preferredWidth: 230
                    color:"#fefefe"
                    padding: 10
                    font.pixelSize: 36
                    style: Text.Outline
                    styleColor:'black'
                    font.bold: true
                    text: Qt.formatTime(new Date(), "hh:mm:ss")
                }

                Timer {
                    interval: 1000
                    repeat: true
                    running: true
                    onTriggered:
                    {
                        globalTime.text = Qt.formatTime(new Date(),"hh:mm:ss")
                    }
                }
            }

            StackView {
                id: stack
                initialItem: cardRead
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }
}
