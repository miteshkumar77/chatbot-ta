import '../css/index.css';
import React from 'react';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Component from "./Component";
import Spinner from 'react-bootstrap/Spinner';


export default function SearchWindow({ updateQuery, sendQuery, cardData, searchLoading}) {
    return (
        <>
            <div>
                <Form className="centered-form" >
                    <Form.Group className="mb-3" >
                        <FloatingLabel controlId="floatingInput" label="Query">
                            <Form.Control type="input" onChange={updateQuery} placeholder="Query" />
                        </FloatingLabel>
                        <Button className="float-end" variant="danger" onClick={sendQuery}>
                            {
                                searchLoading === true
                                    ? <Spinner animation="border" size="sm"></Spinner>
                                    : <div>Send</div>
                            }
                        </Button>
                    </Form.Group>
                    <br></br>
                    <div id="cardholder">
                        {
                            cardData.length === 0
                                ? <h1 style={{ color: 'white' }}> Your query had 0 results. Try modifying your query. </h1>
                                : cardData.map((block, key) => Component(block, key))
                            // : <h1> Test2 </h1>
                        }
                    </div>
                </Form>
            </div>
        </>
    );

}