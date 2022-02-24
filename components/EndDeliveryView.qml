import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2

Item {
    signal moveHome()

    Timer {
        id: tmrSignout
        interval: 3000
        repeat: false
        running: false
        onTriggered: {
            moveHome()
            this.destroy()
        }
    }

    Component.onCompleted: function(){
        tmrSignout.running = true;
    }

    Rectangle{
        anchors.fill: parent
        color: "#333333"

        ColumnLayout{
            id: mainColumn
            anchors.fill: parent
            spacing:0

            // END DELIVERY MESSAGE
            Rectangle{
                Layout.fillHeight: true
                Layout.fillWidth: true
                color:"transparent"

                Text {
                    width: parent.width
                    anchors.centerIn: parent
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.Wrap
                    color:"#fff"
                    padding: 2
                    font.pixelSize: 72
                    style: Text.Outline
                    styleColor:'orange'
                    font.bold: true
                    text: "Sağlıklı Günler Dileriz"
                }

            }
        }
    }
}
