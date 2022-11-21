import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Styles 1.0
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.0

Item {
    signal moveBack()
    signal moveSpiralView(int itemId)

     // ON LOAD EVENT
    Component.onCompleted: function(){
        backend.requestUserData()
        backend.requestProperItems()
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

        function onGetItems(data){
            createItems(JSON.parse(data));
        }
    }

    // UI FUNCTIONS
    function createItems(itemInfo){
        if (itemInfo){
            txtItemGroupName.text = itemInfo['groupName'];

            for (let i = 0; i < itemInfo['items'].length; i++) {
                const itemObj = itemInfo['items'][i];
                
                cmpItem.createObject(itemContainer, {
                    itemId: itemObj['Id'],
                    groupImage: itemObj['ItemImage'],
                    itemName: itemObj['ItemName']
                });
            }
        }
    }

    function selectItem(itemId){
        moveSpiralView(itemId)
    }

    // DYNAMIC COMPONENT DEFINITION
    Component{
        id: cmpItem

         Button{
            property int itemId
            property string itemName
            property string groupImage

            onClicked: selectItem(itemId)
            background:Rectangle {
                border.width: 1
                border.color: "orange"
                color: "#fff"
                radius: 4
            }
            contentItem: Label {
                text:itemName
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin:2
                font.pointSize: 24
                font.bold: true
                fontSizeMode: Text.HorizontalFit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignTop
                wrapMode: Label.Wrap
            }

            height:mainColumn.height / 5 - 10
            width: mainColumn.width / 4 - 13

            Image {
                visible: groupImage != null && groupImage.length > 0
                opacity: 1
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                anchors.topMargin:30
                sourceSize.width: parent.width - 10
                sourceSize.height: parent.height / 2 - 13
                
                fillMode: Image.PreserveAspectFit
                source: groupImage
            }
        }
    }

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

            // SELECTED ITEM GROUP OR CATEGORY TEXT
            Rectangle{
                Layout.fillWidth: true
                Layout.preferredHeight:60
                color:"orange"
                Text {
                    id: txtItemGroupName
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

            // ITEM GROUP ITEMS FLOW
            Rectangle{
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "transparent"

                Flow{
                    id: itemContainer
                    width: parent.width
                    padding: 10
                    spacing: 10
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
