import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtQuick.Controls.Styles 1.0
import QtGraphicalEffects 1.0

Item {
    signal moveItemGroups(int categoryId)
    signal moveQuickDelivery()
    signal moveCardRead()

    // UI FUNCTIONS
    function userLogout(){
        backend.requestLogout();
    }

    function createCategories(categories){
        if (categories){
            var perRowCount = categories.length / 2;
            var dataIndex = 0;

            // fill first row
            while (dataIndex < perRowCount){
                if (categories.length <= dataIndex)
                    break;

                var cat = categories[dataIndex];

                cmpItemCategory.createObject(topCategoryPanel, {
                    categoryId: cat['Id'],
                    categoryName: cat['ItemCategoryName'],
                    categoryImage: cat['CategoryImage'],
                    perRowCount: perRowCount,
                    activeCredit: cat['ActiveCredit'],
                })
                dataIndex++;
            }

            // fill second row
            while (dataIndex < categories.length){
                if (categories.length <= dataIndex)
                    break;

                var cat = categories[dataIndex];

                cmpItemCategory.createObject(bottomCategoryPanel, {
                    categoryId: cat['Id'],
                    categoryName: cat['ItemCategoryName'],
                    categoryImage: cat['CategoryImage'],
                    activeCredit: cat['ActiveCredit'],
                    perRowCount: perRowCount,
                })
                dataIndex++;
            }
        }
    }

    // ON LOAD EVENT
    Component.onCompleted: function(){
        backend.requestUserData()
        backend.requestItemCategories()
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

        function onUserLoggedOut(){
            moveCardRead();
        }

        function onGetItemCategories(data){
            createCategories(JSON.parse(data));
        }
    }

    // CATEGORY COMPONENT
    Component{
        id: cmpItemCategory

        Rectangle{
            property int categoryId
            property string categoryName
            property string categoryImage
            property int perRowCount
            property int activeCredit

            Layout.preferredWidth: mainColumn.width / perRowCount
            Button{
                onClicked: moveItemGroups(categoryId)
                background:Rectangle {
                    border.width: control.activeFocus ? 2 : 1
                    border.color: "orange"
                    color: "#fff"
                    radius: 4
                }
                anchors.centerIn: parent
                height:mainColumn.height / 5
                width: mainColumn.width / (perRowCount + 1)

                Image {
                    anchors.centerIn: parent
                    sourceSize.height: mainColumn.height / 5 - 10
                    sourceSize.width: mainColumn.width / (perRowCount + 1) - 10
                    fillMode: Image.Stretch
                    source: categoryImage
                }

                // Label{
                //     color: "orange"
                //     anchors.bottom: parent.bottom
                //     anchors.top: parent.bottom
                //     anchors.left: parent.left
                //     anchors.right: parent.right
                //     horizontalAlignment: Text.AlignHCenter 
                //     text: activeCredit.toString() + ' Adet'
                //     font.bold: true
                //     font.pixelSize: 36
                // }
            }
        }
    }

    // PAGE LAYOUT
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
                        id: topCategoryPanel
                        Layout.fillWidth: true
                        Layout.preferredHeight: mainColumn.height / 3
                    }

                    RowLayout{
                        id: bottomCategoryPanel
                        Layout.fillWidth: true
                        Layout.preferredHeight: mainColumn.height / 4
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
                    onClicked: userLogout()
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
