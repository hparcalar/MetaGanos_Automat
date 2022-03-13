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
                stack.replace(spiralView, endDelivery)
            }
            else
            {
                pushErrorDialog.text = pushResult.ErrorMessage;
                pushErrorDialog.visible = true;
                tmrPushError.running = true;
            }
        }
    }

    // ON LOAD EVENTS & UI FUNCTIONS
    Component.onCompleted: function(){
        backend.checkMachineConfig()
    }

    function showConfigView(){
        stack.replace(stack.currentItem, machineConfig)
    }

    // COMPONENT DECLARATIONS

    // MACHINE CONFIG VIEW
    Component{
        id:machineConfig
        MachineConfigView{
            onCompleted: function(){
                stack.replace(machineConfig, cardRead)
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
                stack.replace(cardRead, userHome)
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
                backend.requestPushSpiral(parseInt(spiralNo))
            }
        }
    }

    // END DELIVERY
    Component{
        id: endDelivery
        EndDeliveryView{
            onMoveHome: function(){
                stack.replace(endDelivery, cardRead)
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
                console.log('Selected spiral no: ' + spiralNo);
                stack.replace(quickDelivery, endDelivery)
            }
        }
    }

    // MAIN LAYOUT
    Rectangle{
        anchors.fill: parent
        color: "#c8cacc"
        focus: true
        Keys.onPressed: {
            if (stack.currentItem.toString().indexOf('CardReadView') > -1){
                if (event.text.match(/^[a-z0-9]+$/i))
                    backend.cardReading(event.text)
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
