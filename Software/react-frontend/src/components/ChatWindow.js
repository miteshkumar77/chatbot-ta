import React from 'react'
import Chat from './Chat';
import "bootstrap/dist/css/bootstrap.min.css";

export default class Main extends React.Component {

  constructor(props) {
    this.state = {
      messages: [],
    }
  }
  onMessageHandler = (e) => {
    let start = Math.max(0, this.state.messages.length - 10);
    let incomingMessage = JSON.parse(e.data);
    console.log(e.timestamp);
    console.log("incoming message: ");
    console.log(incomingMessage);
    this.setState({
      messages: [
        ...this.state.messages.slice(start, this.state.messages.length),
        incomingMessage
      ]
    });
  }


  sendMessage = (messageText) => {
    this.state.messages.push(messageText);

  }

  render() {
    const { messages } = this.state;
    return (
      <Chat
        sendMessageFunc={this.sendMessage}
        messageList={messages}
      />
    )
  }
}