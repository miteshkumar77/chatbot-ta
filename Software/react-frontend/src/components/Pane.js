import React from 'react'
// import { Card, CardBody, Badge, Alert } from "shards-react";
import { Alert } from 'react-bootstrap';
import "bootstrap/dist/css/bootstrap.min.css";
// import "shards-ui/dist/css/shards.min.css"

const themes = ["secondary", "success", "info", "warning", "danger", "light", "dark"];
// own ? "text-align:right" : "text-align:left"
function Pane({ user, heading, description, link }) {
    return (
        <div style={{ width: '100%' }}>
            {user === 0 ?
                <Alert variant='light' style={{ float: 'left', width: '60%' }}  >
                    <Alert.Heading>{heading}</Alert.Heading>
                    <p>{description}</p>
                    <hr></hr>
                    <Alert.Link href={link[0]}>{link[0]}</Alert.Link>  
                </Alert>
                :
                <Alert variant='dark' style={{ float: 'right', width: '60%' }}  >
                    <Alert.Heading>{heading}</Alert.Heading>
                </Alert>

            }
        </div>
    );
}

export default Pane