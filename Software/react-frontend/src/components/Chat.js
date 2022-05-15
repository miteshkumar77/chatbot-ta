import React, { useState, createRef, useEffect } from 'react'
import '../css/chat.css';
import { Form, FormGroup, Button, InputGroup } from 'react-bootstrap';
import Spinner from 'react-bootstrap/Spinner';
import Pane from './Pane';

export default function Chat({ sendMessage, messageText, messageList, addMessage, updateMessageText, loading, resetChat}) {


    const bottom = createRef();

    const scrollToBottom = () => {
        console.log("scrolling to bottom");
        bottom.current.scrollIntoView();
    };



    return (
        <div>
            <main className="messagesWindow" style={{paddingLeft: "10%", paddingRight: "10%"}}>
                {
                    messageList.map((message, index) => {
                        return (<Pane
                            heading={message.heading}
                            description={message.description}
                            link={message.link}
                            user={message.user}
                            key={index}
                        />);
                    })
                }
                <div ref={bottom} />
            </main>
            <Form onSubmit={(e) => {
                e.preventDefault();
                console.log("In Form Submit");
                console.log(messageText);
                if (messageText.length !== 0) {
                    addMessage({ 
                        user: 1,
                        heading: messageText,
                        description: '',
                        link: []
                     });
                    scrollToBottom();
                    sendMessage(messageText);

                }
                console.log(messageList);
                updateMessageText("");
            }}>
                <FormGroup >
                    <Form.Control placeholder="type a message" value={messageText} onChange={(e) => { updateMessageText(e.target.value) }} />
                    <Button type="submit">
                        {
                            loading === true
                                ? <Spinner animation="border" size="sm"></Spinner>
                                : <div>Send</div>
                        }
                    </Button>
                    <Button onClick={resetChat}>Reset</Button>
                </FormGroup>
            </Form>
        </div>
    );
}
