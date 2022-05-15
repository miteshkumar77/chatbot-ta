import React from "react";
import "../css/dash.css";
import Tab from "react-bootstrap/Tab";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Nav from "react-bootstrap/Nav";
import DataTable from "./DataTable";
import ChatLogsTable from "./ChatLogsTable";
import { useState, useEffect } from "react";
import conf from "../config";
const SERVER_URL = conf.SERVER_URL;

function InstructorDashboard() {
  const [searchData, setSearchData] = useState([]);
  const [chatData, setChatData] = useState([]);

  useEffect(() => {
    console.log("useEffect");

    fetch(new URL("/fetch_search", SERVER_URL).href).then((res) =>
      res.json().then((data) => {
        console.log(data);
        setSearchData(data);
      })
    );
    fetch(new URL("fetch_chat", SERVER_URL).href).then((res) =>
      res.json().then((data) => {
        console.log(data);
        setChatData(data);
      })
    );
  }, []);

  return (
    <Tab.Container id="left-tabs-example" defaultActiveKey="first">
      <Row id="tabs-container">
        <Col sm={4}>
          <Nav variant="pills" className="flex-column">
            <Nav.Item>
              <Nav.Link eventKey="first">Search Logs</Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link eventKey="second">Unanswerable Queries</Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link eventKey="third">Chat Logs</Nav.Link>
            </Nav.Item>
          </Nav>
        </Col>
        <Col sm={8}>
          <Tab.Content>
            <Tab.Pane id="tab-1" eventKey="first">
              <DataTable tableData={searchData}></DataTable>
            </Tab.Pane>
            <Tab.Pane id="tab-2" eventKey="second">
              <h2 style={{ color: "white" }}>
                To be implemented: table for unanswerable queries
              </h2>
            </Tab.Pane>
            <Tab.Pane id="tab-3" eventKey="third">
              <ChatLogsTable tableData={chatData}></ChatLogsTable>
            </Tab.Pane>
          </Tab.Content>
        </Col>
      </Row>
    </Tab.Container>
  );
}

export default InstructorDashboard;
