import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.2
import QtMultimedia 5.12
import QtGraphicalEffects 1.0

Item {
    property StackView view
    signal moveNextStep()

    Rectangle{
        id: mainRect
        anchors.fill: parent
        color: "#333333"

        ColumnLayout{
            anchors.fill: parent
            spacing:5

            // VIDEO PLAYER
            Rectangle{
                Layout.fillWidth: true
                Layout.fillHeight: true

                gradient: Gradient
                {
                    GradientStop {position: 0.000;color: "#c8cacc";}
                    GradientStop {position: 1.000;color: "#333";}
                }

                Rectangle{
                    anchors.centerIn: parent
                    width: mainRect.width / 1.3 + 50
                    height: mainRect.height / 1.35 + 50
                    border.color: "black"
                    border.width: 50
                    color:"black"

                    MediaPlayer {
                        id: mediaPlayer
                        objectName: "mainVideoPlayer"
                        autoPlay: true
                        autoLoad: true
                        source:"../video/welcome.mp4"
                        onStopped: mediaPlayer.play()
                    }

                    VideoOutput {
                        anchors.centerIn: parent
                        width: mainRect.width / 1.3
                        height: mainRect.height / 1.35
                        id:videoOutput
                        Layout.fillWidth: true
                        source:mediaPlayer
                    }
                }
            }

            // VIEW DESCRIPTION TEXT
            Rectangle{
                Layout.preferredHeight: 200
                Layout.fillWidth: true
                color:"transparent"

                Text {

                    anchors.centerIn: parent
                    Layout.fillHeight: true
                    color:"#fefefe"
                    padding: 10
                    font.pixelSize: 48
                    style: Text.Outline
                    styleColor:'red'
                    font.bold: true
                    text: "Lütfen Kartınızı Okutunuz"
                    MouseArea {
                        signal onCardRead
                        objectName: "cardReadButton"
                        anchors.fill: parent
                        onClicked: moveNextStep()
                    }
                }
            }
        }
    }
}