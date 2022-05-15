import "../css/index.css";
import React from "react";
import { useEffect, useState } from "react";
import Chat from "./Chat";
import SearchWindow from "./SearchWindow";
import conf from "../config";
const SERVER_URL = conf.SERVER_URL;
export default function InteractionWindow({ type }) {
  var [query, setQuery] = useState("");
  var [cardData, setCardData] = useState([]);

  var [nodeId, setNodeId] = useState("entry");
  var [messageList, setMessageList] = useState([
    { user: 0, heading: "Ask a question", description: '', link: '' }
  ]);
  var [messageText, setMessageText] = useState("");
  var [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);

  function resetChat(){
    setMessageList([
      { user: 0, heading: "Ask a question", description: '', link: '' }
    ]);
    setNodeId('entry');
  }

  function handleQueryChange(e) {
    setQuery(e.target.value);
  }

  function handleCardDataChange(data) {
    setCardData(data);
  }

  function handleNodeIDChange(node_id) {
    setNodeId(node_id);
  }

  function addMessage(data) {
    setMessageList((messageList) => [...messageList, data]);
  }

  function handleMessageTextChange(text) {
    setMessageText(text);
  }

  function handleLoadingChange(bool) {
    setLoading(bool);
  }

  const sendMessage = async (e) => {
    setLoading(true);
    console.log("Sending Query");
    var data = { node_id: nodeId, question: messageText };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch(new URL("/tree_next", SERVER_URL).href, requestOptions).then((res) =>
      res.json().then((data) => {
        console.log(data);
        setNodeId(data.node_id);
        addMessage({ 
          user: 0, 
          heading: data.display.prompt,  
          description: data.display.description,
          link: data.display.links
        });
        setLoading(false);
      })
    );
    console.log("After response");
  };

  const sendQuery = async (e) => {
    setSearchLoading(true);
    console.log(searchLoading);
    console.log("Sending Query");
    var data = { question: query };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    // const response = await fetch("http://localhost:8000/ask", requestOptions);
    // const d = await response.json();
    // console.log(d);
    fetch(new URL("/ask", SERVER_URL).href, requestOptions).then((res) =>
      res.json().then((data) => {
        console.log(data);
        setCardData(data.answers);
        setSearchLoading(false);
        // create json here
      })
    );
    console.log("After response");
  };

  useEffect(() => {
    var data = { node_id: "entry" };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch(new URL("/tree_get", SERVER_URL).href, requestOptions).then((res) =>
      res.json().then((data) => {
        console.log(data);
      })
    );
    console.log("After response");
  });

  return (
    <>
      <div>
        {type === "search" ? (
          <SearchWindow
            updateQuery={handleQueryChange}
            sendQuery={sendQuery}
            cardData={cardData}
            searchLoading={searchLoading}
          ></SearchWindow>
        ) : (
          <Chat
            updateNodeID={handleNodeIDChange}
            messageList={messageList}
            messageText={messageText}
            addMessage={addMessage}
            updateMessageText={handleMessageTextChange}
            updateLoading={handleLoadingChange}
            sendMessage={sendMessage}
            resetChat={resetChat}
          ></Chat>
        )}
      </div>
    </>
  );
}
