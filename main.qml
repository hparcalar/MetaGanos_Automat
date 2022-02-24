import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtMultimedia 5.12
import "components"

ApplicationWindow {
    width: screen.desktopAvailableWidth
    height: screen.desktopAvailableHeight
    flags: Qt.WindowMaximized | Qt.FramelessWindowHint | Qt.Window
    visible: true
    title: qsTr("MetaGanos Otomat")

    // BACKEND SIGNALS & SLOTS
    Connections {
        target: backend

    }

    Component.onCompleted: function(){
        
    }

    // COMPONENT DECLARATIONS

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
            onMoveItemGroups: function(groupId){
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
                console.log('Selected spiral no: ' + spiralNo)
                stack.replace(spiralView, endDelivery)
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
